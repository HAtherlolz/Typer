from fastapi import HTTPException

from app.services.utils.utils import pagination
from config.database import AsyncSession

from app.models import Training
from app.schemas.training import TrainingFilters, TrainingCreate
from app.services.quries.trainings_queries import (
    get_training_list_instance, get_training_by_id, create_training_instance,
    update_training_instance, delete_training_instance
)


async def get_training_list(
        filters: TrainingFilters,
        page: int,
        page_size: int,
        db: AsyncSession
) -> list[Training]:
    offset = await pagination(page, page_size)
    return await get_training_list_instance(filters, offset, page_size, db)


async def get_training_retrieve(
        training_id: int,
        db: AsyncSession
) -> Training:
    training = await get_training_by_id(training_id, db)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    return training


async def create_training(
        training: TrainingCreate,
        db: AsyncSession,
        current_user_id: int
) -> Training:
    training.profile_id = current_user_id
    return await create_training_instance(training, db)


async def update_training(
        training_id: int,
        training: TrainingFilters,
        db: AsyncSession
) -> Training:
    check_training_exist = await get_training_by_id(training_id, db)
    if not check_training_exist:
        raise HTTPException(status_code=404, detail="Training not found")
    return await update_training_instance(training_id, training, db)


async def delete_training(
        training_id: int,
        db: AsyncSession
) -> None:
    check_training_exist = await get_training_by_id(training_id, db)
    if not check_training_exist:
        raise HTTPException(status_code=404, detail="Training not found")
    return await delete_training_instance(training_id, db)
