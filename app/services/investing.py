from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud


async def invest_funds(
    source,
    target_getter,
    session: AsyncSession,
):
    """
    Общая логика распределения средств между источником и целями.
    """
    remaining_funds = source.full_amount - source.invested_amount
    invested_amount = 0

    while remaining_funds > 0:
        target = await target_getter(session)
        if target is None:
            break

        needed_funds = target.full_amount - target.invested_amount

        if needed_funds <= remaining_funds:
            target.invested_amount += needed_funds
            invested_amount += needed_funds
            remaining_funds -= needed_funds

            target.fully_invested = True
            target.close_date = datetime.now()
        else:
            target.invested_amount += remaining_funds
            invested_amount += remaining_funds
            remaining_funds = 0

    source.invested_amount += invested_amount
    if remaining_funds == 0:
        source.fully_invested = True
        source.close_date = datetime.now()

    return source


async def distribute_new_donation(
    donation,
    session: AsyncSession,
):
    """
    Распределяет новую пожертвованную сумму (donation) на открытые проекты.
    """
    return await invest_funds(
        source=donation,
        target_getter=charity_project_crud.get_oldest_open_project,
        session=session,
    )


async def allocate_to_new_project(
    project,
    session: AsyncSession,
):
    """
    Распределяет доступные пожертвования на новый проект.
    """
    return await invest_funds(
        source=project,
        target_getter=charity_project_crud.get_oldest_open_donation,
        session=session,
    )