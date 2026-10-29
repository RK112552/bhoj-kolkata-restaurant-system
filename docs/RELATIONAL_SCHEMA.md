# Relational Schema

- USERS(**id**, username UNIQUE, password_hash, role, full_name, email UNIQUE, phone, active, created_at)
- CUSTOMERS(**id**, user_id FK→USERS.id UNIQUE, full_name, phone, email, created_at)
- EMPLOYEES(**id**, user_id FK→USERS.id UNIQUE, full_name, role_title, phone, salary, hire_date, active)
- DINING_TABLES(**id**, table_number UNIQUE, capacity, area, status)
- FOOD_CATEGORIES(**id**, name UNIQUE, description)
- MENU_ITEMS(**id**, category_id FK→FOOD_CATEGORIES.id, name, description, price, is_vegetarian, is_available, image_url, created_at)
- RESERVATIONS(**id**, customer_id FK→CUSTOMERS.id, table_id FK→DINING_TABLES.id NULL, reservation_at, guests, status, notes, created_at)
- FOOD_ORDERS(**id**, customer_id FK→CUSTOMERS.id NULL, order_type, table_id FK→DINING_TABLES.id NULL, status, total_amount, notes, created_at)
- ORDER_ITEMS(**id**, order_id FK→FOOD_ORDERS.id, menu_item_id FK→MENU_ITEMS.id, quantity, unit_price, generated line_total)
- BILLS(**id**, order_id FK→FOOD_ORDERS.id UNIQUE, subtotal, tax_amount, discount_amount, total_amount, status, created_at)
- PAYMENTS(**id**, bill_id FK→BILLS.id, amount, method, status, transaction_ref UNIQUE, paid_at)

## Key constraints
- Primary keys are bold.
- `UK` means unique constraint.
- `FK` means foreign key.
- Price and amount columns are constrained to valid non-negative/positive values.
- A bill belongs to one order; an order can contain multiple order items and a bill can have multiple payment attempts/records.
