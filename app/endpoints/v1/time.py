from fastapi import APIRouter, Depends

from app.schemas.time import TimeRetrieve, TimeCreate

from config.database import AsyncSession, get_session

from app.services.profile.jwt import admin_permission
from app.schemas.profile import ProfileRetrieve

from app.services.time.crud import get_time_list, get_time, create_time, update_time, delete_time


time_router = APIRouter()


@time_router.get("/times/", response_model=list[TimeRetrieve])
async def time_list(
        name: str | None = None,

        page: int = 1,
        page_size: int = 10,

        db: AsyncSession = Depends(get_session)
):
    return await get_time_list(name, page, page_size, db)


@time_router.get("/time/{time_id}/", response_model=TimeRetrieve)
async def time_retrieve(
        time_id: int,
        db: AsyncSession = Depends(get_session)
):
    return await get_time(time_id, db)


@time_router.post("/time/create}/", response_model=TimeRetrieve)
async def time_create(
        time: TimeCreate,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await create_time(time, db)


@time_router.patch("/time/{time_id}/update/", response_model=TimeRetrieve)
async def time_update(
        time_id: int,
        time: TimeCreate,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await update_time(time_id, time, db)


@time_router.delete("/time/{lang_id}/delete/", status_code=204)
async def time_delete(
        lang_id: int,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await delete_time(lang_id, db)
