# app/schemas.py

from typing import Optional, Dict
from pydantic import BaseModel, EmailStr, Field, ConfigDict


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
    # Pydantic v2-style config for ORM objects
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordChangeRequest(BaseModel):
    # Use Field for min_length instead of constr() to keep Pylance happy
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6)


# =======================
# Calculation Schemas
# =======================

class CalculationBase(BaseModel):
    a: float
    b: float
    type: str  # "add", "sub", "mul", "div", "pow", etc.


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


# =======================
# Report Schema
# =======================

class ReportSummary(BaseModel):
    total: int
    avg_a: float
    avg_b: float
    operations: Dict[str, int]  # or Dict[str, float] if you prefer
