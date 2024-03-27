from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.models.user import UserCreate, UserLogin, UserExtended
from backend.database.daos.base_dao import BaseDao
from backend.database.tables import User


class UserDao(BaseDao):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User

    async def signup(self, user_dto: UserCreate) -> UserExtended:
        await self.add(user_dto)
        user = UserExtended.from_orm(user_dto)
        return user

    async def login(self, user_dto: UserLogin) -> UserExtended:
        result = await self.session.execute(
            select(self.model).filter_by(username=user_dto.username))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(401,
                                f"Username {user_dto.username=} does not exist")

        if not user.verify_password(user_dto.password):
            raise HTTPException(401, f"Wrong password")

        return UserExtended.from_orm(user)

    async def make_admin(self, admin: UserExtended, user_id: int):
        if not admin.is_admin:
            raise HTTPException(403, "No permission")

        result = await self.session.execute(
            select(self.model).filter_by(id=user_id))
        user = result.scalar_one_or_none()
        user_orm = UserExtended.from_orm(user)
        user_orm.is_admin = True
        await self.session.commit()

    async def ban_user(self, user_id):
        result = await self.session.execute(
            select(self.model).filter_by(id=user_id)
        )
        user = result.scalar_one_or_none()
        user_orm = UserExtended.from_orm(user)
        user_orm.is_banned = True
        await self.session.commit()

    async def unban_user(self, user_id):
        result = await self.session.execute(
            select(self.model).filter_by(id=user_id)
        )
        user = result.scalar_one_or_none()
        user_orm = UserExtended.from_orm(user)
        user_orm.is_banned = False
        await self.session.commit()
