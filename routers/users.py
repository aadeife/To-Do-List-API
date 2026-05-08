from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserResponse, UserUpdate
import sqlite3
from db import connection

router = APIRouter()

@router.get("/{user_id}")
def get_user(user_id: int, db = Depends(connection.get_db)):
        cursor = db.cursor()
        try:
            cursor.execute(
                """SELECT * FROM users WHERE user_id = ?""", (user_id,)
            )

            user = cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            else:
                return UserResponse(user_id=user["user_id"],
                                    name=user["name"],
                                    email=user["email"],
                                    date=user["date"]
                )
        except sqlite3.OperationalError as e:
             raise HTTPException(status_code=500, detail="Database error")
             
