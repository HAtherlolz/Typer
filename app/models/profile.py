from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Column, Table, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


profile_lesson_association = Table(
    'profile_lesson', Base.metadata,
    Column('profile_id', ForeignKey('profiles.id', ondelete="CASCADE"), primary_key=True),
    Column('lesson_id', ForeignKey('lessons.id', ondelete="CASCADE"), primary_key=True),
    Column("seconds_spent", Integer(), nullable=True),
    Column("is_done", Boolean(), nullable=True),
)


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

    # profile_lessons: Mapped["Lesson"] = relationship(
    #     "Lesson", back_populates="profile"
    # )

    profile_lessons: Mapped[list["Lesson"]] = relationship(
        'Lesson',
        secondary=profile_lesson_association,
        back_populates='lesson_profiles',
        passive_deletes=True,
        #overlaps="bookmarked_activities,profile_bookmarked_activities"
    )

    profile_trainings: Mapped["Training"] = relationship(
        "Training", back_populates="profile"
    )
