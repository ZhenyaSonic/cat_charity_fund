from datetime import datetime
from typing import Awaitable, Callable, Type

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud


async def invest_funds(
    source,
    target_getter: Callable[[AsyncSession], Awaitable],
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

        session.add(target)

    source.invested_amount += invested_amount
    if remaining_funds == 0:
        source.fully_invested = True
        source.close_date = datetime.now()

    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source


async def distribute_resources(
    source,
    target_model: Type,
    session: AsyncSession,
):
    """
    Универсальная функция для распределения средств.
    :param source: Источник средств (пожертвование или проект).
    :param target_model: Модель цели распределения
    (CharityProject или Donation).
    :param session: Асинхронная сессия SQLAlchemy.
    """
    target_getter = (
        lambda session:
        charity_project_crud
        .get_oldest_open_item(session, target_model))
    return await invest_funds(
        source=source,
        target_getter=target_getter,
        session=session,
    )
