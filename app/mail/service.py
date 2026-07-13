from fastapi_mail import (
    FastMail,
    MessageSchema,
    MessageType
)

from app.mail.config import conf


async def send_email(
    subject: str,
    email: str,
    body: str
):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    await fm.send_message(message)