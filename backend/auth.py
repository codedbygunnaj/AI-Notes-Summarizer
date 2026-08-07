from fastapi import APIRouter, HTTPException
from backend.database import SessionLocal
from backend.models import User
from backend.schemas import (
    SignupRequest,
    LoginRequest,
    TokenResponse
)
from backend.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_verification_token
)
from backend.email_service import send_verification_email

from dotenv import load_dotenv
from datetime import datetime, UTC, timedelta
import os

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ======================================================
# Signup
# ======================================================

@router.post("/signup")   # @ decorator binds this endpoint with FastAPI
def signup(request: SignupRequest):

    db = SessionLocal()    # connects to database

    try:

        existing_user = db.query(User).filter(
            User.email == request.email    # finding email (unique)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered."
            )

        verification_token = generate_verification_token()

        verification_expiry = (
            datetime.now(UTC)
            + timedelta(hours=1)
        )

        new_user = User(
            email=request.email,
            password_hash=hash_password(request.password),   # stores hashed password
            verification_token=verification_token,
            verification_expires=verification_expiry,
            is_verified=False
        )

        db.add(new_user)       # adds object to session
        db.commit()            # commits to database
        db.refresh(new_user)   # refreshes python object from database

        verification_link = (
            f"{os.getenv('BACKEND_URL')}"
            f"/auth/verify?token={verification_token}"
        )

        try:

            send_verification_email(
                request.email,
                verification_link
            )

        except Exception:

            raise HTTPException(
                status_code=500,
                detail="Unable to send verification email."
            )

        return {
            "user_id": new_user.id,
            "message": "Verification email sent successfully."
        }

    finally:
        db.close()


# ======================================================
# Login
# ======================================================

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):

    db = SessionLocal()

    try:

        existing_user = db.query(User).filter(
            User.email == request.email
        ).first()

        if not existing_user:
            raise HTTPException(
                status_code=404,
                detail="User not found."
            )

        pwdFlag = verify_password(
            request.password,
            existing_user.password_hash
        )

        if not pwdFlag:
            raise HTTPException(
                status_code=401,
                detail="Incorrect password."
            )

        if not existing_user.is_verified:
            raise HTTPException(
                status_code=403,
                detail="Please verify your email before logging in."
            )

        payload = {
            "email": existing_user.email,
            "plan": existing_user.plan
        }

        token = create_access_token(payload)

        # returning JWT in TokenResponse format
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        db.close()


# ======================================================
# Email Verification
# ======================================================

@router.get("/verify")
def verify_email(token: str):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.verification_token == token
        ).first()

        if not user:
            raise HTTPException(
                status_code=400,
                detail="Invalid verification link."
            )

        if user.is_verified:
            return {
                "message": "Email already verified."
            }

        if (
            user.verification_expires
            and
            datetime.now(UTC).replace(tzinfo=None) > user.verification_expires
        ):
            raise HTTPException(
                status_code=410,
                detail="Verification link expired."
            )

        user.is_verified = True
        user.verification_token = None
        user.verification_expires = None

        db.commit()      # saves verification status

        return {
            "message": "Email verified successfully."
        }

    finally:
        db.close()