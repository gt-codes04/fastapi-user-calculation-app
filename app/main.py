# app/main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.db import Base, engine
from app.routers import users, calculations

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User & Calculation App")

# Include routers
app.include_router(users.router)
app.include_router(calculations.router)

# ---- Frontend files setup ----
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
FRONTEND_DIR = BASE_DIR / "frontend"


def _read_frontend_file(filename: str) -> str:
    file_path = FRONTEND_DIR / filename
    if not file_path.exists():
        # Helpful message if file is missing
        return f"<h1>File not found: {file_path}</h1>"
    return file_path.read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
def index():
    # Simple home page so / is not 404 anymore
    return """
    <h1>FastAPI User & Calculation App</h1>
    <ul>
      <li><a href="/register-page">Register Page</a></li>
      <li><a href="/login-page">Login Page</a></li>
      <li><a href="/docs">OpenAPI Docs</a></li>
    </ul>
    """


@app.get("/register-page", response_class=HTMLResponse)
def register_page():
    return _read_frontend_file("register.html")


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    return _read_frontend_file("login.html")
