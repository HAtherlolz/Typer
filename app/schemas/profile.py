import re

from datetime import datetime

from pydantic import BaseModel, EmailStr, validator


class ProfileBase(BaseModel):
    """ The base schema of profile """
    id: int

    class Config:
        orm_mode = True


class ProfileEmail(BaseModel):
    """ Email Profile schema """
    email: EmailStr


class ProfileLogin(ProfileEmail):
    """ Schema for login"""
    password: str

    @validator("password")
    def password_validator(cls, v: str) -> str:
        password_regex = r"^(?=.*[A-Z])(?=.*\d).{8,}$"
        if not re.match(password_regex, v):
            raise ValueError("The password must contains at least 8 charset, at least 1 uppercase charset")
        return v


class ProfileFilters(BaseModel):
    """ Schema of fields for filters """
    email: EmailStr | None = None,
    nickname: str | None = None,
    date_join: datetime | None = None,
    is_active: bool | None = None,
    is_admin: bool | None = None,
    lessons: str | None = None,
    trainings: str | None = None,


class ProfileRetrieve(ProfileBase):
    """ Schema for retrieve profile fields """
    email: EmailStr
    nickname: str
    avatar: str | None
    date_joined: datetime
    is_active: bool
    is_admin: bool


class ProfileCreate(ProfileLogin):
    """
        Schema for validation profile's fields in creation
    """
    nickname: str


class ProfileUpdate(BaseModel):
    """ Schema for validation profile's fields in updating """
    nickname: str | None
    avatar: str | None


class NewPassword(BaseModel):
    """
        Schema for checking password in reset endpoint
    """
    token: str
    password: str


class TokenData(BaseModel):
    email: str


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class JwtSchema(RefreshToken, AccessToken):
    pass

