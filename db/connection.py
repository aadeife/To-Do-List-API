import sqlite3

sql_statements = [
    """CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            date DATE
        );
    """,

    """CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """
]

try:
    with sqlite3.connect("to-do.db") as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

        cursor = conn.cursor()

        for statement in sql_statements:
            cursor.execute(statement)

        conn.commit()

        print("Tables created succesfully.")

        conn.execute("PRAGMA foreign_keys = ON")
        
except sqlite3.OperationalError as e:
    print("Failed to connect to database:", e)

def get_db():
    conn = sqlite3.connect("to-do.db")
    conn.row_factory = sqlite3.Row  # lets you access columns by name instead of index
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()