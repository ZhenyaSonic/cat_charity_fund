from typing import Type, Optional

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.models.base import BaseModel


class CRUDCharityProject(CRUDBase):

    async def get_project_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_oldest_open_item(
            self,
            session: AsyncSession,
            model: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """
        Универсальная функция для получения самой старой открытой записи
        из указанной модели.
        """
        oldest_open_item = await session.execute(
            select(model).filter(
                model.fully_invested.is_(False)
            ).order_by(asc(model.create_date)).limit(1)
        )
        return oldest_open_item.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
