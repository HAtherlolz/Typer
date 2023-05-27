from datetime import datetime

from fastapi import APIRouter, Depends

from config.database import AsyncSession, get_session

from app.schemas.lesson import (
    LessonRetrieve, LessonFilters, LessonWithProfile,
    LessonCreate
)
from app.services.lesson.crud import (
    get_lessons_list, get_lesson, lesson_create,
    lesson_update, lesson_delete
)


lesson_router = APIRouter()


@lesson_router.get("/lessons/", response_model=list[LessonRetrieve])
async def get_list(
        name: str | None = None,
        wpm: float | None = None,
        cpm: float | None = None,
        row_wpm: float | None = None,
        accuracy: int | None = None,
        consistency: int | None = None,
        date_time: datetime | None = None,
        profile_id: int | None = None,
        language_id: int | None = None,

        page: int = 1,
        page_size: int = 10,

        db: AsyncSession = Depends(get_session)
):
    filters = LessonFilters(
        wpm=wpm, cpm=cpm, row_wpm=row_wpm, accuracy=accuracy,
        consistency=consistency, date_time=date_time, profile_id=profile_id,
        language_id=language_id, name=name
    )
    return await get_lessons_list(filters, page, page_size, db)


@lesson_router.get("/lesson/{lesson_id}/", response_model=LessonWithProfile)
async def get_retrieve(
        lesson_id: int,
        db: AsyncSession = Depends(get_session)
):
    return await get_lesson(lesson_id, db)


@lesson_router.post("/lesson/create/", response_model=LessonRetrieve)
async def create_lesson(
        lesson: LessonCreate,
        db: AsyncSession = Depends(get_session)
        # TODO: Permissions Admin
):
    return await lesson_create(lesson, db)


@lesson_router.patch("/lesson/{lesson_id}/update/", response_model=LessonRetrieve)
async def update_lesson(
        lesson_id: int,
        lesson: LessonCreate,
        db: AsyncSession = Depends(get_session)
        # TODO: Permissions Admin, CHECK SCHEMA
):
    return await lesson_update(lesson_id, lesson, db)


@lesson_router.delete("/lesson/{lesson_id}/delete/", status_code=204)
async def delete_lesson(
        lesson_id: int,
        db: AsyncSession = Depends(get_session)
        # TODO: Permissions Admin
):
    return await lesson_delete(lesson_id, db)
