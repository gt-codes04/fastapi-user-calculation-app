from fastapi import FastAPI
from app.db import Base, engine
from app.routers import users, calculations

# Create tables (for local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI User & Calculation App")

app.include_router(users.router)
app.include_router(calculations.router)


@app.get("/")
def root():
    return {"message": "Backend is running"}

