from fastapi import APIRouter, HTTPException, Depends
from models import ItemCreate, ItemResponse, ItemUpdate, PaginatedItemResponse
import sqlite3
from db import connection
from pwdlib import PasswordHash
from jose import jwt
from dependencies import SECRET_KEY, get_current_user

router = APIRouter(prefix="/items")

@router.get("/")
def get_items(page: int = 1, limit: int = 10, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    offset = (page - 1) * limit
    find_items =    """
                    SELECT * FROM items WHERE user_id = ?
                    LIMIT ? OFFSET ?
                    """
    count_items =   """
                    SELECT COUNT(*) FROM items WHERE user_id = ?
                    """
    cursor = db.cursor()
    
    try:
        cursor.execute(
            find_items, (current_user, limit, offset,)
        )
        all_items = cursor.fetchall()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")

    if all_items is None:
        raise HTTPException(status_code=404, detail="No Items Found")
    
    try:
        cursor.execute(
            count_items, (current_user,)
        )
        item_count = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    items = [ItemResponse(
    item_id=item["item_id"],
    user_id=item["user_id"],
    title=item["title"],
    description=item["description"],
    completed=item["completed"],
    created_at=item["created_at"]
    ) for item in all_items]

    return PaginatedItemResponse(
        data=items,
        page=page,
        limit=limit,
        total=item_count[0]
    )

@router.get("/{item_id}")
def get_item(item_id: int, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    find_item = """
                    SELECT * FROM items WHERE item_id = ?"""
    
    cursor = db.cursor()
    try:
        cursor.execute(
            find_item, (item_id,)
        )
        existing_item = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if existing_item["user_id"] != current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return ItemResponse(
        item_id=existing_item["item_id"],
        user_id=existing_item["user_id"],
        title=existing_item["title"],
        description=existing_item["description"],
        completed=existing_item["completed"],
        created_at=existing_item["created_at"]
    )
    

@router.post("/")
def create_item(item: ItemCreate, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    add_item = """
                INSERT INTO items (user_id, title, description)
                VALUES(?, ?, ?)
                """
    find_item = """
                    SELECT * FROM items WHERE item_id = ?"""
    
    cursor = db.cursor()

    try:
        cursor.execute(
            add_item, (current_user, item.title, item.description,)
        )
        db.commit()
        item_id = cursor.lastrowid
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    try:
        cursor.execute(
            find_item, (item_id,)
        )
        new_item = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    return ItemResponse(
        item_id=new_item["item_id"],
        user_id=new_item["user_id"],
        title=new_item["title"],
        description=new_item["description"],
        completed=new_item["completed"],
        created_at=new_item["created_at"]
    )

@router.put("/{item_id}")
def update_item(item_id: int, item: ItemUpdate, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    fields = {k: v for k, v in item.model_dump().items() if v is not None}
    columns = ", ".join([f"{key} = ?" for key in fields.keys()])
    values = list(fields.values())
    values.append(item_id)

    check_item = """
                    SELECT * FROM items WHERE item_id = ?
                 """
    update_item =f"""
                    UPDATE items SET {columns} WHERE item_id = ?
                  """
    
    cursor = db.cursor()
    try:
        cursor.execute(
               check_item, (item_id,)
          )
        existing_item = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
     
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if existing_item["user_id"] != current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
 
    try:
        cursor.execute(
                update_item, tuple(values)
            )
        db.commit()
        cursor.execute(
            check_item, (item_id,)
        )
        updated_item = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
        
    return ItemResponse(
        item_id=updated_item["item_id"],
        user_id=updated_item["user_id"],
        title=updated_item["title"],
        description=updated_item["description"],
        completed=updated_item["completed"],
        created_at=updated_item["created_at"]
    )

@router.delete("/{item_id}")
def delete_item(item_id: int, current_user = Depends(get_current_user), db = Depends(connection.get_db)):
    check_item = """
                    SELECT * FROM items WHERE item_id = ?
                 """
    
    delete_item = """
                    DELETE FROM items WHERE item_id = ?
                  """
    
    cursor = db.cursor()

    try:
        cursor.execute(
            check_item, (item_id,)
        )
        existing_item = cursor.fetchone()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")
    
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if current_user != existing_item["user_id"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        cursor.execute(
            delete_item, (item_id,)
        )
        db.commit()
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail="Database error")

    return {"message": "Item deleted successfully."}


