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
    Убедитесь, что проект с таким именем отсутствует в базе данных.
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
    Убедитесь, что проект с указанным ID существует.
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
    Убедитесь, что новая сумма не меньше уже вложенной.
    """
    charityproject = await charity_project_crud.get(charityproject_id, session)
    if full_amount < charityproject.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Требуемая сумма не может быть меньше уже внесённой!'
        )


def check_close_project(project):
    """
    Убедитесь, что проект не закрыт.
    Закрытые проекты нельзя редактировать или удалять.
    """
    if project.fully_invested is True:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя редактировать или удалять закрытый проект!'
        )


def check_project_invested_amount(project):
    """
    Убедитесь, что в проект не были внесены средства.
    Проекты с вложениями нельзя удалять.
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя удалять проект, в который внесены средства!'
        )


def check_project_before_edit(project):
    """
    Убедитесь, что параметры проекта можно редактировать.
    Запрещено изменять сумму инвестиций, дату создания,
    дату закрытия и статус инвестирования.
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
            detail='Нельзя изменять статус инвестирования!'
        )
