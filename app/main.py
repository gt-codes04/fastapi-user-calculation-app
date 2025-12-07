# app/main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.db import Base, engine
from app.routers import users, calculations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User & Calculation App")

app.include_router(users.router)
app.include_router(calculations.router)

# Path to the frontend folder
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def _read_frontend_file(filename: str) -> str:
    file_path = FRONTEND_DIR / filename
    return file_path.read_text(encoding="utf-8")


@app.get("/register-page", response_class=HTMLResponse)
def register_page():
    return _read_frontend_file("register.html")


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return _read_frontend_file("login.html")


@app.get("/calculations-page", response_class=HTMLResponse)
def calculations_page():
    return _read_frontend_file("calculations.html")
