from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.dependencies import get_current_user   # adjust if needed

templates = Jinja2Templates(directory="templates")

router = APIRouter()

@router.get("/ui/calculations")
def ui_calculations(request: Request, current_user=Depends(get_current_user)):
    return templates.TemplateResponse(
        "calculations.html",
        {"request": request, "user": current_user},
    )
