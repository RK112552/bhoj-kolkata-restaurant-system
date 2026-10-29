# Project Report: Bhoj Kolkata Restaurant Management System

## 1. Introduction
Bhoj Kolkata is a database-driven web application for centralizing restaurant operations. It covers customer records, table reservations, menu items, food orders, kitchen status, billing, payments and employees. Customers can browse the public menu and submit reservation requests. Signed-in customers can place demo takeaway orders and view only their own account activity. Staff use role-specific operational screens.

## 2. Problem statement
A restaurant may maintain reservations, orders, bills, payments and employee details in separate records. This can lead to duplicate work, inconsistent order status, delayed billing and poor reporting. The proposed system centralizes these records in a relational database and connects them to a web interface.

## 3. Objectives
1. Maintain restaurant data in a central relational database.
2. Provide customer menu browsing, reservations and order history.
3. Support kitchen order-status updates and cashier payment recording.
4. Restrict management features using role-based access control.
5. Produce database-derived operational and sales reports.
6. Demonstrate relational modelling, normalization, SQL queries, views, indexes, stored procedures, a function, triggers and transaction handling.
7. Maintain reproducible code and SQL in GitHub and deploy a live demonstration.

## 4. Scope and roles
- Administrator: full management access including staff login activation.
- Manager: menu, reservations, orders and reports; cannot activate/deactivate staff accounts.
- Kitchen: active order queue and order status updates.
- Cashier: bill/payment status recording; payment is simulated.
- Receptionist: reservations and table assignment.
- Customer: public menu, reservation request, own orders and reservations. No revenue dashboard or staff/customer records.

## 5. Technology used
- HTML5 for page structure.
- CSS3 for responsive design and visual styling.
- JavaScript for navigation and small client-side interactions.
- Python Flask for routes, sessions, validation and authorization.
- MySQL 8 / InnoDB for persistent data and advanced SQL.
- Git and GitHub for source control.
- Optional SQLite preview mode for a quick local UI trial; MySQL is the intended PBL DBMS.

## 6. Database design
The schema includes 11 related tables: USERS, CUSTOMERS, EMPLOYEES, DINING_TABLES, FOOD_CATEGORIES, MENU_ITEMS, RESERVATIONS, FOOD_ORDERS, ORDER_ITEMS, BILLS and PAYMENTS. Primary keys uniquely identify rows. Foreign keys preserve relationships. Unique constraints prevent duplicate usernames, emails, table numbers and one bill per order. CHECK constraints validate prices, quantities, capacities and non-negative amounts. Indexes support menu filtering, customer lookup, reservation status/time, order status and payment reporting.

## 7. Relationships
- One user can have one customer profile or one employee profile.
- One food category has many menu items.
- One customer can make many reservations and food orders.
- A dining table can be associated with reservations and dine-in orders.
- One food order contains many order items.
- Each order item refers to one menu item.
- One order can have one bill.
- A bill can have multiple payment records.

## 8. Normalization
The design aims for Third Normal Form (3NF):
- 1NF: each column stores one value; each table has a primary key.
- 2NF: non-key attributes depend on the whole primary key. Most tables use a single-column surrogate key.
- 3NF: customer details, employee details, category details, menu details, orders, bills and payments are separated into their own tables to avoid transitive dependencies and repeated data.
- `unit_price` is stored in ORDER_ITEMS as a price snapshot at order time, so later menu price changes do not alter past bills. `line_total` is generated from quantity × unit price in MySQL.

## 9. Advanced database features
- Views: `vw_order_summary`, `vw_daily_sales`, `vw_menu_popularity`.
- Indexes: category/availability, menu name, customer phone, reservation time/status, order status/date, customer order lookup, order-item lookup, payment status/date.
- Function: `fn_bill_total` calculates subtotal plus tax less discount.
- Procedures: `sp_update_order_status` validates and changes order status; `sp_daily_sales` reports daily completed payments.
- Triggers: after insert/update on ORDER_ITEMS, update the parent order total.
- Transaction: order placement inserts an order, its line items and a bill in one commit; failures roll back all changes.

## 10. Security
Passwords are stored as Werkzeug password hashes in app-created demo accounts, not as plaintext. The backend checks roles on protected routes. Customers are restricted to their own records. The demo does not process real payments and does not store card details. Before deployment, configure a strong secret, HTTPS, secure database credentials, CSRF protection, rate limiting, backups and a production WSGI server. Change all demo passwords.

## 11. Testing
Use `tests/TEST_PLAN.md`. Test valid and invalid logins, each role's permissions, menu CRUD, reservation submission, order creation, bill generation, payment recording, filters and SQL advanced features.

## 12. Limitations and future scope
- Reservation requests require staff confirmation; robust overlapping-time table allocation should be added before commercial use.
- The current online order is a demo takeaway flow and does not integrate a delivery provider.
- Payments are simulated; no payment gateway is connected.
- Add CSRF protection, password reset, audit logs, automated tests and more comprehensive deployment hardening before production use.

## 13. Conclusion
Bhoj Kolkata demonstrates how a web interface can communicate with a relational database to manage a restaurant's core workflow. It provides role-based screens and SQL artifacts aligned with the BTY39105 PBL requirements. The team should run the SQL scripts, verify every feature, add screenshots and group details, publish the repository and deploy a live version before final submission.
