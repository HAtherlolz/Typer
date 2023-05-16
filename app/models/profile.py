from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class Profile(Base):
    """ The model of profile table """
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, index=True
    )
    email: Mapped[str] = mapped_column("email", String(55), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column("password", String(255), nullable=False)
    nickname: Mapped[str] = mapped_column("nickname", String(255), nullable=False)
    avatar: Mapped[str] = mapped_column("avatar", String(), nullable=True)
    date_joined: Mapped[datetime] = mapped_column("date_joined", DateTime, default=datetime.utcnow)

    # Statements
    is_active: Mapped[bool] = mapped_column("is_active", Boolean(), nullable=False, default=False)
    is_admin: Mapped[bool] = mapped_column("is_admin", Boolean(), nullable=False, default=False)

    profile_lessons: Mapped["Lesson"] = relationship(
        "Lesson", back_populates="profile"
    )

    profile_trainings: Mapped["Training"] = relationship(
        "Training", back_populates="profile"
    )
