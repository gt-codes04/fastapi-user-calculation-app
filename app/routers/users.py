from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.db import get_db 
from app.security import verify_password

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, user_in)
    if not user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return user  # <-- return the SQLAlchemy user object

@router.post("/login")
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Simple login:
    - Look up user by username
    - Check password
    - Return 200 on success, 401 on failure
    """
    user = crud.get_user_by_username(db, user_in.username)
    if not user or not verify_password(user_in.password, user.password_hash):
        # tests expect 401 for bad credentials
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {
        "message": "Login successful",
        "user_id": user.id
    }



