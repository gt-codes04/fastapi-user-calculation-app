# app/main.py
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.db import Base, engine
from app import models
from app.routers import users, calculations, reports

# ----------------- DB SETUP -----------------
# Make sure tables are created
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ----------------- FRONTEND PATHS -----------------
# main.py is in app/, so parent is the project root
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def load_html(filename: str) -> str:
    """Load an HTML file from the root-level frontend/ folder."""
    file_path = FRONTEND_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    return file_path.read_text(encoding="utf-8")
# --------------------------------------------------


# ----------------- PAGE ROUTES -----------------
@app.get("/register-page", response_class=HTMLResponse)
def register_page():
    return load_html("register.html")


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return load_html("login.html")


@app.get("/calculations-page", response_class=HTMLResponse)
def calculations_page():
    return load_html("calculations.html")


@app.get("/report-page", response_class=HTMLResponse)
def report_page():
    return load_html("reports.html")


@app.get("/profile-page", response_class=HTMLResponse)
def profile_page():
    # NEW final-project feature page
    return load_html("profile.html")
# --------------------------------------------------


# ----------------- API ROUTERS -----------------
# /users/register, /users/login, etc.
app.include_router(users.router)
# /calculations/...
app.include_router(calculations.router)
# /reports/stats, etc.
app.include_router(reports.router)
# --------------------------------------------------