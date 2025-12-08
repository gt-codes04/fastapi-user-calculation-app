# app/routers/calculations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import status

from app import schemas, crud
from app.db import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/calculations", tags=["Calculations"])


@router.post("/", response_model=schemas.CalculationRead, status_code=201)
def create_calc(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return crud.create_calculation(db, calc_in, user.id)


@router.get("/", response_model=list[schemas.CalculationRead])
def browse(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_calculations(db, user.id)


@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read(calc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    calc = crud.get_calculation(db, calc_id, user.id)
    if not calc:
        raise HTTPException(404, "Calculation not found")
    return calc


@router.patch("/{calc_id}", response_model=schemas.CalculationRead)
def edit(
    calc_id: int,
    data: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    calc = crud.get_calculation(db, calc_id, user.id)
    if not calc:
        raise HTTPException(404, "Calculation not found")

    return crud.update_calculation(db, calc, data)


@router.delete("/{calc_id}", status_code=200)
def delete(calc_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    calc = crud.get_calculation(db, calc_id, user.id)
    if not calc:
        raise HTTPException(404, "Calculation not found")

    crud.delete_calculation(db, calc)
    return {"detail": "Deleted"}
