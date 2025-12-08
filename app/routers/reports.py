from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import get_current_user
from app import crud, schemas

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/summary", response_model=schemas.ReportSummary)
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud.get_report_summary(db, user.id)
