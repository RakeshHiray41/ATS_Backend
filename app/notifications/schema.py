from pydantic import BaseModel
from datetime import datetime


class NotificationResponseSchema(BaseModel):
    id: int
    message: str
    link: str | None
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }