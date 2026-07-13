from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Applied"
    )

    applied_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id")
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    resume_url: Mapped[str] = mapped_column(
        String(1000)
    )