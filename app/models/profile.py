from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Column, Table, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class ProfileLessonAssociation(Base):
    __tablename__ = 'profile_lesson'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer(), ForeignKey('profiles.id', ondelete="CASCADE"))
    lesson_id = Column(Integer(), ForeignKey('lessons.id', ondelete="CASCADE"))
    seconds_spent = Column(Integer(), nullable=True)
    is_done = Column(Boolean(), nullable=True)


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

    profile_lessons: Mapped[list["Lesson"]] = relationship(
        'Lesson',
        secondary="profile_lesson",
        back_populates='lesson_profiles',
        passive_deletes=True,
    )

    profile_trainings: Mapped[list["Training"]] = relationship(
        "Training", back_populates="profiles"
    )
