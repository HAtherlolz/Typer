from fastapi import HTTPException

from config.database import AsyncSession

from app.services.utils.utils import pagination

from app.models import Language
from app.schemas.language import LanguageCreate
from app.services.quries.languages_quries import (
    get_lang_list_instance, get_lang_by_id, get_lang_by_name,
    create_lang_instance, update_lang_instance, delete_lang_instance
)


async def get_lang_list(
        name: str | None,
        page: int,
        page_size: int,
        db: AsyncSession
) -> list[Language]:
    offset = await pagination(page, page_size)
    return await get_lang_list_instance(name, offset, page_size, db)


async def get_lang(
        lang_id: int,
        db: AsyncSession
) -> Language:
    lang = await get_lang_by_id(lang_id, db)
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    return lang


async def create_lang(
        lang: LanguageCreate,
        db: AsyncSession
) -> Language:
    check_lang_exists = await get_lang_by_name(lang.name, db)
    if check_lang_exists:
        raise HTTPException(status_code=400, detail="Language with this name is already exist")
    return await create_lang_instance(lang, db)


async def update_lang(
        lang_id: int,
        lang: LanguageCreate,
        db: AsyncSession
) -> Language:
    check_lang_exists = await get_lang_by_id(lang_id, db)
    if not check_lang_exists:
        raise HTTPException(status_code=404, detail="Language not found")
    return await update_lang_instance(lang_id, lang, db)


async def delete_lang(
        lang_id: int,
        db: AsyncSession
) -> None:
    return await delete_lang_instance(lang_id, db)
