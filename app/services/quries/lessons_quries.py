from app.models import Lesson, Profile

from config.database import AsyncSession

from app.schemas.lesson import LessonFilters, LessonCreate
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload


async def get_lesson_by_name(
        name: str,
        db: AsyncSession
) -> Lesson | None:
    lesson = await db.execute(
        select(Lesson).where(Lesson.name == name)
    )
    return lesson.scalar_one_or_none()


async def get_lessons_list_instance(
        filters: LessonFilters,
        offset: int,
        page_size: int,
        db: AsyncSession
) -> list[Lesson]:
    lessons = select(Lesson).options(
        selectinload(Lesson.lesson_profiles)
    ).offset(offset).limit(page_size)
    if filters.name:
        lessons = lessons.where(Lesson.name == filters.name)
    if filters.wpm:
        lessons = lessons.where(Lesson.wpm == filters.wpm)
    if filters.cpm:
        lessons = lessons.where(Lesson.cpm == filters.cpm)
    if filters.row_wpm:
        lessons = lessons.where(Lesson.row_wpm == filters.row_wpm)
    if filters.accuracy:
        lessons = lessons.where(Lesson.accuracy == filters.accuracy)
    if filters.consistency:
        lessons = lessons.where(Lesson.consistency == filters.consistency)
    if filters.profile_id:
        lessons = lessons.join(Lesson.lesson_profiles).where(Profile.id == filters.profile_id)
    if filters.language_id:
        lessons = lessons.where(Lesson.language_id == filters.language_id)

    res = await db.execute(lessons)
    return res.scalars().all()


async def get_lesson_instance_by_id(
        lesson_id: int,
        db: AsyncSession
) -> Lesson | None:
    lesson = await db.execute(
        select(Lesson).options(
            selectinload(Lesson.lesson_profiles),
            selectinload(Lesson.language)
        )
    ).where(Lesson.id == lesson_id)
    return lesson.scalar_one_or_none()


async def get_lesson_instance_by_id_simple(
        lesson_id: int,
        db: AsyncSession
) -> Lesson | None:
    lesson = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    return lesson.scalar_one_or_none()


async def create_lesson_instance(
        lesson: LessonCreate,
        db: AsyncSession
) -> Lesson:
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    return await get_lesson_instance_by_id(new_lesson.id, db)


async def update_lesson_instance(
        lesson_id: int,
        lesson: LessonCreate,
        db: AsyncSession
) -> Lesson:
    updated_lesson = await db.execute(
        update(Lesson).where(Lesson.id == lesson_id).values(
            **lesson.dict(exclude_none=True)
        ).returning(Lesson).options(
            selectinload(Lesson.language)
        )
    )
    await db.commit()
    updated_lesson = updated_lesson.scalar_one()
    await db.refresh(updated_lesson)
    return updated_lesson


async def delete_lesson_instance(
        lesson_id: int,
        db: AsyncSession
) -> None:
    lesson = await db.get(Lesson, lesson_id)
    await db.delete(lesson)
    await db.commit()



