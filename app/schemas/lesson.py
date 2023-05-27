from pydantic import BaseModel, validator, EmailStr

from datetime import datetime

from app.schemas.language import LanguageRetrieve


class LessonBase(BaseModel):
    """ The base training schema """
    id: int

    class Config:
        orm_mode = True


class LessonCreate(BaseModel):
    """ The training creating schema """
    name: str
    wpm: float
    cpm: float
    row_wpm: float
    accuracy: int
    consistency: int
    language_id: int

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


class LessonFilters(BaseModel):
    """
        The lesson fields for filtering schema
    """
    name: str
    wpm: float | None
    cpm: float | None
    row_wpm: float | None
    accuracy: int | None
    consistency: int | None
    date_time: datetime | None

    profile_id: int | None
    language_id: int | None


class LessonInfo(BaseModel):
    """ Lesson info """
    seconds_spent: int
    is_done: bool

    class Config:
        orm_mode = True


class LessonRetrieve(BaseModel):
    """ The lessons schema for getting data """
    name: str
    wpm: float
    cpm: float
    row_wpm: float
    accuracy: int
    consistency: int
    date_time: datetime
    language: LanguageRetrieve


class LessonProfile(LessonRetrieve):
    """ The lesson schema for profile """
    lesson_info: LessonInfo


class ProfileRetrieve(BaseModel):
    """ Schema for retrieve profile fields """
    id: int
    email: EmailStr
    nickname: str
    avatar: str | None

    class Config:
        orm_mode = True


class LessonWithProfile(LessonRetrieve):
    lesson_profiles: ProfileRetrieve

