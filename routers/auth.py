from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserResponse, UserUpdate, UserLogin, TokenResponse
import sqlite3
from db import connection
from pwdlib import PasswordHash
from jose import jwt

router = APIRouter()
password_hash = PasswordHash.recommended()

@router.post("/register")
def user_registration(user: UserCreate, db = Depends(connection.get_db)):
    check_user = """
                    SELECT * FROM users WHERE email = ?
                 """
    add_user = """
                INSERT INTO users (name, email, password)
                VALUES(?, ?, ?)
               """
    cursor = db.cursor()

    try:
        cursor.execute(
            check_user, (user.email,)
        )
        existing_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists.")
    
    try:
        #hash and add user to db
        hashed = password_hash.hash(user.password)
        cursor.execute(
            add_user, (user.name, user.email, hashed)
        )
        db.commit()
        user_id = cursor.lastrowid
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    token = jwt.encode(a{"user_id": user_id}, 'secret', algorithm='HS256')

    return TokenResponse(token=token)

@router.post("/login")
def user_login(user: UserLogin, db = Depends(connection.get_db)):
    # check user exists
    check_user = """
                    SELECT * FROM users WHERE email = ?
                 """
    
    cursor = db.cursor()
    
    try:
        cursor.execute(
            check_user, (user.email,)
        )
        existing_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    # check password
    real_pwd = existing_user["password"]
    user_id = existing_user["user_id"]

    if not password_hash.verify(user.password, real_pwd):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    
    token = jwt.encode({"user_id": user_id}, 'secret', algorithm='HS256')

    return TokenResponse(token=token)
    





