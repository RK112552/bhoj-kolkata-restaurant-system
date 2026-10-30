# 🍽️ Bhoj Kolkata – Restaurant Management System

A web-based Restaurant Management System developed using **Python Flask, MySQL, HTML, CSS, and JavaScript** as a DBMS Lab Project at Brainware University.

This project helps manage restaurant operations such as orders, payments, food items, customers, and sales records through a web-based interface.

---

## 1. About the Project

**Bhoj Kolkata** is a restaurant management application designed to make restaurant operations easier and more organized.

Instead of managing restaurant information manually, users can manage important activities through a single web application.

### Main Objectives

- Manage restaurant information digitally.
- Store and organize data using MySQL.
- Manage food orders and order statuses.
- Maintain payment records.
- Support different user roles.
- Generate daily sales information.
- Demonstrate important DBMS concepts using a real-world project.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| HTML | Webpage structure |
| CSS | Website design |
| JavaScript | Frontend interactions |
| SQL | Database queries and operations |

---

## 3. Project Features

The system is designed around the following restaurant management activities:

- **User Management:** Different roles for managing restaurant operations.
- **Food Management:** Store and manage food-related information.
- **Order Management:** Maintain customer orders and their statuses.
- **Payment Management:** Store payment details and payment status.
- **Sales Management:** Retrieve daily sales information.
- **Database Management:** Store information in a structured MySQL database.

### Order Status Options

The order management procedure supports:

1. Placed
2. Confirmed
3. Preparing
4. Ready
5. Served
6. Cancelled

---

## 4. Project Folder Structure

The project is organized into the following folders:

```text
bhoj_kolkata_restaurant_system/
│
├── database/
│   ├── schema.sql
│   ├── insert_data.sql
│   ├── views.sql
│   ├── functions.sql
│   ├── procedures.sql
│   └── triggers.sql
│
├── src/
│   └── backend/
│       ├── app.py
│       └── seed_demo_users.py
│
├── .env
├── requirements.txt
├── bhoj_setup_all.py
└── README.md
```

**Note:** This is the main project structure. Additional frontend templates, static files, and supporting files may also be present.

---

## 5. Software Requirements

Before running the project, install the following:

1. Python 3
2. MySQL Server
3. MySQL Workbench (recommended)
4. Visual Studio Code (recommended)
5. A modern web browser

You should also have access to a MySQL administrator account for the initial database setup.

---

## 6. Installation Guide for Beginners

Follow these steps carefully.

### Step 1: Download or Extract the Project

Place the project folder somewhere easy to access.

For example:

```text
C:\Users\YourName\Documents\bhoj_kolkata_restaurant_system
```

Open this folder in Visual Studio Code.

### Step 2: Install Python

Download Python from:

https://www.python.org/downloads/

Check whether Python is installed.

Open Command Prompt and enter:

```bash
py --version
```

If the version appears, Python is installed successfully.

### Step 3: Install MySQL

Download MySQL Community Server:

https://dev.mysql.com/downloads/mysql/

You can also install MySQL Workbench:

https://dev.mysql.com/downloads/workbench/

Remember your MySQL administrator username and password. You will need them during setup.

### Step 4: Configure the Environment File

Open the `.env` file in your project folder.

Add or update the following configuration:

```env
FLASK_SECRET_KEY=your_long_random_secret

DB_MODE=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=bhoj_kolkata
DB_USER=bhoj_app
DB_PASSWORD=your_actual_mysql_password
```

Replace `your_actual_mysql_password` with the password configured for the `bhoj_app` MySQL account.

**Important:** Never share your actual database password or upload your `.env` file publicly.

### Step 5: Install Project Dependencies

Open the terminal in your project folder.

Run:

```bash
py -m pip install -r requirements.txt
```

This installs the Python libraries required by the project.

### Step 6: Run the Setup Script

Run:

```bash
py bhoj_setup_all.py
```

The setup script is designed to:

1. Install or check the required Python packages.
2. Connect to MySQL using administrator credentials.
3. Create the project database.
4. Configure the application database user.
5. Execute the SQL database scripts.
6. Run the demo user seeder.
7. Start the Flask application.

Follow the instructions shown in the terminal.

**Important:** The initial setup requires appropriate MySQL administrator privileges. Do not grant unnecessary administrator privileges to the application account.

---

## 7. Database Structure and SQL Files

The project uses six SQL files to organize database operations.

| SQL File | Purpose |
|---|---|
| `schema.sql` | Creates database tables and their structure. |
| `insert_data.sql` | Inserts initial sample records. |
| `views.sql` | Creates database views. |
| `functions.sql` | Defines reusable SQL functions. |
| `procedures.sql` | Defines stored procedures. |
| `triggers.sql` | Defines database triggers. |

### Stored Function

The project includes:

`fn_bill_total()`

It calculates the final bill amount using subtotal, tax rate, and discount.

Example:

```sql
SELECT fn_bill_total(1000.00, 5.00, 50.00);
```

Expected result:

```text
1000.00
```

### Stored Procedures

The project includes:

**1. sp_update_order_status**

Updates the status of a particular food order.

Example:

```sql
CALL sp_update_order_status(1, 'preparing');
```

**2. sp_daily_sales**

Retrieves daily payment information and total revenue.

Example:

```sql
CALL sp_daily_sales(CURDATE());
```

### Database Views and Triggers

- Views provide reusable ways to retrieve selected database information.
- Triggers execute automatically when their configured database events occur.

These features demonstrate how database logic can be managed directly inside MySQL.

---

## 8. Running the Application

After successful setup, the Flask application runs locally.

Open your browser and visit:

**http://127.0.0.1:5000**

If the browser does not open automatically, enter the URL manually.

To start the application manually, open the project terminal and run:

```bash
py src/backend/app.py
```

Keep the terminal open while using the application.

To stop the Flask server, press:

```text
CTRL + C
```

---

## 9. Demo User Accounts

The project includes demo accounts for testing different user roles.

| Username | Password | Role |
|---|---|---|
| admin | Admin@12345 | Admin |
| manager | Manager@12345 | Manager |
| kitchen | Kitchen@12345 | Kitchen |
| cashier | Cashier@12345 | Cashier |
| reception | Reception@12345 | Reception |
| customer | Customer@12345 | Customer |

**Security Warning:** These are sample demonstration credentials, not production credentials. Change them before deploying the application or exposing it to other users.

---

## 10. Common Errors and Solutions

### Error 1: Python is not recognized

Try:

```bash
py --version
```

If this works, use `py` instead of `python` in your commands.

### Error 2: MySQL Access Denied

Check:

- MySQL Server is running.
- Database username is correct.
- Database password is correct.
- The application account has the required database permissions.

### Error 3: Procedure Already Exists

MySQL does not support `CREATE OR REPLACE PROCEDURE`.

If a procedure already exists, creating it again may produce error 1304.

Check existing procedures using:

```sql
SELECT ROUTINE_NAME
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = 'bhoj_kolkata';
```

Do not drop existing procedures without checking their definitions and permissions.

### Error 4: Binary Logging and Trigger Creation

You may encounter error 1419 when creating triggers or stored routines on a MySQL server with binary logging enabled.

In an appropriate local development environment, a MySQL administrator can check:

```sql
SHOW VARIABLES LIKE 'log_bin_trust_function_creators';
```

If necessary and permitted by the server administrator, the setting can be changed:

```sql
SET GLOBAL log_bin_trust_function_creators = 1;
```

This setting relaxes restrictions on stored routine and trigger creators. Use it only when appropriate for your environment.

### Error 5: Port 5000 Already in Use

Another application may already be using port 5000.

Stop the other Flask process or configure the application to use another available port.

### Error 6: Database Connection Failed

Check your `.env` file and verify the following:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

Also make sure MySQL Server is running.

---

## 11. DBMS Concepts Demonstrated

This project demonstrates several important Database Management System concepts:

1. **DDL (Data Definition Language):** Creating and managing database structures.
2. **DML (Data Manipulation Language):** Inserting and updating records.
3. **Primary Keys:** Uniquely identifying database records.
4. **Foreign Keys:** Establishing relationships between tables.
5. **Constraints:** Maintaining data integrity.
6. **Joins:** Retrieving related information from multiple tables.
7. **Views:** Creating reusable database queries.
8. **Stored Functions:** Performing reusable calculations.
9. **Stored Procedures:** Executing reusable database operations.
10. **Triggers:** Automating database actions.
11. **Transactions:** Managing database operations reliably, where implemented.

---

## 12. Future Improvements

Possible future enhancements include:

- Online food ordering.
- Online payment gateway integration.
- Restaurant inventory management.
- Customer feedback and ratings.
- Advanced sales reports.
- Improved dashboard analytics.
- Mobile-friendly interface.

---

## 13. Project Information

**Project Name:** Bhoj Kolkata – Restaurant Management System

**Project Type:** DBMS Lab Project / Project-Based Learning (PBL)

**University:** Brainware University

**Department:** Computer Science and Engineering

**Technology Stack:** Python, Flask, MySQL, HTML, CSS, JavaScript

---

## 14. Conclusion

Bhoj Kolkata is a web-based restaurant management project developed to demonstrate the practical implementation of Database Management System concepts.

It combines a Flask-based backend with a MySQL database to organize restaurant-related information and operations.

The project provides practical experience in database design, SQL queries, stored procedures, functions, triggers, and web application development.

**Thank you for using Bhoj Kolkata!** 🍽️