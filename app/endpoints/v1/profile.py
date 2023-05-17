from fastapi import APIRouter, Depends, BackgroundTasks, File, UploadFile, Form

from datetime import datetime

from config.database import get_session, AsyncSession

from app.schemas.profile import EmailStr, ProfileCreate, ProfileRetrieve, AccessToken, JwtSchema, ProfileLogin, \
    ProfileEmail, NewPassword
from app.services.profile.jwt import get_current_user
from app.services.profile.crud import (
    get_profile_list, get_profile_retrieve, create_profile,
    confirm_profile, delete_profile, get_profiles_jwt,
    send_reset_password, password_reset, update_profile
)


profile_router = APIRouter()


@profile_router.get("/profiles/", response_model=list[ProfileRetrieve])
async def profile_list(
        email: EmailStr | None = None,
        nickname: str | None = None,
        date_join: datetime | None = None,
        is_active: bool | None = None,
        is_admin: bool | None = None,

        page: int = 1,
        page_size: int = 10,

        db: AsyncSession = Depends(get_session)
):
    return await get_profile_list(email, nickname, date_join, is_active, is_admin, page, page_size, db)


@profile_router.get("/profile/{profile_id}/", response_model=ProfileRetrieve)
async def profile_retrieve(
        profile_id: int,
        db: AsyncSession = Depends(get_session)
):
    return await get_profile_retrieve(profile_id, db)


@profile_router.post("/profile/create/", response_model=ProfileRetrieve)
async def profile_create(
        profile: ProfileCreate,
        background_tasks: BackgroundTasks,
        db: AsyncSession = Depends(get_session)
):
    return await create_profile(profile, background_tasks, db)


@profile_router.post("/profile/confirmation/", response_model=ProfileRetrieve)
async def profile_confirm(
        token: AccessToken,
        db: AsyncSession = Depends(get_session)
):
    return await confirm_profile(token, db)


@profile_router.post("/profile/tokens/", response_model=JwtSchema)
async def profile_tokens(
        profile: ProfileLogin,
        db: AsyncSession = Depends(get_session)
):
    return await get_profiles_jwt(profile, db)


@profile_router.get("/me/", response_model=ProfileRetrieve, status_code=200)
async def me(profile: ProfileRetrieve = Depends(get_current_user)):
    return profile


@profile_router.patch("/profile/update/", response_model=ProfileRetrieve, status_code=201)
async def profile_update(
        avatar: UploadFile = File(default=None),
        nickname: str = Form(default=None, max_length=15, min_length=3),
        current_user: ProfileRetrieve = Depends(get_current_user),
        db: AsyncSession = Depends(get_session)
):
    return await update_profile(avatar, nickname, current_user, db)


@profile_router.delete("/profile/delete/", status_code=204)
async def profile_delete(
        current_user: ProfileRetrieve = Depends(get_current_user),
        db: AsyncSession = Depends(get_session)
):
    return await delete_profile(current_user, db)


@profile_router.post("/profile/send-reset-email/")
async def send_reset_password_email(
        background_tasks: BackgroundTasks,
        email: ProfileEmail,
        db: AsyncSession = Depends(get_session)
):
    return await send_reset_password(background_tasks, email, db)


@profile_router.post("/profile/new-password/", response_model=ProfileRetrieve)
async def profile_change_password(
    passwords: NewPassword,
    db: AsyncSession = Depends(get_session)
):
    return await password_reset(passwords, db)
