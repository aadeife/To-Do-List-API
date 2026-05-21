from fastapi import HTTPException, Header, Security
from fastapi.security import HTTPBearer
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

security = HTTPBearer()

def get_current_user(credentials = Security(security)):
    token = credentials.credentials

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
