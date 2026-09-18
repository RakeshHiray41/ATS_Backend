from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.dependencies import get_current_user
from app.users.model import User

from app.notifications.schema import NotificationResponseSchema
from app.notifications.service import (
    get_my_notifications,
    get_unread_count,
    mark_notification_read,
    mark_all_read,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/my", response_model=list[NotificationResponseSchema])
def my_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_my_notifications(db, current_user)


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"count": get_unread_count(db, current_user)}


@router.patch("/{notification_id}/read", response_model=NotificationResponseSchema)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return mark_notification_read(notification_id, db, current_user)


@router.patch("/read-all")
def read_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return mark_all_read(db, current_user)