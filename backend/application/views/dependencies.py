from backend.application.settings import settings
from backend.database.daos import (
    AdDao, AuthDao, UserDao, ComplaintDao, CommentDao)
from backend.database.database import Database

db = Database(
    url=settings.DB_URL,
    echo=settings.DEBUG
)


async def start():
    await db.startup()


async def stop():
    await db.shutdown()


async def get_ad_dao() -> AdDao:
    async with db.session() as session:
        async with session.begin():
            yield AdDao(session)


async def get_user_dao() -> UserDao:
    async with db.session() as session:
        async with session.begin():
            yield UserDao(session)


async def get_auth_dao() -> AuthDao:
    async with db.session() as session:
        async with session.begin():
            yield AuthDao(session)


async def get_comment_dao() -> CommentDao:
    async with db.session() as session:
        async with session.begin():
            yield CommentDao(session)


async def get_complaint_dao() -> ComplaintDao:
    async with db.session() as session:
        async with session.begin():
            yield ComplaintDao(session)
