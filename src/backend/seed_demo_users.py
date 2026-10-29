"""Create fictional MySQL demo users with hashed passwords.
Run from the project root after database/schema.sql:
    python src/backend/seed_demo_users.py
Change passwords before any public deployment.
"""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from db import get_connection, execute, is_sqlite

load_dotenv()
if os.getenv("DB_MODE", "mysql").lower() == "sqlite":
    print("SQLite preview users are seeded automatically on first app run.")
    raise SystemExit(0)

accounts = [
    ("admin", "Admin@12345", "admin", "Bhoj Administrator", "admin@bhoj.local", "9000000001"),
    ("manager", "Manager@12345", "manager", "Restaurant Manager", "manager@bhoj.local", "9000000002"),
    ("kitchen", "Kitchen@12345", "kitchen", "Kitchen Staff", "kitchen@bhoj.local", "9000000003"),
    ("cashier", "Cashier@12345", "cashier", "Cashier Demo", "cashier@bhoj.local", "9000000004"),
    ("reception", "Reception@12345", "receptionist", "Reception Desk", "reception@bhoj.local", "9000000005"),
    ("customer", "Customer@12345", "customer", "Demo Customer", "customer@bhoj.local", "9000000006"),
]
conn = get_connection()
try:
    for username, password, role, name, email, phone in accounts:
        cur = execute(conn, "SELECT id FROM users WHERE username=%s", (username,))
        existing = cur.fetchone()
        if existing:
            print(f"Skipped existing user: {username}")
            continue
        cur = execute(conn,
            "INSERT INTO users(username,password_hash,role,full_name,email,phone,active) VALUES(%s,%s,%s,%s,%s,%s,TRUE)",
            (username, generate_password_hash(password), role, name, email, phone))
        uid = cur.lastrowid
        if role == "customer":
            execute(conn, "INSERT INTO customers(user_id,full_name,phone,email) VALUES(%s,%s,%s,%s)", (uid,name,phone,email))
        elif role != "admin":
            execute(conn, "INSERT INTO employees(user_id,full_name,role_title,phone,salary,hire_date) VALUES(%s,%s,%s,%s,0,CURDATE())",
                    (uid,name,role.title(),phone))
        print(f"Created demo account: {username} ({role})")
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
print("Demo accounts ready. Change these passwords before public deployment.")
