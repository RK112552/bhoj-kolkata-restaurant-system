import os
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

DB_MODE = os.getenv("DB_MODE", "mysql").lower()

def get_connection():
    if DB_MODE == "sqlite":
        import sqlite3
        path = os.getenv("SQLITE_PATH", "bhoj_preview.db")
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        return conn
    import mysql.connector
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "bhoj_kolkata"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        autocommit=False,
    )

def is_sqlite(conn):
    return conn.__class__.__module__.startswith("sqlite3")

def row_dict(row):
    return dict(row) if row is not None else None

def rows_dict(rows):
    return [dict(r) for r in rows]

def execute(conn, sql, params=()):
    cur = conn.cursor(dictionary=True) if not is_sqlite(conn) else conn.cursor()
    cur.execute(sql, params)
    return cur

def init_preview_db():
    """Optional lightweight SQLite preview. MySQL remains the required DBMS for PBL."""
    if DB_MODE != "sqlite":
        return
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL, role TEXT NOT NULL, full_name TEXT NOT NULL,
      email TEXT, phone TEXT, active INTEGER DEFAULT 1
    );
    CREATE TABLE IF NOT EXISTS customers(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE,
      full_name TEXT NOT NULL, phone TEXT, email TEXT,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS dining_tables(
      id INTEGER PRIMARY KEY AUTOINCREMENT, table_number TEXT UNIQUE NOT NULL,
      capacity INTEGER NOT NULL, area TEXT DEFAULT 'Main Hall', status TEXT DEFAULT 'available'
    );
    CREATE TABLE IF NOT EXISTS food_categories(
      id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL
    );
    CREATE TABLE IF NOT EXISTS menu_items(
      id INTEGER PRIMARY KEY AUTOINCREMENT, category_id INTEGER, name TEXT NOT NULL,
      description TEXT, price REAL NOT NULL, is_available INTEGER DEFAULT 1,
      is_vegetarian INTEGER DEFAULT 0, image_url TEXT,
      FOREIGN KEY(category_id) REFERENCES food_categories(id)
    );
    CREATE TABLE IF NOT EXISTS reservations(
      id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, table_id INTEGER,
      reservation_at TEXT NOT NULL, guests INTEGER NOT NULL, status TEXT DEFAULT 'pending',
      notes TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(customer_id) REFERENCES customers(id),
      FOREIGN KEY(table_id) REFERENCES dining_tables(id)
    );
    CREATE TABLE IF NOT EXISTS food_orders(
      id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER, order_type TEXT DEFAULT 'dine_in',
      table_id INTEGER, status TEXT DEFAULT 'placed', total_amount REAL DEFAULT 0,
      notes TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(customer_id) REFERENCES customers(id),
      FOREIGN KEY(table_id) REFERENCES dining_tables(id)
    );
    CREATE TABLE IF NOT EXISTS order_items(
      id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER, menu_item_id INTEGER,
      quantity INTEGER NOT NULL, unit_price REAL NOT NULL,
      FOREIGN KEY(order_id) REFERENCES food_orders(id),
      FOREIGN KEY(menu_item_id) REFERENCES menu_items(id)
    );
    CREATE TABLE IF NOT EXISTS bills(
      id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER UNIQUE,
      subtotal REAL NOT NULL, tax_amount REAL NOT NULL, discount_amount REAL DEFAULT 0,
      total_amount REAL NOT NULL, status TEXT DEFAULT 'unpaid',
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(order_id) REFERENCES food_orders(id)
    );
    CREATE TABLE IF NOT EXISTS payments(
      id INTEGER PRIMARY KEY AUTOINCREMENT, bill_id INTEGER, amount REAL NOT NULL,
      method TEXT NOT NULL, status TEXT DEFAULT 'completed',
      transaction_ref TEXT, paid_at TEXT DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(bill_id) REFERENCES bills(id)
    );
    CREATE TABLE IF NOT EXISTS employees(
      id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER UNIQUE, full_name TEXT NOT NULL,
      role_title TEXT NOT NULL, phone TEXT, salary REAL DEFAULT 0, hire_date TEXT,
      FOREIGN KEY(user_id) REFERENCES users(id)
    );
    """)
    # Seed preview data once.
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        demo_users = [
          ("admin","Admin@12345","admin","Bhoj Administrator"),
          ("manager","Manager@12345","manager","Restaurant Manager"),
          ("kitchen","Kitchen@12345","kitchen","Kitchen Staff"),
          ("cashier","Cashier@12345","cashier","Cashier Demo"),
          ("reception","Reception@12345","receptionist","Reception Desk"),
          ("customer","Customer@12345","customer","Demo Customer")
        ]
        for u,p,r,n in demo_users:
            conn.execute("INSERT INTO users(username,password_hash,role,full_name,email) VALUES(?,?,?,?,?)",
                         (u,generate_password_hash(p),r,n,f"{u}@bhoj.local"))
        conn.execute("INSERT INTO customers(user_id,full_name,phone,email) VALUES(6,'Demo Customer','9000000000','customer@bhoj.local')")
        for i in range(1,9):
            conn.execute("INSERT INTO dining_tables(table_number,capacity,area,status) VALUES(?,?,?,?)",
                         (f"T{i:02d}", 2 if i<=3 else 4 if i<=6 else 6, "Garden" if i>=7 else "Main Hall","available"))
        for name in ["Starters","Bengali Classics","Main Course","Breads & Rice","Desserts","Beverages"]:
            conn.execute("INSERT INTO food_categories(name) VALUES(?)",(name,))
        menu = [
          (1,"Kolkata Fish Fry","Crisp crumb-coated fish fillet with kasundi",260,0),
          (1,"Mochar Chop","Banana blossom croquettes",160,1),
          (2,"Shorshe Ilish","Hilsa in mustard gravy",480,0),
          (2,"Kosha Mangsho","Slow-cooked Bengali mutton curry",390,0),
          (2,"Chingri Malai Curry","Prawns in coconut milk gravy",420,0),
          (3,"Chicken Chaap","Rich Kolkata-style chicken chaap",320,0),
          (4,"Basanti Pulao","Fragrant sweet yellow rice",190,1),
          (4,"Luchi (4 pcs)","Fluffy fried Bengali bread",80,1),
          (5,"Baked Rosogolla","Warm baked Bengali cottage-cheese dessert",120,1),
          (5,"Mishti Doi","Traditional sweet yogurt",90,1),
          (6,"Aam Panna","Refreshing raw mango cooler",85,1),
          (6,"Darjeeling Tea","Light aromatic tea",60,1)
        ]
        for c,n,d,p,v in menu:
            conn.execute("INSERT INTO menu_items(category_id,name,description,price,is_vegetarian) VALUES(?,?,?,?,?)",(c,n,d,p,v))
        for username,role,title in [("manager","manager","Manager"),("kitchen","kitchen","Kitchen Staff"),("cashier","cashier","Cashier"),("reception","receptionist","Receptionist")]:
            uid=conn.execute("SELECT id FROM users WHERE username=?",(username,)).fetchone()[0]
            conn.execute("INSERT INTO employees(user_id,full_name,role_title,phone,salary) VALUES(?,?,?,?,?)",(uid,title,title,"9000000000",0))
        conn.commit()
    conn.close()
