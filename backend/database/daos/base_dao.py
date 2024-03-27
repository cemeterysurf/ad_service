from typing import TypeVar, Optional, Any, List

from sqlalchemy import delete, update, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.base_table import Base

AnyModel = TypeVar('AnyModel')


class BaseDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Base

    async def add(self, entity: AnyModel) -> None:
        self.session.add(entity)
        await self.session.flush()

    async def get_all(self) -> List[AnyModel]:
        result = await self.session.execute(
            select(self.model).order_by(self.model.id))
        return result.scalars().all()

    async def filter(self, **kwargs) -> List[AnyModel]:
        result = await self.session.execute(
            select(self.model).filter_by(**kwargs))
        return result.scalars().all()

    async def filter_by_param(self, where: Any) -> List[AnyModel]:
        result = await self.session.execute(select(self.model).where(where))
        return result.scalars().all()

    async def get_one_by_id(self, id_) -> Optional[AnyModel]:
        result = await self.session.execute(
            select(self.model).filter_by(id=id_))
        return result.scalars().one_or_none()

    async def get_all_by_ids(self, ids: List[int]) -> List[AnyModel]:
        result = await self.session.execute(
            select(self.model).where(self.model.id.in_(ids)))
        return result.scalars().all()

    async def get_one_by_params(self, **kwargs) -> Optional[AnyModel]:
        result = await self.session.execute(
            select(self.model).filter_by(**kwargs))
        return result.scalars().one_or_none()

    async def update(self, id_, **kwargs) -> None:
        query = update(self.model).where(self.model.id == id_).values(**kwargs)
        query.execution_options(synchronize_session="fetch")
        await self.session.execute(query)

    async def update_by_param(self, where: Any, **kwargs) -> None:
        query = update(self.model).where(where).values(**kwargs)
        query.execution_options(synchronize_session="fetch")
        await self.session.execute(query)

    async def insert_or_update(self, constraint_name, **kwargs) -> None:
        query = insert(self.model).values(**kwargs).on_conflict_do_update(
            constraint=constraint_name,
            set_=kwargs
        )
        query.execution_options(synchronize_session="fetch")
        await self.session.execute(query)

    async def delete(self, entity: AnyModel) -> None:
        await self.session.delete(entity)

    async def delete_by_id(self, id_) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == id_))

    async def delete_by_params(self, where: Any) -> None:
        await self.session.execute(delete(self.model).where(where))

    async def delete_by_params(self, where: Any) -> None:
        await self.session.execute(delete(self.model).where(where))
