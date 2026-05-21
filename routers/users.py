from fastapi import APIRouter, HTTPException, Depends
from models import UserCreate, UserResponse, UserUpdate
import sqlite3
from db import connection
from dependencies import SECRET_KEY, get_current_user

router = APIRouter(prefix="/users")

@router.get("/{user_id}")
def get_user(user_id: int, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            """SELECT * FROM users WHERE user_id = ?""", (user_id,)
        )
        user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
        
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif user["user_id"] != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        return UserResponse(user_id=user["user_id"],
                            name=user["name"],
                            email=user["email"],
                            date=user["date"]     
        )   
    
@router.put("/{user_id}")
def update_user(user_id: int, user: UserUpdate, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    fields = {k: v for k, v in user.model_dump().items() if v is not None}
    columns = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(user_id)

    check_user = """
                    SELECT * FROM users WHERE user_id = ?
                 """
    update_user =f"""
                    UPDATE users SET {columns} WHERE user_id = ?
                  """
    
    cursor = db.cursor()
    try:
        cursor.execute(
               check_user, (user_id,)
          )
        existing_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
         
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif existing_user["user_id"] != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")
 
    try:
        cursor.execute(
                update_user, tuple(values)
            )
        db.commit()
        cursor.execute(
            check_user, (user_id,)
        )
        updated_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
        
    
    return UserResponse(user_id=updated_user["user_id"],
                            name=updated_user["name"],
                            email=updated_user["email"],
                            date=updated_user["date"]
    )

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user = Depends(get_current_user), db=Depends(connection.get_db)):
    user_delete = """
                    DELETE FROM users WHERE user_id = ?
                  """
    
    check_user = """
                    SELECT * FROM users WHERE user_id = ?
                 """
     
    cursor = db.cursor()

    try:
        cursor.execute(check_user, (user_id,))
        existing_user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    elif existing_user["user_id"] != current_user:
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        cursor.execute(
            user_delete, (user_id,)
        )
        db.commit()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    return {"message": "User deleted successfully."}