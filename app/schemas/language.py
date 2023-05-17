from pydantic import BaseModel, validator


class LanguageBase(BaseModel):
    """ The base language schema """
    id: int

    class Config:
        orm_mode = True


class LanguageCreate(BaseModel):
    """ The schema for language creation """
    name: str

    @validator("name")
    def name_validator(cls, v: str) -> str:
        if len(v) > 50:
            raise ValueError("The password must contains no more than 50 letters")
        return v


class LanguageRetrieve(LanguageBase, LanguageCreate):
    pass
