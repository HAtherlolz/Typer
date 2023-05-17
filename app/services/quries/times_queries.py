from sqlalchemy import select, update

from app.models import Time
from config.database import AsyncSession
from app.schemas.time import TimeCreate


async def get_time_by_seconds(seconds: int, db: AsyncSession) -> Time | None:
    time = await db.execute(
        select(Time).where(Time.seconds == seconds)
    )
    return time.scalar_one_or_none()


async def get_time_list_instance(
        seconds: int | None,
        offset: int,
        page_size: int,
        db: AsyncSession
) -> list[Time]:
    times = select(Time).offset(offset).limit(page_size)
    if seconds:
        times = times.where(Time.seconds == seconds)
    res = await db.execute(times)
    return res.scalars().all()


async def get_time_by_id(time_id: int, db: AsyncSession) -> Time | None:
    language = await db.execute(
        select(Time).where(Time.id == time_id)
    )
    return language.scalar_one_or_none()


async def create_time_instance(
        time: TimeCreate,
        db: AsyncSession
) -> Time:
    new_time = Time(**time.dict())
    db.add(new_time)
    await db.commit()
    await db.refresh(new_time)
    return new_time


async def update_time_instance(
        time_id: int,
        time: TimeCreate,
        db: AsyncSession
) -> Time:
    updated_time = await db.execute(
        update(Time).where(Time.id == time_id).values(**time.dict()).returning(Time)
    )
    await db.commit()
    return updated_time.scalar_one()


async def delete_time_instance(
        time_id: int,
        db: AsyncSession
) -> None:
    training = await db.get(Time, time_id)
    await db.delete(training)
    await db.commit()

