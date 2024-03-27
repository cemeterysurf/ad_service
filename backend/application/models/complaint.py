from datetime import datetime

from backend.application.models.base import BaseModel


class ComplaintCreate(BaseModel):
    body: str


class ComplaintExtended(ComplaintCreate):
    id: int
    created_at: datetime
    created_by: int
    ad_id: int
