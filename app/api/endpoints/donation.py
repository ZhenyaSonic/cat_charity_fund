from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationDBSuperuser,
)
from app.services.investing import distribute_resources


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    new_donation = await donation_crud.create(donation, session, user)

    await distribute_resources(
        source=new_donation,
        target_model=CharityProject,
        session=session)

    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={'user_id'}
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await donation_crud.get_by_user(user=user, session=session)


@router.get('/',
            response_model=list[DonationDBSuperuser],
            dependencies=[Depends(current_superuser)], )
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)):
    return await donation_crud.get_multi(session)
