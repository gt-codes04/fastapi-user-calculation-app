# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password, verify_password  # make sure both are imported


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user_in: schemas.UserCreate):
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


# --- CALCULATION CRUD ---
from sqlalchemy.exc import IntegrityError

def get_calculation(db: Session, calc_id: int):
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()

def get_calculations(db: Session):
    return db.query(models.Calculation).all()

def create_calculation(db: Session, calc_in: schemas.CalculationCreate, owner_id: int = None):
    # Validate calculation type
    valid_types = {"add", "sub", "mul", "div", "subtract", "multiply", "divide"}
    if calc_in.type not in valid_types:
        raise ValueError("Invalid calculation type")

    # Perform calculation
    if calc_in.type in ("add",):
        result = calc_in.a + calc_in.b
    elif calc_in.type in ("sub", "subtract"):
        result = calc_in.a - calc_in.b
    elif calc_in.type in ("mul", "multiply"):
        result = calc_in.a * calc_in.b
    elif calc_in.type in ("div", "divide"):
        if calc_in.b == 0:
            raise ValueError("Division by zero")
        result = calc_in.a / calc_in.b
    else:
        raise ValueError("Invalid calculation type")

    if owner_id is None:
        raise ValueError("owner_id (user_id) is required for calculation creation")
    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=owner_id
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

def update_calculation(db: Session, calc, data: schemas.CalculationUpdate):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(calc, field, value)
    db.commit()
    db.refresh(calc)
    return calc

def delete_calculation(db: Session, calc):
    db.delete(calc)
    db.commit()


