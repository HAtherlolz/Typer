from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from config.database import AsyncSession

from app.models import Training, Profile, Language, Time


from app.schemas.training import TrainingFilters, TrainingCreate


async def get_training_list_instance(
        filters: TrainingFilters,
        offset: int,
        page_size: int,
        db: AsyncSession
) -> list[Training]:
    trainings = select(Training).options(
        selectinload(Training.profile), selectinload(Training.training_language), selectinload(Training.time)
    ).offset(offset).limit(page_size)
    if filters.wpm:
        trainings = trainings.where(Training.wpm == filters.wpm)
    if filters.cpm:
        trainings = trainings.where(Training.cpm == filters.cpm)
    if filters.row_wpm:
        trainings = trainings.where(Training.row_wpm == filters.row_wpm)
    if filters.accuracy:
        trainings = trainings.where(Training.accuracy == filters.accuracy)
    if filters.consistency:
        trainings = trainings.where(Training.consistency == filters.consistency)
    if filters.profile_id:
        trainings = trainings.join(Training.profile).where(Profile.id == filters.profile_id)
    if filters.language_id:
        trainings = trainings.join(Training.training_language).where(Language.id == filters.language_id)
    if filters.time_id:
        trainings = trainings.join(Training.time).where(Time.id == filters.time_id)

    res = await db.execute(trainings)
    return res.scalars().all()


async def get_training_by_id(
        training_id: int,
        db: AsyncSession
) -> Training | None:
    training = await db.execute(
        select(Training).options(
            selectinload(Training.time),
            selectinload(Training.profile),
            selectinload(Training.training_language),
        ).where(Training.id == training_id)
    )
    return training.scalar_one_or_none()


async def create_training_instance(
        training: TrainingCreate,
        db: AsyncSession,
) -> Training:
    new_training = Training(**training.dict())
    db.add(new_training)
    await db.commit()
    await db.refresh(new_training)
    return await get_training_by_id(new_training.id, db)


async def update_training_instance(
        training_id: int,
        training: TrainingFilters,
        db: AsyncSession
) -> Training:
    updated_training = await db.execute(
        update(Training).where(Training.id == training_id).values(
            **training.dict(exclude_none=True)
        ).returning(Training)
    )
    await db.commit()
    updated_training = updated_training.scalar_one()
    await db.refresh(updated_training)
    return updated_training


async def delete_training_instance(
        training_id: int,
        db: AsyncSession
) -> None:
    training = await db.get(Training, training_id)
    await db.delete(training)
    await db.commit()
