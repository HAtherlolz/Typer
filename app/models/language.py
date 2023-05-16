from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base


class Language(Base):
    """ The model of language table """
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column("name", String(50), nullable=False)

    lessons_languages: Mapped["Lesson"] = relationship(
        "Lesson", back_populates="language"
    )

    trainings_languages: Mapped["Training"] = relationship(
        "Training", back_populates="training_language"
    )
