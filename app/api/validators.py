from http import HTTPStatus
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """
    Проверяет, существует ли проект с таким же именем в базе данных.
    """
    project_id = await charity_project_crud.get_project_by_name(
        project_name,
        session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charityproject_exists(
        charityproject_id: int, session: AsyncSession, ) -> CharityProject:
    """
    Проверяет, существует ли проект с указанным ID.
    """
    charityproject = await charity_project_crud.get(charityproject_id, session)
    if charityproject is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charityproject


async def check_full_amount(
        full_amount: int,
        charityproject_id: int,
        session: AsyncSession,
) -> None:
    """
    Проверяет, что новая сумма не меньше уже вложенной суммы.
    """
    charityproject = await charity_project_crud.get(charityproject_id, session)
    if full_amount < charityproject.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Требуемая сумма не может быть меньше уже внесённой!'
        )


def check_close_project(project):
    """
    Проверяет, закрыт ли проект.
    Закрытые проекты нельзя редактировать или удалять.
    """
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать или удалять закрытый проект!'
        )


def check_project_invested_amount(project):
    """
    Проверяет, были ли внесены средства в проект.
    Проекты с вложениями нельзя удалять.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалять проект в который внесены средства!'
        )


def check_project_before_edit(project):
    """
    Проверяет, можно ли редактировать проект.
    Запрещает изменение суммы инвестиций,
    даты создания, даты закрытия и статуса инвестирования.
    """
    if project.invested_amount is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя изменять сумму инвестиций!'
        )
    if project.create_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя изменять дату создания!'
        )
    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя изменять дату закрытия!'
        )
    if project.fully_invested is not None:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя изменять сумму инвестирования!'
        )
