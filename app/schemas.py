from pydantic import BaseModel, EmailStr


# -------- USER SCHEMAS --------
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -------- CALCULATION SCHEMAS --------
class CalculationCreate(BaseModel):
    a: float
    b: float
    type: str  # "add", "sub", "mul", "div"


class CalculationUpdate(BaseModel):
    a: float | None = None
    b: float | None = None
    type: str | None = None
    result: float | None = None


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: float | None = None

    class Config:
        from_attributes = True

