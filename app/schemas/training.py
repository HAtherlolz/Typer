from pydantic import BaseModel, validator

from datetime import datetime

from app.schemas.profile import ProfileRetrieve
from app.schemas.language import LanguageRetrieve
from app.schemas.time import TimeRetrieve


class TrainingBase(BaseModel):
    """ The base training schema """
    id: int

    class Config:
        orm_mode = True


class TrainingCreate(BaseModel):
    """ The training creating schema """
    wpm: float
    cpm: float
    row_wpm: float
    accuracy: int
    consistency: int

    profile_id: int | None
    language_id: int
    time_id: int

    @validator("accuracy")
    def accuracy_validator(cls, v: int) -> int:
        if v > 100 or v < 1:
            raise ValueError("Invalid percent of accuracy")
        return v

    @validator("consistency")
    def consistency_validator(cls, v: int) -> int:
        if v > 100 or v < 1:
            raise ValueError("Invalid percent of accuracy")
        return v


class TrainingFilters(BaseModel):
    """
        The training fields for filtering schema
    """
    wpm: float | None
    cpm: float | None
    row_wpm: float | None
    accuracy: int | None
    consistency: int | None
    date_time: datetime | None

    profile_id: int | None
    language_id: int | None
    time_id: int | None


class TrainingRetrieve(TrainingBase):
    """ The training retrieve schema """
    wpm: float
    cpm: float
    row_wpm: float
    accuracy: int
    consistency: int
    date_time: datetime

    profile: ProfileRetrieve
    training_language: LanguageRetrieve
    time: TimeRetrieve

