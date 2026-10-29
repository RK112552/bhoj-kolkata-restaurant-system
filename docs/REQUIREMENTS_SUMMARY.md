# Requirements Summary

## Functional requirements
1. Login/logout and role-based authorization.
2. Browse, search and filter menu items.
3. Create reservation requests and staff confirmation/table assignment.
4. Place customer orders and view order status/history.
5. Manage order processing statuses.
6. Generate a bill for each order.
7. Record demo payments and payment status.
8. Manage menu items and availability.
9. View employee records and restrict employee login activation to admin.
10. Display operational and sales dashboard values from database queries.

## Non-functional requirements
- Responsive design for desktop, tablet and mobile.
- Data integrity using primary/foreign keys and constraints.
- Password hashing and server-side role checks.
- Friendly validation and error pages.
- Reproducible SQL setup and documented local execution.
- GitHub history and a deployed public demo URL for final evaluation.

## Business rules
- Only admin and manager can edit menu records.
- Only admin can enable/disable employee logins.
- Kitchen staff can update order status but cannot see revenue.
- Cashier can record payment status but cannot manage menu/staff.
- Receptionist can manage reservations but cannot see sales reports.
- Customer can only see their own order/reservation records and cannot access internal dashboards.
- An order is created with order lines and a bill in a single transaction.
- Payment is simulated; no real payment details are collected.
