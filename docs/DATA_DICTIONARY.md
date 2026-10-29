# Data Dictionary (Summary)

| Table | Purpose | Important attributes |
|---|---|---|
| USERS | Login identity and role | id, username, password_hash, role, active |
| CUSTOMERS | Customer contact/profile | id, user_id, full_name, phone, email |
| EMPLOYEES | Staff information | id, user_id, role_title, salary, active |
| DINING_TABLES | Restaurant seating | id, table_number, capacity, area, status |
| FOOD_CATEGORIES | Menu groupings | id, name, description |
| MENU_ITEMS | Food catalogue | id, category_id, name, price, availability |
| RESERVATIONS | Booking requests | id, customer_id, table_id, reservation_at, guests, status |
| FOOD_ORDERS | Order header | id, customer_id, order_type, status, total_amount |
| ORDER_ITEMS | Items inside an order | id, order_id, menu_item_id, quantity, unit_price |
| BILLS | Financial summary for an order | id, order_id, subtotal, tax_amount, discount_amount, total_amount, status |
| PAYMENTS | Payment records | id, bill_id, amount, method, status, transaction_ref |

## Notes
- `password_hash` contains a one-way password hash, never a plaintext password.
- `unit_price` captures the item price when ordered.
- `is_available` lets managers hide a menu item without deleting historical order references.
- Revenue should be computed from completed payment records, not typed into HTML.
