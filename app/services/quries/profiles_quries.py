from datetime import datetime

from sqlalchemy.orm import selectinload

from config.database import AsyncSession

from app.schemas.profile import ProfileFilters, ProfileCreate, ProfileRetrieve, ProfileUpdate

from app.models.profile import Profile
from app.models.lesson import Lesson
from app.models.training import Training

from sqlalchemy import select, update


async def check_profile_with_email_exists(
        email: str,
        db: AsyncSession
) -> Profile | None:
    profile = await db.execute(
        select(Profile).where(Profile.email == email)
    )
    return profile.scalar_one_or_none()


async def get_profile_by_email_password(
        email: str,
        password: str,
        db: AsyncSession
) -> Profile | None:
    profile = await db.execute(
        select(Profile).where(Profile.email == email)
    )
    return profile.scalar_one_or_none()


async def get_profile_list_instances(
        filters: ProfileFilters,

        offset: int,
        page_size: int,

        db: AsyncSession
) -> list[Profile]:
    profiles = select(Profile).options(
        selectinload(Profile.profile_lessons), selectinload(Profile.profile_trainings)
    ).offset(offset).limit(page_size)
    if filters.email:
        profiles = profiles.where(Profile.email.startswith(filters.email))
    if filters.nickname:
        profiles = profiles.where(Profile.nickname.startswith(filters.nickname))
    if filters.date_join:
        profiles = profiles.where(Profile.date_joined == filters.date_join)
    if filters.is_active:
        profiles = profiles.where(Profile.is_active == filters.is_active)
    if filters.is_admin:
        profiles = profiles.where(Profile.is_admin == filters.is_admin)
    if filters.lessons:
        profiles = profiles.join(Profile.profile_lessons).where(Lesson.name.startswith(filters.lessons))
    if filters.trainings:
        profiles = profiles.join(Profile.profile_trainings).where(Training.name.startswith(filters.trainings))

    res = await db.execute(profiles.distinct())
    return res.scalars().all()


async def get_profile_instance_by_id(profile_id: int, db: AsyncSession) -> Profile | None:
    profile = await db.execute(
        select(Profile).where(Profile.id == profile_id)
    )
    return profile.scalar_one_or_none()


async def create_profile_instance(
        profile: ProfileCreate,
        db: AsyncSession
) -> Profile:
    new_profile = Profile(**profile.dict())
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


async def update_profile_instance_is_active(
        profile_id: int,
        db: AsyncSession
) -> Profile:
    profile = await db.execute(
        update(Profile).where(Profile.id == profile_id).values(is_active=True).returning(Profile)
    )
    await db.commit()
    return profile.scalar_one()


async def update_profile_password(
        profile_id: int,
        hashed_password: str,
        db: AsyncSession
) -> Profile:
    update_pass = await db.execute(
        update(Profile).where(Profile.id == profile_id).values(password=hashed_password).returning(Profile)
    )
    await db.commit()
    return update_pass.scalar_one()


async def update_profile_instance(
        profile: ProfileUpdate,
        current_user: ProfileRetrieve,
        db: AsyncSession
) -> Profile:
    updated_profile = await db.execute(
        update(Profile).where(
            Profile.id == current_user.id
        ).values(**profile.dict(exclude_none=True)).returning(Profile)
    )
    await db.commit()
    return updated_profile.scalar_one()


async def delete_profile_instance(
        current_user: ProfileRetrieve,
        db: AsyncSession
) -> None:
    await db.delete(current_user)
    await db.commit()
