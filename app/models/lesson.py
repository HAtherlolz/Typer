from datetime import datetime

from sqlalchemy import String, ForeignKey, Float, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class Lesson(Base):
    """ The model of lesson table """
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column("name", String(50), nullable=False)
    text: Mapped[str] = mapped_column("text", Text(), nullable=True)
    seconds_spent: Mapped[int] = mapped_column("seconds", Integer(), nullable=False)

    wpm: Mapped[float] = mapped_column("wpm", Float(), nullable=False, index=True)
    cpm: Mapped[float] = mapped_column("cpm", Float(), nullable=False, index=True)
    row_wpm: Mapped[float] = mapped_column("row_wpm", Float(), nullable=False, index=True)
    accuracy: Mapped[int] = mapped_column("accuracy", Integer(), nullable=False, index=True)
    consistency: Mapped[int] = mapped_column("consistency", Integer(), nullable=False, index=True)

    date_time: Mapped[datetime] = mapped_column("date_time", DateTime, default=datetime.utcnow)

    profile_id: Mapped[int] = mapped_column(
        "profile_id", ForeignKey("profiles.id"), nullable=False
    )

    language_id: Mapped[int] = mapped_column(
        "language_id", ForeignKey("languages.id"), nullable=False
    )

    profile: Mapped["Profile"] = relationship(
        "Profile", back_populates="profile_lessons"
    )

    language: Mapped["Language"] = relationship(
        "Language", back_populates="lessons_languages"
    )



