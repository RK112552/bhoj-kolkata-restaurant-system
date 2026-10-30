
USE bhoj_kolkata;

DROP TRIGGER IF EXISTS trg_order_item_after_insert;
DROP TRIGGER IF EXISTS trg_order_item_after_update;

DELIMITER //

CREATE TRIGGER trg_order_item_after_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE food_orders
    SET total_amount = (
        SELECT COALESCE(SUM(quantity * unit_price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END//

CREATE TRIGGER trg_order_item_after_update
AFTER UPDATE ON order_items
FOR EACH ROW
BEGIN
    UPDATE food_orders
    SET total_amount = (
        SELECT COALESCE(SUM(quantity * unit_price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END//

DELIMITER ;
