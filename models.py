from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    name: str
    email: str
    user_id: int
    date: Optional[date] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    
class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ItemResponse(BaseModel):
    item_id: int
    user_id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime

class PaginatedItemResponse(BaseModel):
    data: list[ItemResponse]
    page: int
    limit: int
    total: int

    