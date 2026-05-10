from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "operator"

class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    role: str
    is_active: bool
    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str