from datetime import datetime, UTC, timedelta
import os
from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
#cryptcontext instead of bcrypt (for pswd hashing) so that if bcrypt becomes old and argon2 or anyother comes, cryptcontext acts as a manager and handles all that on it's own!
from jose import JWTError
from backend.database import SessionLocal
from backend.models import User
from fastapi import HTTPException
import secrets

load_dotenv()
SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #one hour

#JWT = [header, payload, signature] => signature uses algorithm (hs256)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)
# hello123 -> $2b$12$ahsdjkashdjkashd... (everytime diff hash even if pwd same (uses diff "salt"))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
#passlib automatically extracts salt from the hashed_password, use that and hash plain password and both hash same? password same!

def create_access_token(data: dict):    

    to_encode = data.copy() #bcz if coming from login/signup we can't modify that

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #now+1hr
    to_encode.update({
        "exp":expire} #in jwt standards exp means expire
    )

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY_JWT,
        algorithm=ALGORITHM
    )

    return encoded_jwt

def verify_access_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY_JWT,
            algorithms=[ALGORITHM]
        )

        currUserEmail = payload.get("email")
        if currUserEmail is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        db = SessionLocal()
        try:
            user_exists = db.query(User).filter(
                User.email == currUserEmail
            ).first()
            if not user_exists:
                raise HTTPException(
                    status_code=401,
                    detail="User does not exist."
                )

            return user_exists      #Return complete user object

        finally:
            db.close()

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token."
        )
    
def generate_verification_token():
    return secrets.token_urlsafe(32)