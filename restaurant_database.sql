-- Create database
CREATE DATABASE RestaurantDB;
USE RestaurantDB;

-- Table 1: Menu
CREATE TABLE Menu (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(100),
    price DECIMAL(10, 2)
);

-- Table 2: Customers
CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    phone_number VARCHAR(15)
);

-- Table 3: Orders
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    item_id INT,
    quantity INT,
    order_time DATETIME,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (item_id) REFERENCES Menu(item_id)
);

-- Insert sample data into Menu
INSERT INTO Menu VALUES 
(1, 'Burger', 120.00),
(2, 'Pizza', 250.00),
(3, 'Fried Rice', 180.00),
(4, 'Pasta', 220.00);

-- Insert sample data into Customers
INSERT INTO Customers VALUES 
(101, 'Rahul Sharma', '9876543210'),
(102, 'Anjali Mehta', '9123456780');

-- Insert sample orders
INSERT INTO Orders VALUES 
(1001, 101, 2, 1, NOW()),
(1002, 102, 3, 2, NOW());
