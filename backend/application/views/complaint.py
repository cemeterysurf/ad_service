from fastapi import APIRouter, Depends

from backend.application.models import (
    ComplaintCreate, ComplaintExtended, UserExtended
)
from backend.application.views.auth import get_current_user
from backend.application.views.dependencies import (
    get_complaint_dao
)
from backend.database.daos import ComplaintDao

web_router = APIRouter(tags=['Complaint'])


@web_router.post("/advert/{advert_id}/complaint/add")
async def add_complaint(ad_id: int, complaint_dto: ComplaintCreate,
                        user: UserExtended = Depends(get_current_user),
                        complaint_dao: ComplaintDao = Depends(get_complaint_dao)
                        ):
    complaint = complaint_dto
    complaint.ad_id = ad_id
    complaint.created_by = user.id
    await complaint_dao.add(complaint)


@web_router.get("/advert/{advert_id}/complaints")
async def get_all_by_ad_id(ad_id: int,
                           complaint_dao: ComplaintDao = Depends(
                               get_complaint_dao)
                           ) -> list[ComplaintExtended]:
    return await complaint_dao.get_all_by_ad_id(ad_id=ad_id)


@web_router.delete("/complaint/{complaint_id}")
async def delete(complaint_id: int,
                 user: UserExtended = Depends(get_current_user),
                 complaint_dao: ComplaintDao = Depends(get_complaint_dao)):
    current_user = get_current_user()
    if current_user.is_admin:
        return await complaint_dao.delete_by_id(complaint_id)
