from sqlalchemy import String, Boolean, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from app.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    message: Mapped[str] = mapped_column(String(500))
    link: Mapped[str] = mapped_column(String(300), nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )