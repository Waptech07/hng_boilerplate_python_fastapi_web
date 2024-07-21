from api.db.database import get_db
from api.v1.models.user import User
from api.v1.models.org import Organization
from api.v1.models.profile import Profile
from api.v1.models.product import Product
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from api.v1.schemas.auth import PasswordResetRequest
from api.v1.core.security import create_reset_token
from api.v1.core.email import send_password_reset_email

router = APIRouter()


@router.post("/password-reset-email", status_code=status.HTTP_200_OK)
async def password_reset_email(request: PasswordResetRequest, db: Session = Depends(get_db)):
    # Verify if the email exists in the database
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    # Generate a unique token for password reset using JWT
    token_data = {"sub": str(user.email)}
    token = create_reset_token(token_data)

    # Send the password reset email with the reset link
    reset_link = f"https://example.com/reset-password?token={token}"
    send_password_reset_email(user.email, reset_link)

    return {"message": "Password reset email sent successfully.", "reset_link": reset_link}
