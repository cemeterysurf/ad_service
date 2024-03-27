from fastapi import APIRouter, Depends

from backend.application.models import (
    CommentCreate, CommentExtended, UserExtended
)
from backend.application.views.auth import get_current_user
from backend.application.views.dependencies import (
    get_comment_dao
)
from backend.database.daos import CommentDao

web_router = APIRouter(tags=['Comment'])


@web_router.post("/advert/{advert_id}/comment/add")
async def add_comment(ad_id: int, comment_dto: CommentCreate,
                      user: UserExtended = Depends(get_current_user),
                      comment_dao: CommentDao = Depends(get_comment_dao)
                      ):
    comment = comment_dto
    comment.ad_id = ad_id
    comment.created_by = user.id
    await comment_dao.add(comment)


@web_router.get("/advert/{advert_id}/comments")
async def get_all_by_ad_id(ad_id: int,
                           comment_dao: CommentDao = Depends(get_comment_dao)
                           ) -> list[CommentExtended]:
    return await comment_dao.get_all_by_ad_id(ad_id=ad_id)


@web_router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int,
                         user: UserExtended = Depends(get_current_user),
                         comment_dao: CommentDao = Depends(get_comment_dao)):
    current_user = get_current_user()
    if current_user.is_admin:
        return await comment_dao.delete_by_id(comment_id)
