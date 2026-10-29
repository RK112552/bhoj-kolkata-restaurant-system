# Normalization Notes

## Functional dependencies (examples)
- USERS: `id → username, password_hash, role, full_name, email, phone, active`
- MENU_ITEMS: `id → category_id, name, description, price, is_vegetarian, is_available`
- RESERVATIONS: `id → customer_id, table_id, reservation_at, guests, status, notes`
- FOOD_ORDERS: `id → customer_id, order_type, table_id, status, total_amount, created_at`
- ORDER_ITEMS: `id → order_id, menu_item_id, quantity, unit_price`
- BILLS: `id → order_id, subtotal, tax_amount, discount_amount, total_amount, status`
- PAYMENTS: `id → bill_id, amount, method, status, transaction_ref, paid_at`

## First Normal Form (1NF)
Every table has a primary key and attributes contain single/atomic values. Menu items are not stored as comma-separated lists inside an order; each ordered dish is a separate ORDER_ITEMS row.

## Second Normal Form (2NF)
Each table uses a single-column primary key. Therefore non-key attributes depend on the entire primary key. ORDER_ITEMS records one menu item and quantity per row.

## Third Normal Form (3NF)
Entities are separated to avoid storing category names in every menu row, customer contact information in every order, or payment details in bills. Menu category names live in FOOD_CATEGORIES, customer profile data in CUSTOMERS, and payment transaction details in PAYMENTS.

## Design trade-off
FOOD_ORDERS.total_amount is maintained for efficient operational display and recalculated from order lines by triggers in MySQL. In production, ensure application and trigger logic remain consistent and consider whether to store calculated totals or derive them at query time.
