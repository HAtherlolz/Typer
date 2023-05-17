from datetime import datetime

from fastapi import APIRouter, Depends

from config.database import AsyncSession, get_session

from app.schemas.profile import ProfileRetrieve
from app.schemas.training import TrainingRetrieve, TrainingFilters, TrainingCreate

from app.services.profile.jwt import admin_permission, get_current_user
from app.services.training.crud import (
    get_training_list, get_training_retrieve, create_training,
    update_training, delete_training
)


training_router = APIRouter()


@training_router.get("/trainings/", response_model=list[TrainingRetrieve])
async def training_list(
        wpm: float | None = None,
        cpm: float | None = None,
        row_wpm: float | None = None,
        accuracy: int | None = None,
        consistency: datetime | None = None,

        profile_id: int | None = None,
        language_id: int | None = None,
        time_id: int | None = None,

        page: int = 1,
        page_size: int = 10,

        db: AsyncSession = Depends(get_session)
):
    filters = TrainingFilters(
        wpm=wpm, cpm=cpm, row_wpm=row_wpm, accuracy=accuracy, consistency=consistency,
        profile_id=profile_id, language_id=language_id, time_id=time_id
    )
    return await get_training_list(filters, page, page_size, db)


@training_router.get("/training/{training_id}/", response_model=TrainingRetrieve)
async def training_retrieve(
        training_id: int,
        db: AsyncSession = Depends(get_session)
):
    return await get_training_retrieve(training_id, db)


@training_router.post("/training/create/", response_model=TrainingRetrieve)
async def training_create(
        training: TrainingCreate,
        db: AsyncSession = Depends(get_session),
        current_user: ProfileRetrieve = Depends(get_current_user),
):
    return await create_training(training, db, current_user.id)


@training_router.patch("/training/{training_id}/update/", response_model=TrainingRetrieve)
async def training_update(
        training_id: int,
        training: TrainingFilters,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await update_training(training_id, training, db)


@training_router.delete("/training/{training_id}/delete/", status_code=204)
async def training_delete(
        training_id: int,
        db: AsyncSession = Depends(get_session),
        admin: ProfileRetrieve = Depends(admin_permission)
):
    return await delete_training(training_id, db)
