from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    location: Mapped[str] = mapped_column(
        String(255)
    )

    experience: Mapped[str] = mapped_column(
        String(100)
    )

    salary: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="open"
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id")
    )