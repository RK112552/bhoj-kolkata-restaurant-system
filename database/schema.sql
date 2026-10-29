-- Bhoj Kolkata Restaurant Management System
-- MySQL 8.0+ | Run with a MySQL user that can create databases.
CREATE DATABASE IF NOT EXISTS bhoj_kolkata CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bhoj_kolkata;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(60) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('admin','manager','kitchen','cashier','receptionist','customer') NOT NULL,
  full_name VARCHAR(120) NOT NULL,
  email VARCHAR(160) UNIQUE,
  phone VARCHAR(25),
  active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS customers (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  phone VARCHAR(25) NOT NULL,
  email VARCHAR(160),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_customer_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_customer_phone(phone)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS employees (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT UNIQUE,
  full_name VARCHAR(120) NOT NULL,
  role_title VARCHAR(80) NOT NULL,
  phone VARCHAR(25),
  salary DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK(salary >= 0),
  hire_date DATE,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  CONSTRAINT fk_employee_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS dining_tables (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  table_number VARCHAR(12) NOT NULL UNIQUE,
  capacity TINYINT UNSIGNED NOT NULL CHECK(capacity BETWEEN 1 AND 20),
  area VARCHAR(50) NOT NULL DEFAULT 'Main Hall',
  status ENUM('available','reserved','occupied','maintenance') NOT NULL DEFAULT 'available'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS food_categories (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(80) NOT NULL UNIQUE,
  description VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS menu_items (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  category_id BIGINT NOT NULL,
  name VARCHAR(120) NOT NULL,
  description VARCHAR(500),
  price DECIMAL(10,2) NOT NULL CHECK(price > 0),
  is_vegetarian BOOLEAN NOT NULL DEFAULT FALSE,
  is_available BOOLEAN NOT NULL DEFAULT TRUE,
  image_url VARCHAR(500),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_menu_category FOREIGN KEY(category_id) REFERENCES food_categories(id),
  INDEX idx_menu_category_availability(category_id,is_available),
  INDEX idx_menu_name(name)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reservations (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_id BIGINT NOT NULL,
  table_id BIGINT NULL,
  reservation_at DATETIME NOT NULL,
  guests TINYINT UNSIGNED NOT NULL CHECK(guests BETWEEN 1 AND 20),
  status ENUM('pending','confirmed','seated','completed','cancelled') NOT NULL DEFAULT 'pending',
  notes VARCHAR(500),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_reservation_customer FOREIGN KEY(customer_id) REFERENCES customers(id),
  CONSTRAINT fk_reservation_table FOREIGN KEY(table_id) REFERENCES dining_tables(id) ON DELETE SET NULL,
  INDEX idx_reservation_time_status(reservation_at,status)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS food_orders (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  customer_id BIGINT NULL,
  order_type ENUM('dine_in','takeaway','delivery') NOT NULL DEFAULT 'dine_in',
  table_id BIGINT NULL,
  status ENUM('placed','confirmed','preparing','ready','served','cancelled') NOT NULL DEFAULT 'placed',
  total_amount DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK(total_amount >= 0),
  notes VARCHAR(500),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_order_customer FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE SET NULL,
  CONSTRAINT fk_order_table FOREIGN KEY(table_id) REFERENCES dining_tables(id) ON DELETE SET NULL,
  INDEX idx_order_status_created(status,created_at),
  INDEX idx_order_customer(customer_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id BIGINT NOT NULL,
  menu_item_id BIGINT NOT NULL,
  quantity SMALLINT UNSIGNED NOT NULL CHECK(quantity BETWEEN 1 AND 100),
  unit_price DECIMAL(10,2) NOT NULL CHECK(unit_price > 0),
  line_total DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  CONSTRAINT fk_order_item_order FOREIGN KEY(order_id) REFERENCES food_orders(id) ON DELETE CASCADE,
  CONSTRAINT fk_order_item_menu FOREIGN KEY(menu_item_id) REFERENCES menu_items(id),
  INDEX idx_order_items_order(order_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bills (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  order_id BIGINT NOT NULL UNIQUE,
  subtotal DECIMAL(10,2) NOT NULL CHECK(subtotal >= 0),
  tax_amount DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK(tax_amount >= 0),
  discount_amount DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK(discount_amount >= 0),
  total_amount DECIMAL(10,2) NOT NULL CHECK(total_amount >= 0),
  status ENUM('unpaid','paid','void') NOT NULL DEFAULT 'unpaid',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_bill_order FOREIGN KEY(order_id) REFERENCES food_orders(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS payments (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  bill_id BIGINT NOT NULL,
  amount DECIMAL(10,2) NOT NULL CHECK(amount > 0),
  method ENUM('cash','upi','card','online') NOT NULL,
  status ENUM('pending','completed','failed','refunded') NOT NULL DEFAULT 'pending',
  transaction_ref VARCHAR(100) UNIQUE,
  paid_at TIMESTAMP NULL,
  CONSTRAINT fk_payment_bill FOREIGN KEY(bill_id) REFERENCES bills(id),
  INDEX idx_payment_status_date(status,paid_at)
) ENGINE=InnoDB;
