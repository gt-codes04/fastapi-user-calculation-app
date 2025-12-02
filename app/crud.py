# app/crud.py
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .security import hash_password

# ---------------- USER HELPERS ---------------- #


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    """
    Idempotent create: if email already exists, return existing user instead
    of raising a UNIQUE constraint error.
    """
    existing = get_user_by_email(db, user_in.email)
    if existing:
        return existing

    hashed = hash_password(user_in.password)
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------- CALCULATION HELPERS ---------------- #

VALID_TYPES = {"add", "sub", "subtract", "mul", "multiply", "div", "divide"}


def _compute_result(a: float, b: float, type_: str) -> float:
    if type_ in ("add",):
        return a + b
    elif type_ in ("sub", "subtract"):
        return a - b
    elif type_ in ("mul", "multiply"):
        return a * b
    elif type_ in ("div", "divide"):
        if b == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Division by zero",
            )
        return a / b
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid calculation type",
        )


def get_calculation(db: Session, calc_id: int) -> Optional[models.Calculation]:
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()


def get_calculations(db: Session):
    return db.query(models.Calculation).all()


def create_calculation(
    db: Session,
    calc_in: schemas.CalculationCreate,
    owner_id: Optional[int] = None,
) -> models.Calculation:
    if owner_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="owner_id is required for calculation creation",
        )

    if calc_in.type not in VALID_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid calculation type",
        )

    result = _compute_result(calc_in.a, calc_in.b, calc_in.type)

    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=owner_id,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def update_calculation(
    db: Session,
    calc: models.Calculation,
    data: schemas.CalculationUpdate,
) -> models.Calculation:
    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(calc, field, value)

    # If a, b or type changed, recompute result
    if any(k in update_data for k in ("a", "b", "type")):
        if calc.type not in VALID_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid calculation type",
            )
        calc.result = _compute_result(calc.a, calc.b, calc.type)

    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc: models.Calculation) -> None:
    db.delete(calc)
    db.commit()



