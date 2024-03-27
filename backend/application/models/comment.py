from datetime import datetime

from backend.application.models.base import BaseModel


class CommentCreate(BaseModel):
    body: str


class CommentExtended(CommentCreate):
    id: int
    created_at: datetime
    created_by: int
