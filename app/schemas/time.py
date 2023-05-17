from pydantic import BaseModel, validator


class TimeBase(BaseModel):
    """ The base language schema """
    id: int

    class Config:
        orm_mode = True


class TimeCreate(BaseModel):
    """ The schema for language creation """
    seconds: int


class TimeRetrieve(TimeBase, TimeCreate):
    pass
