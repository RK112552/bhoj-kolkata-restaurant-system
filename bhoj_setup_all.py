
"""
BHOJ KOLKATA RESTAURANT MANAGEMENT SYSTEM
Complete Setup and Launcher

Run:
    py bhoj_setup_all.py

Place this file in the project root, beside .env and requirements.txt.
"""

import os
import re
import sys
import time
import socket
import getpass
import subprocess
import webbrowser
from pathlib import Path


# ==========================================================
# PROJECT CONFIGURATION
# ==========================================================

ROOT = Path(__file__).resolve().parent

ENV_FILE = ROOT / ".env"
REQUIREMENTS_FILE = ROOT / "requirements.txt"

DATABASE_DIR = ROOT / "database"
BACKEND_DIR = ROOT / "src" / "backend"

APP_FILE = BACKEND_DIR / "app.py"
SEED_FILE = BACKEND_DIR / "seed_demo_users.py"

SQL_FILES = [
    "schema.sql",
    "insert_data.sql",
    "views.sql",
    "functions.sql",
    "procedures.sql",
    "triggers.sql",
]

WEBSITE_URL = "http://127.0.0.1:5000"
PORT = 5000


# ==========================================================
# MESSAGES
# ==========================================================

def heading(message):
    print("\n" + "=" * 65)
    print(message)
    print("=" * 65)


def success(message):
    print("[SUCCESS]", message)


def warning(message):
    print("[WARNING]", message)


def fail(message):
    raise RuntimeError(message)


# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

def load_environment():

    heading("STEP 1 - LOADING ENVIRONMENT")

    if not ENV_FILE.exists():
        fail(".env file not found in project root.")

    config = {}

    for line in ENV_FILE.read_text(
        encoding="utf-8-sig"
    ).splitlines():

        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)

        key = key.strip()
        value = value.strip().strip('"').strip("'")

        config[key] = value
        os.environ[key] = value

    required = [
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD",
    ]

    for key in required:
        if not config.get(key):
            fail(f"{key} is missing in .env")

    if config.get("DB_MODE", "mysql").lower() != "mysql":
        fail("DB_MODE must be mysql.")

    config["DB_HOST"] = config.get(
        "DB_HOST", "127.0.0.1"
    )

    config["DB_PORT"] = int(
        config.get("DB_PORT", "3306")
    )

    if not re.fullmatch(r"[A-Za-z0-9_]+", config["DB_NAME"]):
        fail("Invalid database name.")

    if not re.fullmatch(r"[A-Za-z0-9_]+", config["DB_USER"]):
        fail("Invalid database username.")

    success("Environment loaded.")

    return config


# ==========================================================
# CHECK PROJECT FILES
# ==========================================================

def check_project():

    heading("STEP 2 - CHECKING PROJECT FILES")

    required = [
        DATABASE_DIR,
        BACKEND_DIR,
        APP_FILE,
        ENV_FILE,
    ]

    for path in required:
        if not path.exists():
            fail(f"Missing project item: {path}")

    for filename in SQL_FILES:
        path = DATABASE_DIR / filename

        if not path.exists():
            fail(f"Missing SQL file: {filename}")

    success("Project files verified.")


# ==========================================================
# INSTALL PYTHON PACKAGES
# ==========================================================

def install_packages():

    heading("STEP 3 - INSTALLING PYTHON PACKAGES")

    if REQUIREMENTS_FILE.exists():

        command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(REQUIREMENTS_FILE),
        ]

    else:

        command = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "Flask",
            "mysql-connector-python",
            "python-dotenv",
        ]

    result = subprocess.run(command, cwd=ROOT)

    if result.returncode != 0:
        fail("Python package installation failed.")

    success("Python packages installed.")


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

def get_admin_connection(config):

    import mysql.connector

    heading("STEP 4 - MYSQL ADMIN LOGIN")

    print("Enter your MySQL administrator account.")
    print("Usually the username is root.")
    print("Your password will not be displayed.")

    username = (
        input("MySQL username [root]: ").strip()
        or "root"
    )

    password = getpass.getpass("MySQL password: ")

    connection = mysql.connector.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        user=username,
        password=password,
        autocommit=True,
    )

    success("MySQL administrator connected.")

    return connection


def get_app_connection(config):

    import mysql.connector

    return mysql.connector.connect(
        host=config["DB_HOST"],
        port=config["DB_PORT"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_NAME"],
        autocommit=True,
    )


# ==========================================================
# DATABASE SETUP
# ==========================================================

def setup_database(config):

    heading("STEP 5 - CREATING DATABASE")

    connection = get_admin_connection(config)
    cursor = connection.cursor()

    database = config["DB_NAME"]
    username = config["DB_USER"]

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{database}` "
        "CHARACTER SET utf8mb4 "
        "COLLATE utf8mb4_unicode_ci"
    )

    # Grant only database-level privileges.
    # No SYSTEM_USER or global privileges are granted.
    for account_host in ["localhost", "127.0.0.1"]:

        try:
            cursor.execute(
                f"GRANT ALL PRIVILEGES ON `{database}`.* "
                f"TO '{username}'@'{account_host}'"
            )

        except Exception as exc:
            warning(
                f"Could not grant access to "
                f"{username}@{account_host}: {exc}"
            )

    cursor.close()
    connection.close()

    success("Database creation checked.")


# ==========================================================
# SQL DEFINER CLEANUP
# ==========================================================

def remove_definer(sql):

    pattern = (
        r"\bDEFINER\s*=\s*"
        r"(?:CURRENT_USER(?:\(\))?|"
        r"(?:'[^']*'|`[^`]*`|[A-Za-z0-9_.%-]+)"
        r"(?:\s*@\s*"
        r"(?:'[^']*'|`[^`]*`|[A-Za-z0-9_.%-]+))?)"
    )

    return re.sub(
        pattern,
        "",
        sql,
        flags=re.IGNORECASE
    )


# ==========================================================
# SQL STATEMENT SPLITTER
# ==========================================================

def split_sql(sql):

    statements = []
    buffer = []

    delimiter = ";"
    quote = None
    escaped = False

    i = 0

    while i < len(sql):

        if quote is None and (
            i == 0 or sql[i - 1] == "\n"
        ):

            end = sql.find("\n", i)

            if end == -1:
                end = len(sql)

            line = sql[i:end].strip()

            if line.upper().startswith("DELIMITER "):

                delimiter = line.split(None, 1)[1].strip()
                i = end + 1
                continue

        char = sql[i]
        nxt = sql[i + 1] if i + 1 < len(sql) else ""

        if quote is None:

            if char == "-" and nxt == "-":
                end = sql.find("\n", i)
                if end == -1:
                    break
                i = end
                continue

            if char == "#":
                end = sql.find("\n", i)
                if end == -1:
                    break
                i = end
                continue

            if char == "/" and nxt == "*":
                end = sql.find("*/", i + 2)
                if end == -1:
                    fail("Unclosed SQL block comment.")
                i = end + 2
                continue

        if quote is not None:

            buffer.append(char)

            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                if nxt == quote:
                    buffer.append(nxt)
                    i += 1
                else:
                    quote = None

            i += 1
            continue

        if char in ("'", '"', "`"):
            quote = char
            buffer.append(char)
            i += 1
            continue

        if sql.startswith(delimiter, i):

            statement = "".join(buffer).strip()

            if statement:
                statements.append(statement)

            buffer = []
            i += len(delimiter)
            continue

        buffer.append(char)
        i += 1

    remaining = "".join(buffer).strip()

    if remaining:
        statements.append(remaining)

    return statements


# ==========================================================
# CHECK EXISTING FUNCTION
# ==========================================================

def function_exists(connection, name):

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA = DATABASE()
          AND ROUTINE_NAME = %s
          AND ROUTINE_TYPE = 'FUNCTION'
        """,
        (name,)
    )

    result = cursor.fetchone()[0]

    cursor.close()

    return result > 0


# ==========================================================
# EXECUTE SQL FILE
# ==========================================================

def execute_sql_file(connection, filename):

    heading("EXECUTING " + filename)

    path = DATABASE_DIR / filename

    sql = path.read_text(
        encoding="utf-8-sig"
    )

    # Remove explicit DEFINER declarations.
    sql = remove_definer(sql)

    # Preserve the existing bill function to avoid
    # attempting to drop a protected stored function.
    if filename == "functions.sql":

        if function_exists(connection, "fn_bill_total"):

            success(
                "fn_bill_total already exists. "
                "Skipping functions.sql."
            )

            return

        # Remove DROP FUNCTION statements from the file.
        sql = re.sub(
            r"DROP\s+FUNCTION\s+IF\s+EXISTS\s+"
            r"(?:`[^`]+`\.)?`?fn_bill_total`?\s*;",
            "",
            sql,
            flags=re.IGNORECASE
        )

    statements = split_sql(sql)

    cursor = connection.cursor()

    try:

        for number, statement in enumerate(statements, 1):

            try:

                cursor.execute(statement)

                if cursor.with_rows:
                    cursor.fetchall()

                print(f"[OK] Statement {number}")

            except Exception as exc:

                raise RuntimeError(
                    f"{filename}, statement {number}: {exc}"
                ) from exc

    finally:
        cursor.close()

    success(filename + " completed.")


# ==========================================================
# EXECUTE ALL DATABASE FILES
# ==========================================================

def execute_all_sql(config):

    heading("STEP 6 - EXECUTING DATABASE FILES")

    connection = get_app_connection(config)

    try:

        for filename in SQL_FILES:
            execute_sql_file(connection, filename)

    finally:
        connection.close()

    success("Database SQL processing completed.")


# ==========================================================
# DEMO USERS
# ==========================================================

def create_demo_users():

    heading("STEP 7 - CREATING DEMO USERS")

    if not SEED_FILE.exists():

        warning("Demo user seeder not found. Skipping.")
        return

    result = subprocess.run(
        [sys.executable, str(SEED_FILE)],
        cwd=ROOT
    )

    if result.returncode != 0:
        fail("Demo user seeder failed.")

    success("Demo users processed.")


# ==========================================================
# CHECK PORT
# ==========================================================

def port_available():

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as sock:

        return sock.connect_ex(
            ("127.0.0.1", PORT)
        ) != 0


# ==========================================================
# START WEBSITE
# ==========================================================

def start_website():

    heading("STEP 8 - STARTING FLASK WEBSITE")

    if not APP_FILE.exists():
        fail("Flask app.py not found.")

    if not port_available():

        warning("Port 5000 is already in use.")

        webbrowser.open(WEBSITE_URL)
        return

    process = subprocess.Popen(
        [sys.executable, str(APP_FILE)],
        cwd=ROOT
    )

    time.sleep(3)

    if process.poll() is not None:
        fail("Flask stopped during startup. Check its error.")

    success("Flask server started.")

    print("\nWebsite:", WEBSITE_URL)

    webbrowser.open(WEBSITE_URL)

    print("\nPress CTRL+C to stop Flask.")

    try:
        process.wait()

    except KeyboardInterrupt:

        print("\nStopping Flask...")

        process.terminate()

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

        success("Flask stopped.")


# ==========================================================
# MAIN
# ==========================================================

def main():

    heading(
        "BHOJ KOLKATA RESTAURANT MANAGEMENT SYSTEM"
    )

    print("Complete Automatic Setup and Launcher")
    print("Brainware University - DBMS Lab PBL")

    try:

        check_project()

        config = load_environment()

        install_packages()

        setup_database(config)

        execute_all_sql(config)

        create_demo_users()

        start_website()

    except KeyboardInterrupt:

        print("\nSetup interrupted.")

    except Exception as exc:

        print("\n[ERROR]", exc)

        print(
            "\nSetup stopped. "
            "Check the error above before retrying."
        )

    finally:

        print("\n" + "=" * 65)
        print("BHOJ KOLKATA SETUP PROCESS FINISHED")
        print("=" * 65)


if __name__ == "__main__":
    main()
