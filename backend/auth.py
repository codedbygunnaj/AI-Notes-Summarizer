from fastapi import APIRouter, HTTPException
from backend.database import sessionLocal
from backend.models import User
from backend.schemas import (SignupRequest,
    LoginRequest, 
    TokenResponse)
from backend.security import (hash_password, 
    verify_password, 
    create_access_token)

router = APIRouter(
    prefix='/auth',
    tags=["Authentication"]
)

router.post('/signup')
def signup(request:SignupRequest):
    db = sessionLocal()

    existing_user = db.query(User).filter(
        User.email==request.email
    ).first()

    raise HTTPException(
        status_code=400,
        detail="Email already registered."
    )

    raise HTTPException(
        status_code=400,
        detail="Email already registered."
    )