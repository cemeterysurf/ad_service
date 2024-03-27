from datetime import date

from backend.application.models.base import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(UserLogin):
    full_name: str
    email: str
    phone: str


class UserExtended(BaseModel):
    id: int
    username: str
    created_at: date
    full_name: str
    email: str
    phone: str
    is_admin: bool
    is_banned: bool
