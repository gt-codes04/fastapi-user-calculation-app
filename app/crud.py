# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


# =======================
# USER CRUD
# =======================

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# =======================
# CALCULATIONS CRUD
# =======================

def _compute(a: float, b: float, type: str) -> float:
    if type == "add":
        return a + b
    if type == "sub":
        return a - b
    if type == "mul":
        return a * b
    if type == "div":
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    if type == "pow":
        return a ** b
    raise ValueError("Invalid operation type")

def create_calculation(db: Session, calc_in: schemas.CalculationCreate, user_id: int):
    result = _compute(calc_in.a, calc_in.b, calc_in.type)
    calc = models.Calculation(
        a=calc_in.a,
        b=calc_in.b,
        type=calc_in.type,
        result=result,
        user_id=user_id
    )
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc

def get_calculations(db: Session, user_id: int):
    return db.query(models.Calculation).filter(models.Calculation.user_id == user_id).all()

def get_calculation(db: Session, calc_id: int, user_id: int):
    return (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calc_id,
                models.Calculation.user_id == user_id)
        .first()
    )

def update_calculation(db: Session, calc: models.Calculation, data: schemas.CalculationUpdate):
    if data.a is not None:
        calc.a = data.a
    if data.b is not None:
        calc.b = data.b
    if data.type is not None:
        calc.type = data.type

    calc.result = _compute(calc.a, calc.b, calc.type)

    db.commit()
    db.refresh(calc)
    return calc

def delete_calculation(db: Session, calc):
    db.delete(calc)
    db.commit()


# =======================
# REPORTS CRUD
# =======================

def get_report_summary(db: Session, user_id: int):
    rows = db.query(models.Calculation).filter(models.Calculation.user_id == user_id)

    total = rows.count()
    avg_a = rows.with_entities(func.avg(models.Calculation.a)).scalar() or 0
    avg_b = rows.with_entities(func.avg(models.Calculation.b)).scalar() or 0

    # count by operation type
    op_counts = (
        db.query(models.Calculation.type, func.count(models.Calculation.id))
        .filter(models.Calculation.user_id == user_id)
        .group_by(models.Calculation.type)
        .all()
    )

    operation_dict = {op: count for op, count in op_counts}

    return schemas.ReportSummary(
        total=total,
        avg_a=float(avg_a),
        avg_b=float(avg_b),
        operations=operation_dict,
    )



