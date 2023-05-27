from fastapi import HTTPException

from app.models import Lesson

from config.database import AsyncSession

from app.schemas.lesson import LessonFilters, LessonCreate
from app.services.utils.utils import pagination
from app.services.quries.lessons_quries import (
    get_lessons_list_instance, get_lesson_instance_by_id,
    get_lesson_by_name, create_lesson_instance, update_lesson_instance,
    get_lesson_instance_by_id_simple, delete_lesson_instance
)


async def get_lessons_list(
        filters: LessonFilters,
        page: int,
        page_size: int,
        db: AsyncSession
) -> list[Lesson]:
    offset = await pagination(page, page_size)
    return await get_lessons_list_instance(filters, offset, page_size, db)


async def get_lesson(
        lesson_id: int,
        db: AsyncSession
):
    lesson = await get_lesson_instance_by_id(lesson_id, db)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson with this id does not exist")
    return lesson


async def lesson_create(
        lesson: LessonCreate,
        db: AsyncSession
) -> Lesson:
    check_lesson_exists = await get_lesson_by_name(lesson.name, db)
    if check_lesson_exists:
        raise HTTPException(status_code=400, detail="Lesson with this name is already exist")
    return await create_lesson_instance(lesson, db)


async def lesson_update(
        lesson_id: int,
        lesson: LessonCreate,
        db: AsyncSession
) -> Lesson:
    check_lesson_exists = await get_lesson_instance_by_id_simple(lesson_id, db)
    if not check_lesson_exists:
        raise HTTPException(status_code=404, detail="Lesson with this id does not exist")
    return await update_lesson_instance(lesson_id, lesson, db)


async def lesson_delete(
        lesson_id: int,
        db: AsyncSession
):
    check_lesson_exists = await get_lesson_instance_by_id_simple(lesson_id, db)
    if not check_lesson_exists:
        raise HTTPException(status_code=404, detail="Lesson with this id does not exist")
    return await delete_lesson_instance(lesson_id, db)
