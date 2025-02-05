from typing import Type, Optional

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from app.crud.base import CRUDBase
from app.models import CharityProject, Donation


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
            model: Type[DeclarativeMeta]
    ) -> Optional[DeclarativeMeta]:
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

    async def get_oldest_open_project(
            self, session: AsyncSession
    ) -> Optional[CharityProject]:
        return await self.get_oldest_open_item(session, CharityProject)

    async def get_oldest_open_donation(
            self, session: AsyncSession
    ) -> Optional[Donation]:
        return await self.get_oldest_open_item(session, Donation)


charity_project_crud = CRUDCharityProject(CharityProject)
