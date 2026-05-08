from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserResponse, UserUpdate, UserLogin
import sqlite3
from db import connection
from pwdlib import PasswordHash

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
        new_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    if new_user:
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




