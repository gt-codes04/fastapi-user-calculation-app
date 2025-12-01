from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password


# -------- USER CRUD --------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user_in: schemas.UserCreate):
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


# -------- CALCULATION CRUD --------
def create_calculation(db: Session, calc_in: schemas.CalculationCreate):
    a, b, t = calc_in.a, calc_in.b, calc_in.type
    result = None

    if t == "add":
        result = a + b
    elif t == "sub":
        result = a - b
    elif t == "mul":
        result = a * b
    elif t == "div":
        result = a / b if b != 0 else None

    calc = models.Calculation(
        a=a,
        b=b,
        type=t,
        result=result,
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc


def get_calculations(db: Session):
    return db.query(models.Calculation).all()


def get_calculation(db: Session, calc_id: int):
    return db.query(models.Calculation).filter(models.Calculation.id == calc_id).first()


def update_calculation(db: Session, calc, data: schemas.CalculationUpdate):
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(calc, k, v)
    db.commit()
    db.refresh(calc)
    return calc


def delete_calculation(db: Session, calc):
    db.delete(calc)
    db.commit()

