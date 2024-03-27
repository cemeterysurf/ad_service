from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.application.models import AdExtended, Pagination, AdFilter
from backend.database.daos.base_dao import BaseDao
from backend.database.tables import Ad


class AdDao(BaseDao):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Ad

    async def get_all_filtered(self,
                               pagination: Pagination,
                               desc_sorting: bool,
                               filters: AdFilter) -> List[AdExtended]:
        order_by = (
            self.model.created_at.desc() if desc_sorting
            else self.model.created_at
        )

        query = select(self.model).options(joinedload(Ad.creator))

        if filters.title:
            query = query.filter(self.model.title.ilike(f'%{filters.title}%'))
        if filters.body:
            query = query.filter(self.model.body.ilike(f'%{filters.body}%'))
        if filters.type is not None:
            query = query.filter(self.model.type == filters.type)
        if filters.user_id is not None:
            query = query.filter(
                self.model.user_id == filters.user_id)

        query = (query.order_by(order_by).limit(
            pagination.per_page).offset(
            (pagination.page - 1) * pagination.per_page))

        result = await self.session.execute(query)

        return [AdExtended.from_orm(row) for row in result.scalars()]
