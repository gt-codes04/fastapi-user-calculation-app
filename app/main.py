# app/main.py
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.db import Base, engine
from app.routers import users, calculations

# -----------------------
# Database setup
# -----------------------
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User & Calculation App")

# -----------------------
# Routers
# -----------------------
app.include_router(users.router)
app.include_router(calculations.router)

# -----------------------
# Frontend file loader
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def _read_frontend_file(filename: str) -> str:
    """Return HTML content or a 'not found' message."""
    file_path = FRONTEND_DIR / filename
    if not file_path.exists():
        return f"<h1>File not found: {file_path}</h1>"
    return file_path.read_text(encoding="utf-8")


# -----------------------
# Routes for UI pages
# -----------------------

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <h1>FastAPI User & Calculation App</h1>
    <ul>
      <li><a href="/register-page">Register Page</a></li>
      <li><a href="/login-page">Login Page</a></li>
      <li><a href="/calculations-page">Calculations (BREAD)</a></li>
      <li><a href="/docs">OpenAPI Docs</a></li>
    </ul>
    """


@app.get("/register-page", response_class=HTMLResponse)
def register_page():
    return _read_frontend_file("register.html")


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return _read_frontend_file("login.html")


@app.get("/calculations-page", response_class=HTMLResponse)
def calculations_page():
    return _read_frontend_file("calculations.html")
