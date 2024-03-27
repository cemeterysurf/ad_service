from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.models import ComplaintExtended
from backend.database.daos.base_dao import BaseDao
from backend.database.tables import Complaint


class ComplaintDao(BaseDao):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Complaint

    async def get_all_by_ad_id(self,
                               ad_id: int) -> List[ComplaintExtended]:
        query = select(self.model).filter_by(ad_id=ad_id)
        result = await self.session.execute(query)
        return [ComplaintExtended.from_orm(row) for row in result.scalars()]
