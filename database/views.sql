USE bhoj_kolkata;
CREATE OR REPLACE VIEW vw_order_summary AS
SELECT o.id AS order_id, o.created_at, o.order_type, o.status AS order_status,
       c.full_name AS customer_name, o.total_amount, b.id AS bill_id,
       b.status AS bill_status, b.tax_amount
FROM food_orders o
LEFT JOIN customers c ON c.id=o.customer_id
LEFT JOIN bills b ON b.order_id=o.id;

CREATE OR REPLACE VIEW vw_daily_sales AS
SELECT DATE(p.paid_at) AS sales_date, COUNT(DISTINCT p.id) AS payment_count,
       SUM(p.amount) AS revenue
FROM payments p
WHERE p.status='completed'
GROUP BY DATE(p.paid_at);

CREATE OR REPLACE VIEW vw_menu_popularity AS
SELECT m.id AS menu_item_id, m.name, c.name AS category,
       COALESCE(SUM(oi.quantity),0) AS units_sold,
       COALESCE(SUM(oi.quantity*oi.unit_price),0) AS sales_value
FROM menu_items m
JOIN food_categories c ON c.id=m.category_id
LEFT JOIN order_items oi ON oi.menu_item_id=m.id
LEFT JOIN food_orders o ON o.id=oi.order_id AND o.status <> 'cancelled'
GROUP BY m.id,m.name,c.name;
