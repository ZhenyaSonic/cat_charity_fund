from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charityproject_exists,
    check_close_project,
    check_full_amount,
    check_name_duplicate,
    check_project_before_edit,
    check_project_invested_amount,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import distribute_resources


router = APIRouter()


@router.post('/',
             response_model=CharityProjectDB,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],
             summary="Создать новый благотворительный проект"
             )
async def create_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)

    invest_project = await distribute_resources(
        source=new_project,
        target_model=Donation,
        session=session)
    return invest_project


@router.get('/',
            response_model=list[CharityProjectDB],
            response_model_exclude_none=True,
            summary="Получить список всех благотворительных проектов"
            )
async def get_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Частично обновить благотворительный проект"
)
async def partially_update_charityproject(
        charityproject_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session), ):
    project = await check_charityproject_exists(
        charityproject_id, session)
    check_project_before_edit(obj_in)
    check_close_project(project)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_full_amount(obj_in.full_amount, charityproject_id, session)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{charityproject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
    summary="Удалить благотворительный проект"
)
async def remove_charityproject(
        charityproject_id: int,
        session: AsyncSession = Depends(get_async_session), ):
    project = await check_charityproject_exists(
        charityproject_id, session
    )
    project = await charity_project_crud.remove(project, session)
    check_close_project(project)
    check_project_invested_amount(project)
    return project
