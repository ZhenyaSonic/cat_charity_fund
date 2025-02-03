from typing import Optional

from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def get_oldest_open_project(
            self, session: AsyncSession,
    ) -> Optional[CharityProject]:
        oldest_open_project = await session.execute(
            select(CharityProject).filter(
                CharityProject.fully_invested.is_(False))
            .order_by(asc(CharityProject.create_date))
            .limit(1))
        return oldest_open_project.scalars().first()

    async def get_oldest_open_donation(
            self, session: AsyncSession,
    ) -> Optional[Donation]:
        oldest_open_donation = await session.execute(
            select(Donation).filter(
                Donation.fully_invested.is_(False))
            .order_by(asc(Donation.create_date))
            .limit(1))
        return oldest_open_donation.scalars().first()


charityproject_crud = CRUDCharityProject(CharityProject)
