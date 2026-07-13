from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from datetime import datetime

from app.database.base import Base


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    interview_date: Mapped[datetime] = mapped_column(
        DateTime
    )

    meeting_link: Mapped[str] = mapped_column(
        String(500)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Scheduled"
    )

    notes: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    application_id: Mapped[int] = mapped_column(
        ForeignKey("applications.id")
    )