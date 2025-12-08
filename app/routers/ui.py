# app/routers/ui.py

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["default"])

# All paths are relative to the project root where you run `uvicorn app.main:app`

@router.get("/register-page")
def register_page():
    return FileResponse("frontend/register.html")


@router.get("/login-page")
def login_page():
    return FileResponse("frontend/login.html")


@router.get("/calculations-page")
def calculations_page():
    return FileResponse("frontend/calculations.html")


@router.get("/report-page")
def report_page():
    return FileResponse("frontend/reports.html")


@router.get("/profile-page")
def profile_page():
    # NEW final-project feature page
    return FileResponse("frontend/profile.html")

