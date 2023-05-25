from datetime import datetime

from sqlalchemy import ForeignKey, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class Training(Base):
    """ The model of training table """
    __tablename__ = "trainings"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, index=True
    )
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

    time_id: Mapped[int] = mapped_column(
        "time_id", ForeignKey("times.id"), nullable=False
    )

    profiles: Mapped["Profile"] = relationship(
        "Profile", back_populates="profile_trainings"
    )

    training_language: Mapped["Language"] = relationship(
        "Language", back_populates="trainings_languages"
    )

    time: Mapped["Time"] = relationship(
        "Time", back_populates="time_trainings"
    )
