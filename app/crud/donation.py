from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import User, Donation


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            session: AsyncSession,
            user: User
    ):
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id, ))
        return reservations.scalars().all()


donation_crud = CRUDDonation(Donation)
