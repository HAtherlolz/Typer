from fastapi import APIRouter, Depends

from app.schemas.language import LanguageRetrieve, LanguageCreate

from config.database import AsyncSession, get_session

from app.services.profile.jwt import admin_permission
from app.schemas.profile import ProfileRetrieve

from app.services.language.crud import get_lang_list, get_lang, create_lang, update_lang, delete_lang


lang_router = APIRouter()


@lang_router.get("/languages/", response_model=list[LanguageRetrieve])
async def lang_list(
        name: str | None = None,

        page: int = 1,
        page_size: int = 10,

        db: AsyncSession = Depends(get_session)
):
    return await get_lang_list(name, page, page_size, db)


@lang_router.get("/language/{lang_id}/", response_model=LanguageRetrieve)
async def lang_retrieve(
        lang_id: int,
        db: AsyncSession = Depends(get_session)
):
    return await get_lang(lang_id, db)


@lang_router.post("/language/create}/", response_model=LanguageRetrieve)
async def lang_create(
        lang: LanguageCreate,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await create_lang(lang, db)


@lang_router.patch("/language/{lang_id}/update/", response_model=LanguageRetrieve)
async def lang_update(
        lang_id: int,
        lang: LanguageCreate,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await update_lang(lang_id, lang, db)


@lang_router.delete("/language/{lang_id}/delete/", status_code=204)
async def lang_delete(
        lang_id: int,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await delete_lang(lang_id, db)
