-- NailsbyBrookJ Database Schema
-- Business management and booking system for independent nail business

-- Drop tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS PhotoTags;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS PortfolioPhotos;
DROP TABLE IF EXISTS LoyaltyPoints;
DROP TABLE IF EXISTS ServiceItems;
DROP TABLE IF EXISTS Appointments;
DROP TABLE IF EXISTS Services;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Clients;

-- Clients Table
-- Stores customer information including preferences and allergies
CREATE TABLE Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    instagram VARCHAR(100),
    email VARCHAR(100),
    allergies TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_phone (phone)
);

-- Services Table
-- Catalog of nail services offered
CREATE TABLE Services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    avg_duration INT NOT NULL COMMENT 'Duration in minutes',
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Appointments Table
-- Manages bookings and tracks profitability
CREATE TABLE Appointments (
    appt_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    service_id INT NOT NULL,
    appt_date DATE NOT NULL,
    appt_time TIME NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status ENUM('scheduled', 'confirmed', 'completed', 'cancelled', 'no-show') DEFAULT 'scheduled',
    notes TEXT,
    product_cost DECIMAL(10, 2) DEFAULT 0.00,
    profit DECIMAL(10, 2) GENERATED ALWAYS AS (price - product_cost) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES Services(service_id) ON DELETE RESTRICT,
    INDEX idx_appt_date (appt_date),
    INDEX idx_status (status)
);

-- Inventory Table
-- Tracks nail supplies and products
CREATE TABLE Inventory (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity DECIMAL(10, 2) NOT NULL DEFAULT 0,
    unit VARCHAR(20) NOT NULL COMMENT 'oz, ml, count, etc.',
    unit_cost DECIMAL(10, 2) NOT NULL,
    supplier VARCHAR(100),
    low_stock_threshold DECIMAL(10, 2) NOT NULL DEFAULT 5,
    category VARCHAR(50) COMMENT 'polish, gel, tools, etc.',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_low_stock (quantity, low_stock_threshold)
);

-- ServiceItems Table
-- Links services to inventory items used (many-to-many)
CREATE TABLE ServiceItems (
    service_item_id INT AUTO_INCREMENT PRIMARY KEY,
    service_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity_used DECIMAL(10, 2) NOT NULL COMMENT 'Amount used per service',
    FOREIGN KEY (service_id) REFERENCES Services(service_id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id) ON DELETE CASCADE,
    UNIQUE KEY unique_service_item (service_id, item_id)
);

-- PortfolioPhotos Table
-- Showcases completed nail sets
CREATE TABLE PortfolioPhotos (
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(500) NOT NULL,
    title VARCHAR(100),
    description TEXT,
    appt_id INT COMMENT 'Optional link to appointment',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appt_id) REFERENCES Appointments(appt_id) ON DELETE SET NULL,
    INDEX idx_created (created_at DESC)
);

-- Tags Table
-- Style tags for categorizing nail designs
CREATE TABLE Tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(50) COMMENT 'color, style, season, occasion, etc.',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PhotoTags Table
-- Many-to-many relationship between photos and tags
CREATE TABLE PhotoTags (
    photo_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (photo_id, tag_id),
    FOREIGN KEY (photo_id) REFERENCES PortfolioPhotos(photo_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(tag_id) ON DELETE CASCADE
);

-- LoyaltyPoints Table
-- Tracks customer loyalty rewards
CREATE TABLE LoyaltyPoints (
    client_id INT PRIMARY KEY,
    points INT NOT NULL DEFAULT 0,
    lifetime_points INT NOT NULL DEFAULT 0,
    last_earned TIMESTAMP NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id) ON DELETE CASCADE
);

-- Insert sample services
INSERT INTO Services (name, base_price, avg_duration, description) VALUES
('Classic Manicure', 25.00, 30, 'Traditional manicure with polish'),
('Gel Manicure', 40.00, 45, 'Long-lasting gel polish application'),
('Acrylic Full Set', 55.00, 90, 'Full set of acrylic nails'),
('Gel Extension', 65.00, 120, 'Gel nail extensions'),
('Nail Art - Simple', 10.00, 15, 'Basic nail art design (per nail)'),
('Nail Art - Complex', 20.00, 30, 'Detailed nail art design (per nail)'),
('Pedicure', 35.00, 45, 'Full pedicure service'),
('Nail Repair', 5.00, 10, 'Single nail repair');

-- Insert sample tags
INSERT INTO Tags (name, category) VALUES
('French', 'style'),
('Ombre', 'style'),
('Matte', 'finish'),
('Glossy', 'finish'),
('Glitter', 'element'),
('Chrome', 'finish'),
('Floral', 'design'),
('Geometric', 'design'),
('Minimalist', 'style'),
('Red', 'color'),
('Pink', 'color'),
('Nude', 'color'),
('Black', 'color'),
('White', 'color'),
('Pastel', 'color'),
('Spring', 'season'),
('Summer', 'season'),
('Fall', 'season'),
('Winter', 'season'),
('Wedding', 'occasion'),
('Holiday', 'occasion'),
('Everyday', 'occasion');

-- Insert sample inventory items
INSERT INTO Inventory (name, quantity, unit, unit_cost, supplier, low_stock_threshold, category) VALUES
('Base Coat', 3, 'bottle', 8.99, 'Beauty Supply Co', 2, 'polish'),
('Top Coat', 4, 'bottle', 9.99, 'Beauty Supply Co', 2, 'polish'),
('Gel Base Coat', 2, 'bottle', 15.99, 'Gel Pro', 1, 'gel'),
('Gel Top Coat', 2, 'bottle', 15.99, 'Gel Pro', 1, 'gel'),
('Acrylic Powder - Clear', 500, 'gram', 25.00, 'Nail Tech Supplies', 100, 'acrylic'),
('Acrylic Liquid', 8, 'oz', 18.00, 'Nail Tech Supplies', 4, 'acrylic'),
('Nail Files - 100 grit', 50, 'count', 0.50, 'Beauty Supply Co', 20, 'tools'),
('Nail Buffer', 30, 'count', 0.75, 'Beauty Supply Co', 15, 'tools'),
('Cuticle Oil', 5, 'bottle', 6.99, 'Beauty Supply Co', 2, 'treatment'),
('Acetone', 32, 'oz', 12.99, 'Beauty Supply Co', 16, 'supplies');
