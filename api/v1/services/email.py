from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from api.utils.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True
)

async def send_password_reset_email(email: str, reset_link: str):
    html = f"""
    <html>
    <body>
        <h1>Password Reset Request</h1>
        <p>Hello,</p>
        <p>You requested a password reset. Please use the link below to reset your password. This link will expire in 15 minutes.</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <a>{reset_link}</a>
        <p>If you did not request this password reset, please ignore this email.</p>
        <p>Thank you,</p>
        <p>YourAppName Team</p>
    </body>
    </html>
    """

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
