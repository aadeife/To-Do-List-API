from fastapi import HTTPException, Header
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["user_id"]
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")
