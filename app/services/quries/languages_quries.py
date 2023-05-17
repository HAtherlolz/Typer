from sqlalchemy import select, update

from app.models import Language
from config.database import AsyncSession
from app.schemas.language import LanguageCreate


async def get_lang_by_name(name: str, db: AsyncSession) -> Language | None:
    language = await db.execute(
        select(Language).where(Language.name == name)
    )
    return language.scalar_one_or_none()


async def get_lang_list_instance(
        name: str | None,
        offset: int,
        page_size: int,
        db: AsyncSession
) -> list[Language]:
    languages = select(Language).offset(offset).limit(page_size)
    if name:
        languages = languages.where(Language.name == name)
    res = await db.execute(languages)
    return res.scalars().all()


async def get_lang_by_id(lang_id: int, db: AsyncSession) -> Language | None:
    language = await db.execute(
        select(Language).where(Language.id == lang_id)
    )
    return language.scalar_one_or_none()


async def create_lang_instance(
        lang: LanguageCreate,
        db: AsyncSession
) -> Language:
    new_lang = Language(**lang.dict())
    db.add(new_lang)
    await db.commit()
    await db.refresh(new_lang)
    return new_lang


async def update_lang_instance(
        lang_id: int,
        lang: LanguageCreate,
        db: AsyncSession
) -> Language:
    updated_lang = await db.execute(
        update(Language).where(Language.id == lang_id).values(**lang.dict()).returning(Language)
    )
    await db.commit()
    return updated_lang.scalar_one()


async def delete_lang_instance(
        lang_id: int,
        db: AsyncSession
) -> None:
    await db.delete(
        select(Language).where(Language.id == lang_id)
    )
    await db.commit()

