CREATE DATABASE IF NOT EXISTS plantfarma
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE plantfarma;

CREATE TABLE IF NOT EXISTS farmers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kisan_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(120) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    efficientnet_class VARCHAR(150) NOT NULL,
    crop VARCHAR(100) NOT NULL,
    disease VARCHAR(180) NOT NULL,
    medicine VARCHAR(150) NOT NULL,
    active_ingredient VARCHAR(180) NOT NULL,
    treatment_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price VARCHAR(80) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_product_medicine (medicine),
    INDEX idx_product_class (efficientnet_class)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Confirmed',
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    ordered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_farmer
        FOREIGN KEY (farmer_id) REFERENCES farmers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    price_text VARCHAR(80) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products(id)
);
