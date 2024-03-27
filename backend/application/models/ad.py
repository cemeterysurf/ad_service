from datetime import datetime

from backend.application.models.base import BaseModel
from backend.database.tables import AdType
from .user import UserExtended


class AdAdd(BaseModel):
    title: str
    body: str
    compensation: str = None
    location: str = None
    type: AdType


class AdFilter(BaseModel):
    title: str = None
    body: str = None
    type: AdType = None
    user_id: int = None


class AdExtended(AdAdd):
    id: int
    created_at: datetime
    updated_at: datetime
    user: UserExtended
