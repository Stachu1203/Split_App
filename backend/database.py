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

def create_trip(name,user_id):

    conn = get_db_connection()
    cursor = conn.cursor()
     
    if name is None or user_id is None:
          return False

    try:
         cursor.execute('INSERT INTO trips (name,created_by) VALUES (?,?)',(name,user_id))
         new_trip_id = cursor.lastrowid
         cursor.execute('INSERT INTO trip_members (trip_id,user_id) VALUES (?,?)', (new_trip_id,user_id))

         conn.commit()
         return new_trip_id
    except sqlite3.IntegrityError:
            conn.rollback()
            return False
    finally:
            conn.close() 

def get_user_trips(user_id):

     conn = get_db_connection()
     cursor = conn.cursor()
     trips_list = []
     if user_id is None:
          return []

     try:
          cursor.execute('SELECT id, name, created_by FROM trips JOIN trip_members ON trips.id = trip_members.trip_id WHERE trip_members.user_id = ?',(user_id,))
          trips_list = cursor.fetchall()
     finally:
          conn.close()
     return trips_list

def add_user_to_trip(user_id,trip_id):

     if user_id is None or trip_id is None:
          return False

     conn = get_db_connection()
     cursor = conn.cursor()

     try:
          cursor.execute('INSERT INTO trip_members (trip_id, user_id) VALUES (?,?)',(trip_id,user_id))
          conn.commit()
     except sqlite3.IntegrityError:
          conn.rollback()
          return False
     finally:
          conn.close()
     return 

def add_expense(trip_id, payer_id, title, total_amount, splits):
     
     if trip_id is None or payer_id is None or title is None or total_amount is None:
          return False
     
     total_check = 0 

     for i in range(len(splits)):
          total_check += splits[i][1]

     if total_check != total_amount:
          return False
     conn = get_db_connection()
     cursor = conn.cursor()

     try:
          cursor.execute('INSERT INTO expenses (trip_id,payer_id,title,total_amount) VALUES (?,?,?,?)',(trip_id,payer_id,title,total_amount))
          new_expense_id = cursor.lastrowid
     

          for userId, amount in splits:
              cursor.execute('INSERT INTO expense_splits (expense_id,user_id,amount_owed) VALUES (?,?,?)', (new_expense_id,userId,amount))
          conn.commit()
     except sqlite3.IntegrityError:
              conn.rollback()
              return False
          
     finally:
        conn.close()
     return True

def get_trip_expenses(trip_id):
     if trip_id is None:
          return []
     
     conn = get_db_connection()
     cursor = conn.cursor()

     expensesList = []
     try:
          cursor.execute('SELECT expenses.id, expenses.title, expenses.total_amount, users.username FROM expenses JOIN users ON users.id = expenses.payer_id WHERE expenses.trip_id =?',(trip_id,))
          expensesList = cursor.fetchall()
     finally:
          conn.close()
     return expensesList

def get_trip_users(trip_id):
     if trip_id is None:
          return []
     conn =get_db_connection()
     cursor = conn.cursor()
     tripUsersList = []
     try:
          cursor.execute('SELECT users.id, users.username FROM users JOIN trip_members ON users.id = trip_members.user_id WHERE trip_members.trip_id = ?',(trip_id,))
          tripUsersList = cursor.fetchall()
     finally:
          conn.close()
     return tripUsersList
     



    
     
     



