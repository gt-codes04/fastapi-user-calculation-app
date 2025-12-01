from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session


from app import schemas, crud
from app.db import get_db
from fastapi import Query

router = APIRouter(prefix="/calculations", tags=["calculations"])


@router.post("/", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def create(
    calc_in: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    owner_id: int = Query(None, alias="owner_id")
):
    try:
        calc = crud.create_calculation(db, calc_in, owner_id=owner_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return calc


@router.get("/", response_model=list[schemas.CalculationRead])
def browse(db: Session = Depends(get_db)):
    return crud.get_calculations(db)


@router.get("/{calc_id}", response_model=schemas.CalculationRead)
def read(calc_id: int, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return calc


@router.put("/{calc_id}", response_model=schemas.CalculationRead)
def update(calc_id: int, data: schemas.CalculationUpdate, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    updated = crud.update_calculation(db, calc, data)
    return updated


@router.delete("/{calc_id}", status_code=status.HTTP_200_OK)
def delete(calc_id: int, db: Session = Depends(get_db)):
    calc = crud.get_calculation(db, calc_id)
    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")
    crud.delete_calculation(db, calc)
    return {"detail": "Calculation deleted"}

