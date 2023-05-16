from datetime import datetime

from config.database import AsyncSession

from app.schemas.profile import EmailStr, ProfileCreate, ProfileRetrieve

from app.models.profile import Profile
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
        email: EmailStr | None,
        nickname: str | None,
        date_join: datetime | None,
        is_active: bool | None,
        is_admin: bool | None,

        offset: int,
        page_size: int,

        db: AsyncSession
) -> list[Profile]:
    profiles = select(Profile).offset(offset).limit(page_size)
    if email:
        profiles = profiles.where(Profile.email == email)
    if nickname:
        profiles = profiles.where(Profile.nickname == nickname)
    if date_join:
        profiles = profiles.where(Profile.date_joined == date_join)
    if is_active:
        profiles = profiles.where(Profile.is_active == is_active)
    if is_admin:
        profiles = profiles.where(Profile.is_admin == is_admin)

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


async def delete_profile_instance(
        current_user: ProfileRetrieve,
        db: AsyncSession
) -> None:
    await db.delete(current_user)
    await db.commit()
