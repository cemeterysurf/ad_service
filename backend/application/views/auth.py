from fastapi import (
    HTTPException, Depends, APIRouter, Security, Response, Request
)
from fastapi.security.api_key import APIKeyCookie

from backend.application.models.user import UserExtended, UserCreate
from backend.application.settings import settings
from backend.application.views.dependencies import (
    get_auth_dao, get_user_dao
)
from backend.database.daos import UserDao, AuthDao

web_router = APIRouter(tags=['Auth'])

api_key_refresh = APIKeyCookie(name=settings.REFRESH_TOKEN_COOKIE_NAME,
                               auto_error=False)
api_key_access = APIKeyCookie(name=settings.ACCESS_TOKEN_COOKIE_NAME,
                              auto_error=False)


def get_current_user(
        access_token: str | None = Security(api_key_access),
) -> UserExtended:
    if access_token is None:
        raise HTTPException(401, "Not authenticated")

    user_info = AuthDao.authenticate_by_access_token(access_token)

    if user_info.is_banned:
        raise HTTPException(403, "User is banned")

    return user_info


def get_admin_user(
        user: UserExtended = Depends(get_current_user),
) -> UserExtended:
    if not user.is_admin:
        raise HTTPException(403, "Not an admin")

    return user


def set_cookie_tokens(refresh_token: str, access_token: str, res: Response):
    res.set_cookie(
        settings.ACCESS_TOKEN_COOKIE_NAME,
        access_token,
        max_age=settings.ACCESS_TOKEN_DURATION_MINUTES * 60,
        httponly=True,
        secure=True,
        samesite="strict",
    )
    res.set_cookie(
        settings.REFRESH_TOKEN_COOKIE_NAME,
        refresh_token,
        max_age=settings.REFRESH_TOKEN_DURATION_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/auth/refresh_tokens"
    )


@web_router.post("/signup")
async def signup(
        user_dto: UserCreate,
        req: Request,
        res: Response,
        user_dao: UserDao = Depends(get_user_dao),
        auth_dao: AuthDao = Depends(get_auth_dao)
) -> UserExtended:
    user = await user_dao.signup(user_dto)

    refresh_token, access_token = await auth_dao.issue_tokens(user.id)

    set_cookie_tokens(refresh_token, access_token, res)

    return user


@web_router.post("/login")
async def login(
        user_dto: UserCreate,
        req: Request,
        res: Response,
        user_dao: UserDao = Depends(get_user_dao),
        auth_dao: AuthDao = Depends(get_auth_dao)
) -> UserExtended:
    user = await user_dao.login(user_dto)

    refresh_token, access_token = await auth_dao.issue_tokens(user.id)

    set_cookie_tokens(refresh_token, access_token, res)

    return user


@web_router.post("/refresh_tokens")
async def refresh_tokens(
        res: Response,
        refresh_token: str | None = Security(api_key_refresh),
        auth_dao: AuthDao = Depends(get_auth_dao)
):
    refresh_token, access_token = await auth_dao.refresh_tokens(refresh_token)
    set_cookie_tokens(refresh_token, access_token, res)
