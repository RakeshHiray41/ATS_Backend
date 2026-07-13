from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    bio: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    skills: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    experience: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    linkedin_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    github_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    resume_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )

    photo_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True
    )