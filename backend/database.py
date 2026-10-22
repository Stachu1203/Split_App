import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def get_db_connection():
    conn = sqlite3.connect('splitapp.db')   
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
    )
    ''')
    conn.commit()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_by INTEGER NOT NULL,
    FOREIGN KEY (created_by)
    REFERENCES users(id)
    ON DELETE CASCADE 
    )
    ''')
    conn.commit()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS trip_members (
    trip_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (trip_id, user_id),
    FOREIGN KEY (trip_id) 
    REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) 
    REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    conn.commit()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    payer_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (payer_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    conn.commit()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS expense_splits (
    expense_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    amount_owed REAL NOT NULL,
    PRIMARY KEY (expense_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE
    )
    ''')
    conn.commit()

    conn.close()

def create_user(username, password):
    conn = get_db_connection()
    hashed_password = generate_password_hash(password)
    try:
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def verify_user(username, password):
        conn = get_db_connection()
        
        user = conn.execute('SELECT password_hash FROM users WHERE username = ?',(username,)).fetchone()
        conn.close()

        if user == None:
             return False

        if check_password_hash(user['password_hash'],password):
             return True

        return False



