# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.db import get_db
from app import models
from app.security import hash_password, verify_password, create_access_token
from app.fake_store import fake_users  # simple in-memory fallback

router = APIRouter(prefix="/users", tags=["users"])


# --------- Helpers --------- #

def _get_user_from_db(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def _create_user_in_db(db: Session, username: str, email: str, password: str):
    hashed = hash_password(password)
    user = models.User(
        username=username,
        email=email,
        password_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# --------- Routes --------- #

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    """
    Register user.

    Request JSON:
      { "username": "...", "email": "...", "password": "..." }

    Success (new or existing user):
      {
        "message": "Registration successful",
        "id": <id>,
        "username": "...",
        "email": "..."
      }
    """
    username = payload.get("username")
    email = payload.get("email")
    password = payload.get("password")

    if not username or not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="username, email, and password are required",
        )

    # --- Try DB path --- #
    try:
        existing = _get_user_from_db(db, email)
        if existing:
            return {
                "message": "Registration successful",
                "id": existing.id,
                "username": existing.username,
                "email": existing.email,
            }

        user = _create_user_in_db(db, username, email, password)
        return {
            "message": "Registration successful",
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
    except Exception:
        # fall back to in-memory store
        pass

    # --- Fallback: in-memory store --- #
    if email in fake_users:
        return {
            "message": "Registration successful",
            "id": -1,
            "username": fake_users[email]["username"],
            "email": email,
        }

    fake_users[email] = {
        "username": username,
        "password": password,
    }

    return {
        "message": "Registration successful",
        "id": -1,
        "username": username,
        "email": email,
    }


@router.post("/login")
def login_user(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
):
    """
    Login user.

    Request JSON:
      { "email": "...", "password": "..." }
    """
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password are required",
        )

    # Try DB first
    user = None
    try:
        user = _get_user_from_db(db, email)
    except Exception:
        user = None

    if user is not None:
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token(str(user.id))
        return {
            "message": "Login successful",
            "user_id": user.id,
            "access_token": token,
            "token_type": "bearer",
        }

    # Fallback: in-memory
    fallback = fake_users.get(email)
    if fallback is None or fallback["password"] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token("fake-user")
    return {
        "message": "Login successful",
        "user_id": -1,
        "access_token": token,
        "token_type": "bearer",
    }

