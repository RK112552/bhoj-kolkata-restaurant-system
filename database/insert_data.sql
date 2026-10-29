USE bhoj_kolkata;
-- Password hashes are generated at first application start for the demo users.
-- The Flask app's SQLite preview seeds its own accounts. For MySQL, run the app once
-- after schema setup; it creates no MySQL demo users automatically. Use scripts below
-- to add fictional catalogue data. Add user accounts through a secure seed script or
-- generate hashes with: python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))"

INSERT IGNORE INTO food_categories(name,description) VALUES
('Starters','Small plates and Bengali snacks'),
('Bengali Classics','Traditional Bengali favourites'),
('Main Course','Comforting mains'),
('Breads & Rice','Rice and breads'),
('Desserts','Sweet endings'),
('Beverages','Refreshing drinks');

INSERT INTO dining_tables(table_number,capacity,area,status) VALUES
('T01',2,'Main Hall','available'),('T02',2,'Main Hall','available'),
('T03',2,'Window Side','available'),('T04',4,'Main Hall','available'),
('T05',4,'Main Hall','available'),('T06',4,'Window Side','available'),
('T07',6,'Garden','available'),('T08',6,'Garden','available')
ON DUPLICATE KEY UPDATE capacity=VALUES(capacity),area=VALUES(area);

INSERT INTO menu_items(category_id,name,description,price,is_vegetarian,is_available) VALUES
((SELECT id FROM food_categories WHERE name='Starters'),'Kolkata Fish Fry','Crisp crumb-coated fish fillet with kasundi',260,FALSE,TRUE),
((SELECT id FROM food_categories WHERE name='Starters'),'Mochar Chop','Banana blossom croquettes',160,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Bengali Classics'),'Shorshe Ilish','Hilsa in mustard gravy',480,FALSE,TRUE),
((SELECT id FROM food_categories WHERE name='Bengali Classics'),'Kosha Mangsho','Slow-cooked Bengali mutton curry',390,FALSE,TRUE),
((SELECT id FROM food_categories WHERE name='Bengali Classics'),'Chingri Malai Curry','Prawns in coconut milk gravy',420,FALSE,TRUE),
((SELECT id FROM food_categories WHERE name='Main Course'),'Chicken Chaap','Rich Kolkata-style chicken chaap',320,FALSE,TRUE),
((SELECT id FROM food_categories WHERE name='Breads & Rice'),'Basanti Pulao','Fragrant sweet yellow rice',190,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Breads & Rice'),'Luchi (4 pcs)','Fluffy fried Bengali bread',80,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Desserts'),'Baked Rosogolla','Warm baked Bengali cottage-cheese dessert',120,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Desserts'),'Mishti Doi','Traditional sweet yogurt',90,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Beverages'),'Aam Panna','Refreshing raw mango cooler',85,TRUE,TRUE),
((SELECT id FROM food_categories WHERE name='Beverages'),'Darjeeling Tea','Light aromatic tea',60,TRUE,TRUE);
