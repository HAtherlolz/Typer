from pydantic import BaseModel, validator, EmailStr

from datetime import datetime

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


class TrainingProfileRetrieve(TrainingBase):
    """ Schema to return trainings for profile """
    wpm: float
    cpm: float
    row_wpm: float
    accuracy: int
    consistency: int
    date_time: datetime
    training_language: LanguageRetrieve
    time: TimeRetrieve


class ProfileRetrieve(BaseModel):
    """ Schema for retrieve profile fields """
    id: int
    email: EmailStr
    nickname: str
    avatar: str | None
    date_joined: datetime
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class TrainingRetrieve(TrainingProfileRetrieve):
    """ The training retrieve schema """
    profiles: ProfileRetrieve


