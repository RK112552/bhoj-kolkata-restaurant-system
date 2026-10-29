USE bhoj_kolkata;
DELIMITER //
CREATE FUNCTION fn_bill_total(p_subtotal DECIMAL(10,2), p_tax_rate DECIMAL(5,2), p_discount DECIMAL(10,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
NO SQL
BEGIN
  RETURN GREATEST(0, ROUND(p_subtotal + (p_subtotal * p_tax_rate / 100) - p_discount, 2));
END//
DELIMITER ;
-- Example: SELECT fn_bill_total(1000.00, 5.00, 50.00) AS bill_total;
