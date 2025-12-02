# app/schemas.py
from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from pydantic import ConfigDict


# =======================
# User Schemas
# =======================

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    # Used for registration
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    # Used for login
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int

    # Replaces old orm_mode = True
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =======================
# Calculation Schemas
# =======================

class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # "add", "sub", "mul", "div", etc.


class CalculationCreate(CalculationBase):
    # Used when creating a calculation
    pass


class CalculationUpdate(BaseModel):
    # Used when updating a calculation
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[str] = None


class CalculationRead(CalculationBase):
    # What we return to clients
    id: int
    result: float
    user_id: int

    model_config = ConfigDict(from_attributes=True)

