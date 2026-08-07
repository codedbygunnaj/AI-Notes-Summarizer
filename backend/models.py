#v1: Only 1 table:: Users(id, email, pwd_hash, plan, daily_usage, created_at)

from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime, UTC
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, index=True
    )

    email = Column(
        String, unique=True, nullable=False
    )

    password_hash = Column(
        String, nullable=False
    )

    plan = Column(
        String, default="free"
    )

    daily_usage = Column(
        Integer, default=0
    )

    created_at = Column(
        DateTime, default= lambda: datetime.now(UTC)
    )

    last_usage = Column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    # ======================================================
    # Email Verification
    # ======================================================

    is_verified = Column(
        Boolean,
        default=False
    )

    verification_token = Column(
        String,
        nullable=True
    )

    verification_expires = Column(
        DateTime(timezone=True),
        nullable=True
    )
