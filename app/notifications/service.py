from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

from app.notifications.model import Notification


def _purge_expired(db: Session, user_id: int):
    """Delete this user's notifications older than 24 hours. Called at the
    start of every read so old notifications quietly disappear from the
    inbox without needing a separate background cron job running."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.created_at < cutoff,
    ).delete()
    db.commit()


def create_notification(
    user_id: int,
    message: str,
    db: Session,
    link: str | None = None
):
    """Called from other modules (e.g. when an application status changes)
    to leave an in-app notification for a user. Best-effort — callers
    should not let a notification failure break the main action."""
    notification = Notification(
        user_id=user_id,
        message=message,
        link=link
    )
    db.add(notification)
    db.commit()
    return notification


def get_my_notifications(
    db: Session,
    current_user
):
    _purge_expired(db, current_user.id)
    return (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(50)
        .all()
    )


def get_unread_count(
    db: Session,
    current_user
):
    _purge_expired(db, current_user.id)
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,  # noqa: E712
        )
        .count()
    )


def mark_notification_read(
    notification_id: int,
    db: Session,
    current_user
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your notification")

    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification


def mark_all_read(
    db: Session,
    current_user
):
    (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False,  # noqa: E712
        )
        .update({"is_read": True})
    )
    db.commit()
    return {"detail": "All notifications marked as read"}