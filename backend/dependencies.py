from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from backend.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

def get_current_user(token:str = Depends(oauth2_scheme)):
    return verify_access_token(token)
    # splits bearer rjd..... to rjd.. (main token) and forward that to verify_token fn