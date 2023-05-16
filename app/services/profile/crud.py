from datetime import datetime

from fastapi import HTTPException, BackgroundTasks, status

from config.database import AsyncSession

from app.schemas.profile import EmailStr, ProfileCreate, AccessToken, ProfileRetrieve, ProfileLogin, ProfileEmail, \
    NewPassword

from app.models.profile import Profile

from app.services.utils.utils import pagination
from app.services.profile.jwt import get_password_hash, create_tokens, get_current_user_by_refresh_token, \
    authenticate_user, get_current_user
from app.services.quries.profiles_quries import (
    get_profile_list_instances, get_profile_instance_by_id,
    check_profile_with_email_exists, create_profile_instance,
    update_profile_instance_is_active, delete_profile_instance, update_profile_password
)
from app.services.profile.profile import send_register_email, send_password_email


async def get_profile_list(
        email: EmailStr | None,
        nickname: str | None,
        date_join: datetime | None,
        is_active: bool | None,
        is_admin: bool | None,

        page: int,
        page_size: int,

        db: AsyncSession
) -> list[Profile]:
    offset = await pagination(page, page_size)
    return await get_profile_list_instances(email, nickname, date_join, is_active, is_admin, offset, page_size, db)


async def get_profile_retrieve(profile_id: int, db: AsyncSession) -> Profile:
    profile = await get_profile_instance_by_id(profile_id, db)
    if not profile:
        raise HTTPException(status_code=400, detail="Profile with this id does not exist")
    return profile


async def create_profile(
        profile: ProfileCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession
) -> Profile:
    check_profile_exists = await check_profile_with_email_exists(profile.email, db)
    if check_profile_exists:
        raise HTTPException(status_code=400, detail="Profile with this email is already exist")
    profile.password = get_password_hash(profile.password)
    created_profile = await create_profile_instance(profile, db)
    tokens = await create_tokens(created_profile)
    background_tasks.add_task(send_register_email, created_profile.email, tokens.access_token)
    return created_profile


async def confirm_profile(
        token: AccessToken,
        db: AsyncSession
) -> Profile:
    profile = await get_current_user_by_refresh_token(token.access_token, db)
    return await update_profile_instance_is_active(profile.id, db)


async def get_profiles_jwt(
        profile: ProfileLogin,
        db: AsyncSession
):
    profile = await authenticate_user(profile.email, profile.password, db)
    if isinstance(profile, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=profile,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await create_tokens(profile)


async def delete_profile(
        current_user: ProfileRetrieve,
        db: AsyncSession
) -> None:
    return await delete_profile_instance(current_user, db)


async def send_reset_password(
        background_tasks: BackgroundTasks,
        email: ProfileEmail,
        db: AsyncSession
) -> HTTPException | dict:
    profile_check = await check_profile_with_email_exists(email.email, db)
    if not profile_check:
        raise HTTPException(status_code=400, detail="Profile with this email is already exist")
    access_token, _ = create_tokens(profile_check)
    background_tasks.add_task(send_password_email, email.email, access_token)
    return {"message": "The email for with link to reset password successfully send"}


async def password_reset(
        passwords: NewPassword,
        db: AsyncSession
) -> Profile | HTTPException:
    if passwords.password != passwords.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The passwords are different"
        )
    profile = await get_current_user(passwords.token)
    if isinstance(profile, bool):
        raise HTTPException(status_code=400, detail="Invalid token")
    hashed_password = get_password_hash(profile.password)
    return await update_profile_password(profile.id, hashed_password, db)
