import uuid
from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.application.models.user import UserExtended
from backend.application.settings import settings
from backend.database.daos.base_dao import BaseDao
from backend.database.tables import Session


class AuthDao(BaseDao):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Session

    @staticmethod
    def generate_refresh_token() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def authenticate_by_access_token(access_token: str) -> UserExtended:
        try:
            data = jwt.decode(
                access_token, settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(401,
                                "Access token expired")

        return UserExtended(**data["user"])

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        result = await self.session.execute(
            select(self.model).filter_by(token=refresh_token).options(
                joinedload(self.model.user)))
        data = result.scalar_one_or_none()

        if not (session := data.scalar_one_or_none()):
            raise HTTPException(401, "Refresh token is invalid")
        if session.expires < datetime.utcnow():
            raise HTTPException(401, "Refresh token expired")

        user_info = UserExtended.from_orm(session.user).dict()
        user_info["registered_at"] = user_info["registered_at"].isoformat()

        session = Session(
            user_id=session.user_id,
            token=AuthDao.generate_refresh_token(),
            expires=datetime.utcnow()
                    + timedelta(days=settings.ACCESS_TOKEN_DURATION_MINUTES)
        )
        await self.add(session)
        refresh_token = session.token

        access_token = jwt.encode(
            {
                "user": user_info,
                "exp": datetime.utcnow()
                       + timedelta(
                    minutes=settings.ACCESS_TOKEN_DURATION_MINUTES),
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        return refresh_token, access_token

    async def issue_tokens(self, user_id: int) -> tuple[str, str]:
        session = Session(
            user_id=user_id,
            token=AuthDao.generate_refresh_token(),
            expires=datetime.utcnow()
                    + timedelta(days=settings.ACCESS_TOKEN_DURATION_MINUTES)
        )
        await self.add(session)
        refresh_token = session.token

        user_info = UserExtended.from_orm(session.user).dict()
        user_info["registered_at"] = user_info["registered_at"].isoformat()

        access_token = jwt.encode(
            {
                "user": user_info,
                "exp": datetime.utcnow()
                       + timedelta(
                    minutes=settings.ACCESS_TOKEN_DURATION_MINUTES),
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        return refresh_token, access_token
