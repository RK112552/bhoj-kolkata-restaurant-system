# Bhoj Kolkata Restaurant Management System

**Project:** Restaurant Management System  
**Course:** BTY39105 DBMS Lab PBL — Brainware University  
**Main technologies:** Python, Flask, MySQL, HTML, CSS, JavaScript

This project is a web application for managing restaurant activities such as menu items, customer reservations, food orders, kitchen order status, bills/payments, employees, and management dashboards.

> This is an academic/demo project. Use fictional data. Change demo passwords and the Flask secret before putting the application on a public server.

---

## 1. What you need

Install these before running the project:

- Windows 10 or Windows 11
- Python 3.10 or newer
- MySQL Server 8.0 or newer
- MySQL Workbench (helpful for running the SQL files)
- Visual Studio Code (recommended)
- A web browser

Check Python and MySQL from the VS Code terminal:

```powershell
python --version
mysql --version
```

If `mysql --version` is not recognised, make sure the MySQL Server `bin` folder is added to Windows `Path`, then completely close and reopen VS Code.

---

## 2. Open the project

1. Extract the project ZIP to a folder, for example `C:\Projects\bhoj_kolkata_restaurant_system`.
2. Open VS Code.
3. Select **File → Open Folder** and choose the extracted `bhoj_kolkata_restaurant_system` folder.
4. Open **Terminal → New Terminal**.
5. Check that the terminal is at the project root. The `dir` command should show files/folders such as `README.md`, `requirements.txt`, `database`, and `src`.

Run the commands in this guide from the project root unless a step says otherwise.

---

## 3. Create and activate a Python virtual environment

In the VS Code PowerShell terminal, run:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use this command for the current terminal session only, then try activation again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

When activation works, the terminal prompt usually starts with `(.venv)`.

Install the required Python packages:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you have already installed the requirements successfully, you can skip this section.

---

## 4. Configure the `.env` file

The `.env` file stores local settings for Flask and the database. It should be in the **project root**, next to `README.md` and `requirements.txt`.

If you do not have a `.env` file but `.env.example` exists, create it with:

```powershell
Copy-Item .env.example .env
```

If `.env` already exists, open it in VS Code and edit it instead of copying over it.

A MySQL configuration for this project looks like this:

```dotenv
FLASK_SECRET_KEY=put-a-long-random-secret-here
DB_MODE=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=bhoj_kolkata
DB_USER=root
DB_PASSWORD=your_actual_mysql_password
```

Important:

- `DB_NAME` should be `bhoj_kolkata` because `database/schema.sql` creates and uses that database.
- `DB_USER` must be the MySQL username you actually use. The example above uses `root`; if you use another MySQL account, put that username here.
- `DB_PASSWORD` must be that user's real MySQL password. Replace the example text; do not include angle brackets.
- If your MySQL root account has no password, leave `DB_PASSWORD=` empty. Do this only if that matches your local MySQL setup.
- `FLASK_SECRET_KEY` should be a long, private random value. Do not post your `.env` file or password publicly.
- Do not add spaces around the `=` sign.
- Keep `DB_MODE=mysql` for the DBMS project. SQLite is only an optional preview mode and does not replace the MySQL SQL-script demonstration.

The project database account must have permission to read and write the `bhoj_kolkata` database. If you use a separate account such as `bhoj_app`, create that account in MySQL and grant it access to this database, then use its credentials in `.env`.
--sql
CREATE USER 'bhoj_app'@'localhost'
IDENTIFIED BY 'Choose_A_Strong_Password_123!';

GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE, SHOW VIEW
ON bhoj_kolkata.*
TO 'bhoj_app'@'localhost';
--
If MySQL says the account already exists, don't run CREATE USER again. Use ALTER USER to set its password, then run the GRANT statement.
--sql
ALTER USER 'bhoj_app'@'localhost'
IDENTIFIED BY 'Choose_A_Strong_Password_123!';
--


These permissions allow the account to read records, insert new records, update and delete records, execute stored routines, and access database views. They do not grant permission to drop tables or change the schema.
Step 3 — Verify the permissions
Run this query in Workbench:
--sql
SHOW GRANTS FOR 'bhoj_app'@'localhost';
--

You should see a grant that includes permissions on bhoj_kolkata.*.
---

## 5. Set up the MySQL database

If you have already run all the SQL files successfully in MySQL Workbench, go to Section 6.

Otherwise:

1. Open MySQL Workbench and connect to your local MySQL Server.
2. Select **File → Open SQL Script**.
3. Open and run the following files from the project's `database` folder, in this exact order:

   1. `database/schema.sql`
   2. `database/insert_data.sql`
   3. `database/views.sql`
   4. `database/functions.sql`
   5. `database/procedures.sql`
   6. `database/triggers.sql`
   7. `database/queries.sql` — use this last file to run sample/report queries.

4. After running `schema.sql`, the database should be named `bhoj_kolkata`.
5. To confirm the database exists, run this in a Workbench query tab:

```sql
SHOW DATABASES;
USE bhoj_kolkata;
SHOW TABLES;
```

`queries.sql` is for demonstrating queries and reports; it is not required to create the tables. Run the other SQL files in the order shown above.

---

## 6. Create the demo login accounts

Make sure your `.env` file has the correct MySQL connection details before running the seeder.

In the VS Code terminal, from the project root, run:

```powershell
python src/backend/seed_demo_users.py
```

If the connection settings are correct, the script creates the demo users and stores password hashes in the database. If an account already exists, the script skips it.

### Demo logins

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `Admin@12345` |
| Manager | `manager` | `Manager@12345` |
| Kitchen staff | `kitchen` | `Kitchen@12345` |
| Cashier | `cashier` | `Cashier@12345` |
| Reception | `reception` | `Reception@12345` |
| Customer | `customer` | `Customer@12345` |

These are public demo credentials for local testing only. Do not use them for a real restaurant or public deployment.

---

## 7. Start the website

From the project root, with the virtual environment activated, run:

```powershell
python src/backend/app.py
```

Wait until the terminal indicates that the local Flask server is running. Then open this address in your browser:

**http://127.0.0.1:5000**

Log in using one of the demo accounts above.

Keep the terminal window open while using the site. To stop the server, return to the terminal and press **Ctrl + C**.

If you change Python code, restart the server if the changes do not appear. Do not share screenshots that expose passwords or private data.

---

## 8. Common problems and fixes

### A. `mysql` is not recognised

Windows cannot find the MySQL command. Add the MySQL Server `bin` folder to the Windows `Path`, then fully restart VS Code. Test with:

```powershell
mysql --version
```

### B. `ModuleNotFoundError` when starting the app

Activate `.venv` and install requirements again:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### C. `Access denied for user`

The username or password in `.env` is incorrect, or that MySQL account does not have the required database permissions. Check the credentials in MySQL Workbench and update `.env`. Do not paste your password into chat or a public issue.

### D. `Unknown database 'bhoj_kolkata'`

Open `database/schema.sql` in MySQL Workbench and run it. Confirm that `.env` contains `DB_NAME=bhoj_kolkata`.

### E. `Can't connect to MySQL server` / connection refused

Confirm that the MySQL Server service is running, that `DB_HOST=127.0.0.1`, and that `DB_PORT=3306` matches your installation. MySQL Workbench opening successfully does not always mean the server is currently running.

### F. `mysql` works in Windows but not in VS Code

Completely close all VS Code windows and reopen VS Code after changing Windows `Path`. Then open a new terminal and try `mysql --version` again.

### G. The website says `Internal Server Error`

Read the latest error printed in the VS Code terminal. It often points to a database setting, missing table, or Python dependency. Fix the specific error shown rather than changing random settings.

### H. Port 5000 is already in use

Close the other local app using port 5000, or set a different `PORT` value in `.env` and open the matching local URL. For example, if `PORT=5001`, open `http://127.0.0.1:5001`.

---

## 9. Project folder guide

```text
bhoj_kolkata_restaurant_system/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── run_windows.bat
├── run_linux_mac.sh
├── database/
│   ├── schema.sql
│   ├── insert_data.sql
│   ├── views.sql
│   ├── functions.sql
│   ├── procedures.sql
│   ├── triggers.sql
│   └── queries.sql
├── src/
│   ├── backend/
│   │   ├── app.py
│   │   ├── db.py
│   │   └── seed_demo_users.py
│   └── frontend/
│       ├── templates/
│       └── static/
├── docs/
├── deployment/
└── tests/
```

- `database/` — database creation, sample data, views, functions, procedures, triggers, and demo queries.
- `src/backend/app.py` — Flask web application.
- `src/backend/db.py` — database connection and database helper functions.
- `src/backend/seed_demo_users.py` — creates the demo login accounts.
- `src/frontend/templates/` — HTML templates for website pages.
- `src/frontend/static/` — CSS and JavaScript files.
- `docs/` — project report, ER diagram notes, relational schema, data dictionary, normalization, and requirements.
- `tests/` — test plan and manual testing guidance.

---

## 10. Application roles

- **Administrator:** overall application management and access to administrative functions.
- **Manager:** restaurant operations and management views.
- **Kitchen:** views active orders and updates kitchen status.
- **Cashier:** handles billing/payment demo functions.
- **Reception:** handles reservations and table availability.
- **Customer:** browses the menu and uses customer reservation/order functions.

Access available to each role is controlled by the application. The exact pages/actions depend on the implemented features.

---

## 11. DBMS features demonstrated

The SQL files demonstrate relational database concepts, including:

- Tables, primary keys, foreign keys, and constraints
- Sample records and joins/queries
- Views
- Stored functions
- Stored procedures
- Triggers
- Reporting/demo queries
- Database-driven application operations

Refer to the files in `docs/` for the project report, ER diagram notes, relational schema, normalization, and data dictionary.

---

## 12. Security notes

- Never upload `.env` or share its contents publicly.
- Change every demo password before any public deployment.
- Generate a unique secret key for Flask.
- Use HTTPS and a production WSGI server for public deployment; Flask's local development server is for development/testing.
- Do not collect or store real payment-card numbers or CVV values in this academic demo.
- Use fictional customer, employee, and transaction data.
- Restrict MySQL user permissions to only what the application needs.

---

## 13. Checklist before submission

- [ ] Project runs locally from VS Code.
- [ ] MySQL database and all required SQL scripts have been tested.
- [ ] Login has been tested for the relevant roles.
- [ ] Screenshots have been captured for the report/presentation.
- [ ] ER diagram, relational schema, normalization, and data dictionary are reviewed.
- [ ] Team members, team number, and contribution details are accurate.
- [ ] GitHub repository and deployment details are added if required.
- [ ] Demo credentials and limitations are explained in the presentation.

---

**For local development:** configure `.env` → run the SQL scripts → run `python src/backend/seed_demo_users.py` → run `python src/backend/app.py` → open `http://127.0.0.1:5000`.
