from fastapi import APIRouter, Depends

from backend.application.views.dependencies import (
    get_user_dao
)
from backend.database.daos import UserDao
from .auth import get_current_user

web_router = APIRouter(tags=['User'])


@web_router.post("/{user_id}/make-admin")
async def make_admin(user_id: int,
                     user_dao: UserDao = Depends(get_user_dao)):
    current_user = await get_current_user()
    await user_dao.make_admin(admin=current_user, user_id=user_id)


@web_router.post("/{user_id/ban")
async def ban_user(user_id: int,
                   user_dao: UserDao = Depends(get_user_dao)):
    current_user = await get_current_user()
    if current_user.is_admin:
        user_to_ban = await user_dao.get_one_by_id(user_id)
        user_to_ban.banned = True


@web_router.post("/{user_id/unban")
async def unban_user(user_id: int,
                     user_dao: UserDao = Depends(get_user_dao)):
    current_user = await get_current_user()
    if current_user.is_admin:
        user_to_unban = await user_dao.get_one_by_id(user_id)
        user_to_unban.banned = False
