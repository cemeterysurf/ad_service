from fastapi import APIRouter, Depends

from backend.application.models import (
    AdAdd, AdExtended, UserExtended, AdFilter, Pagination, AdType
)
from backend.application.views.auth import get_current_user
from backend.application.views.dependencies import (
    get_ad_dao
)
from backend.database.daos import AdDao

web_router = APIRouter(tags=['Ad'])


@web_router.post("/add")
async def add_ad(
        ad_dto: AdAdd,
        ad_dao: AdDao = Depends(get_ad_dao),
):
    await ad_dao.add(ad_dto)


@web_router.get("/all")
async def get_all_ads(
        desc_sorting: bool,
        pagination: Pagination = Depends(),
        ad_filter: AdFilter = Depends(),
        ad_dao: AdDao = Depends(get_ad_dao)
) -> list[AdExtended]:
    return await ad_dao.get_all_filtered(
        filters=ad_filter,
        desc_sorting=desc_sorting,
        pagination=pagination,
    )


@web_router.get("/{advert_id}")
async def get_ad_by_id(
        ad_id: int, ad_dao: AdDao = Depends(get_ad_dao)
) -> AdExtended:
    return await ad_dao.get_one_by_id(ad_id)


@web_router.delete("/{advert_id}")
async def delete_advert(
        ad_id: int,
        user: UserExtended = Depends(get_current_user),
        ad_dao: AdDao = Depends(get_ad_dao)
):
    ad = await ad_dao.get_one_by_id(ad_id)
    if ad.user_id == user.id:
        await ad_dao.delete(ad_id)


@web_router.patch("/{advert_id}")
async def update_ad_type(
        ad_id: int,
        ad_type: AdType,
        user: UserExtended = Depends(get_current_user),
        ad_dao: AdDao = Depends(get_ad_dao)
) -> AdExtended:
    ad = await ad_dao.get_one_by_id(ad_id)
    if ad.user_id == user.id:
        ad.type = ad_type
    return ad
