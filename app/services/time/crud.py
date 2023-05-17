from fastapi import HTTPException

from config.database import AsyncSession

from app.services.utils.utils import pagination

from app.models import Time
from app.schemas.time import TimeCreate
from app.services.quries.times_queries import (
    get_time_list_instance, get_time_by_id, get_time_by_seconds,
    create_time_instance, update_time_instance, delete_time_instance
)


async def get_time_list(
        seconds: int | None,
        page: int,
        page_size: int,
        db: AsyncSession
) -> list[Time]:
    offset = await pagination(page, page_size)
    return await get_time_list_instance(seconds, offset, page_size, db)


async def get_time(
        time_id: int,
        db: AsyncSession
) -> Time:
    time = await get_time_by_id(time_id, db)
    if not time:
        raise HTTPException(status_code=404, detail="Language not found")
    return time


async def create_time(
        time: TimeCreate,
        db: AsyncSession
) -> Time:
    check_time_exists = await get_time_by_seconds(time.seconds, db)
    if check_time_exists:
        raise HTTPException(status_code=400, detail="Language with this name is already exist")
    return await create_time_instance(time, db)


async def update_time(
        time_id: int,
        time: TimeCreate,
        db: AsyncSession
) -> Time:
    check_time_exists = await get_time_by_id(time_id, db)
    if not check_time_exists:
        raise HTTPException(status_code=404, detail="Language not found")
    return await update_time_instance(time_id, time, db)


async def delete_time(
        time_id: int,
        db: AsyncSession
) -> None:
    return await delete_time_instance(time_id, db)
