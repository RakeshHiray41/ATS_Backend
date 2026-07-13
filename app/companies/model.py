from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1000))
    website: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    logo_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )