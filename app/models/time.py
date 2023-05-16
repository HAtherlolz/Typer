from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class Time(Base):
    """ The model of Time table """
    __tablename__ = "times"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, index=True
    )
    seconds: Mapped[int] = mapped_column("seconds", Integer(), nullable=False)

    time_trainings: Mapped["Training"] = relationship(
        "Training", back_populates="time"
    )
