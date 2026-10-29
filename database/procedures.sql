USE bhoj_kolkata;
DELIMITER //
CREATE PROCEDURE sp_update_order_status(IN p_order_id BIGINT, IN p_new_status VARCHAR(20))
BEGIN
  IF p_new_status NOT IN ('placed','confirmed','preparing','ready','served','cancelled') THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Invalid order status';
  END IF;
  UPDATE food_orders SET status=p_new_status WHERE id=p_order_id;
  IF ROW_COUNT()=0 THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Order not found';
  END IF;
END//

CREATE PROCEDURE sp_daily_sales(IN p_sales_date DATE)
BEGIN
  SELECT COUNT(DISTINCT p.id) AS payment_count,
         COALESCE(SUM(p.amount),0) AS total_revenue
  FROM payments p
  WHERE p.status='completed' AND DATE(p.paid_at)=p_sales_date;
END//
DELIMITER ;
-- Examples:
-- CALL sp_update_order_status(1,'preparing');
-- CALL sp_daily_sales(CURDATE());
