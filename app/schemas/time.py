from pydantic import BaseModel


class TimeBase(BaseModel):
    """ The base time schema """
    id: int

    class Config:
        orm_mode = True


class TimeCreate(BaseModel):
    """ The schema for time creation """
    seconds: int


class TimeRetrieve(TimeBase, TimeCreate):
    """ The schema for retrieve creation """
    pass
