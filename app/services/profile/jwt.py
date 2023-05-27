from datetime import timedelta, datetime

from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


from passlib.context import CryptContext

from config.conf import settings
from config.database import AsyncSession, async_session

from app.models import Profile
from app.services.quries.profiles_quries import check_profile_with_email_exists
from app.schemas.profile import TokenData, JwtSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def admin_permission(token: str = Depends(oauth2_scheme)):
    """ Admin Permission """
    profile = await get_current_user(token)
    if not profile.is_admin:
        raise HTTPException(status_code=403, detail="No permissions for this action")


async def authenticate_user(email: str, password: str, db: AsyncSession) -> Profile | str:
    profile = await check_profile_with_email_exists(email, db)
    if not profile:
        return "Incorrect username or password"
    if not verify_password(password, profile.password):
        return "Incorrect username or password"
    if not profile.is_active:
        return "Profile is not active"
    return profile


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Profile:
    async with async_session() as db:
        return await get_user_instance(token, db)


async def get_current_user_by_refresh_token(token: str, db: AsyncSession) -> Profile:
    return await get_user_instance(token, db)


async def get_user_instance(token: str, db: AsyncSession):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await check_profile_with_email_exists(token_data.email, db)
    if user is None:
        raise credentials_exception
    return user


async def create_tokens(profile: Profile) -> JwtSchema:
    to_encode = {
        "sub": profile.email,
        "user_id": profile.id
    }
    access_expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 7)
    refresh_expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 24 * 30)

    to_encode.update({"exp": access_expire})
    to_encode.update({"token_type": "access"})
    access_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    to_encode.update({"exp": refresh_expire})
    to_encode.update({"token_type": "refresh"})
    refresh_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return JwtSchema(access_token=access_jwt, refresh_token=refresh_jwt)
