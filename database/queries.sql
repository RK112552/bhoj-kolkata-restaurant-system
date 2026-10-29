USE bhoj_kolkata;

-- 1. Basic SELECT: available menu
SELECT name,price FROM menu_items WHERE is_available=TRUE ORDER BY name;

-- 2. Basic SELECT: active users (never display password hashes)
SELECT id,username,role,full_name FROM users WHERE active=TRUE;

-- 3. Basic SELECT: tables by capacity
SELECT table_number,capacity,area FROM dining_tables WHERE status='available' ORDER BY capacity;

-- 4. Basic SELECT: pending reservations
SELECT * FROM reservations WHERE status='pending' ORDER BY reservation_at;

-- 5. Basic SELECT: active orders
SELECT id,status,total_amount FROM food_orders WHERE status IN ('placed','confirmed','preparing');

-- 6. Basic SELECT: unpaid bills
SELECT id,order_id,total_amount FROM bills WHERE status='unpaid';

-- 7. Basic SELECT: completed payments
SELECT id,bill_id,amount,method,paid_at FROM payments WHERE status='completed';

-- 8. Basic SELECT: vegetarian menu
SELECT name,price FROM menu_items WHERE is_vegetarian=TRUE;

-- 9. Basic SELECT: menu in a price range
SELECT name,price FROM menu_items WHERE price BETWEEN 100 AND 300 ORDER BY price;

-- 10. Basic SELECT: latest orders
SELECT id,created_at,status,total_amount FROM food_orders ORDER BY created_at DESC LIMIT 10;

-- 11. Aggregate / GROUP BY: order counts by status
SELECT status,COUNT(*) AS order_count FROM food_orders GROUP BY status;

-- 12. Aggregate: paid revenue by payment method
SELECT method,SUM(amount) AS revenue FROM payments WHERE status='completed' GROUP BY method;

-- 13. Aggregate: average menu price by category
SELECT c.name,ROUND(AVG(m.price),2) AS average_price
FROM food_categories c JOIN menu_items m ON m.category_id=c.id GROUP BY c.id,c.name;

-- 14. Aggregate: high-demand dishes
SELECT m.name,SUM(oi.quantity) AS units_sold
FROM order_items oi JOIN menu_items m ON m.id=oi.menu_item_id
GROUP BY m.id,m.name HAVING SUM(oi.quantity)>=1 ORDER BY units_sold DESC;

-- 15. Aggregate: sales per day
SELECT DATE(paid_at) AS sales_date,SUM(amount) AS revenue
FROM payments WHERE status='completed' GROUP BY DATE(paid_at) ORDER BY sales_date DESC;

-- 16. JOIN: order with customer
SELECT o.id,c.full_name,o.status,o.total_amount FROM food_orders o
LEFT JOIN customers c ON c.id=o.customer_id;

-- 17. JOIN: order line details
SELECT oi.order_id,m.name,oi.quantity,oi.unit_price,oi.line_total
FROM order_items oi JOIN menu_items m ON m.id=oi.menu_item_id;

-- 18. JOIN: reservation and table
SELECT r.id,c.full_name,r.reservation_at,r.guests,t.table_number,r.status
FROM reservations r JOIN customers c ON c.id=r.customer_id
LEFT JOIN dining_tables t ON t.id=r.table_id;

-- 19. JOIN: bills and payments
SELECT b.id,b.order_id,b.total_amount,b.status,p.method,p.amount,p.status AS payment_status
FROM bills b LEFT JOIN payments p ON p.bill_id=b.id;

-- 20. JOIN: menu category and availability
SELECT m.name,c.name AS category,m.price,m.is_available
FROM menu_items m JOIN food_categories c ON c.id=m.category_id;

-- 21. Subquery: dishes above average price
SELECT name,price FROM menu_items WHERE price>(SELECT AVG(price) FROM menu_items);

-- 22. Subquery: customers who have placed orders
SELECT full_name FROM customers WHERE id IN (SELECT customer_id FROM food_orders WHERE customer_id IS NOT NULL);

-- 23. Subquery: orders whose total exceeds average
SELECT id,total_amount FROM food_orders WHERE total_amount>(SELECT AVG(total_amount) FROM food_orders);

-- 24. Correlated subquery: items priced above their category average
SELECT m.name,m.price,m.category_id FROM menu_items m
WHERE m.price>(SELECT AVG(m2.price) FROM menu_items m2 WHERE m2.category_id=m.category_id);

-- 25. Correlated subquery: customers with at least one order
SELECT c.id,c.full_name FROM customers c
WHERE EXISTS (SELECT 1 FROM food_orders o WHERE o.customer_id=c.id);

-- 26. Dashboard query: recent orders
SELECT * FROM vw_order_summary ORDER BY created_at DESC LIMIT 10;

-- 27. Dashboard query: daily sales
SELECT * FROM vw_daily_sales ORDER BY sales_date DESC;

-- 28. Dashboard query: popular menu
SELECT * FROM vw_menu_popularity ORDER BY units_sold DESC LIMIT 10;
