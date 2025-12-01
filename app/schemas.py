from typing import Optional
from pydantic import BaseModel, EmailStr


# ---------- USER SCHEMAS ----------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True  # allow reading from SQLAlchemy model attributes


class UserLogin(BaseModel):
    username: str
    password: str


# ---------- CALCULATION SCHEMAS ----------

class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # e.g. "add", "subtract", "multiply", "divide"


class CalculationCreate(CalculationBase):
    pass


class CalculationRead(CalculationBase):
    id: int
    user_id: int
    result: float

    class Config:
        orm_mode = True  # allow reading from SQLAlchemy model attributes


class CalculationUpdate(BaseModel):
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[str] = None  # allow partial updates
