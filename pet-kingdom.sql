DROP DATABASE petkingdom;
CREATE DATABASE IF NOT EXISTS petkingdom;
use petkingdom; 
DROP TABLE IF EXISTS Users;
CREATE TABLE Users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  password VARCHAR(255),
  type varchar(225)
);

INSERT INTO Users (name, email, password, type)
VALUES 
  ('John Smith', 'john.smith@example.com', 'password123', 'admin'),
  ('Jane Doe', 'jane.doe@example.com', 'qwertyuiop', 'admin'),
  ('Bob Johnson', 'bob.johnson@example.com', 'mypassword', 'customer'),
  ('Alice Green', 'alice.green@example.com', 'letmein', 'customer'),
  ('David Lee', 'david.lee@example.com', '123456789', 'customer'),
  ('Sarah Johnson', 'sarah.johnson@example.com', 'mypassword', 'customer'),
  ('Mark Davis', 'mark@example.com', 'password1234', 'customer'),
  ('Karen Lee', 'karen.lee@example.com', 'secret123', 'supplier'),
  ('Mark Wilson', 'mark@example.com', 'p@ssw0rd', 'supplier'),
  ('Emily Chen', 'emily.chen@example.com', 'ilovecats', 'supplier');
  
  SELECT * FROM Users;

DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  order_date DATE,
  user_id INT,
  product_name VARCHAR(100) NOT NULL,
  quantity INT NOT NULL,
  total_price DECIMAL(10, 2),
  FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


DELETE FROM Orders
WHERE order_id = 3;

INSERT INTO Orders (order_date, user_id, product_name, quantity, total_price)
VALUES 
  ('2022-03-10', 3, 'Pedigree', 10, 300.00);
INSERT INTO Orders (order_date, user_id, product_name, quantity, total_price)
VALUES 
  ('2022-03-10', 3, 'Royal Canine', 1, 60.00);
  
SELECT * FROM Orders;
  
SELECT order_id, order_date, total_price FROM Orders WHERE user_id = 3;

DROP TABLE IF EXISTS Products;
CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);

INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (101, 'Pedigree', 'Dog food for Puppies', 30.00, 1000);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (102, 'Royal Canine', 'Canned fruitables', 60.00, 550);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (103, 'Ball', 'Ball for pets', 20.00, 100);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (104, 'Sweater', 'Fuzzy wear for cats/dogs', 15.00, 400);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (105, 'Fancy Feast', 'Gourmet cat food', 25.00, 800);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (106, 'Bedsure Orthopedic Dog Bed', 'Memory foam dog bed', 70.00, 300);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (108, 'Kong Classic', 'Durable chew toy for dogs', 12.00, 500);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (107, 'SmartyKat Skitter Critters', 'Interactive cat toy', 5.00, 700);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (109, 'Trixie Pet Products Miguel Fold and Store Cat Tower', 'Cat tree with scratch pad and condo', 80.00, 200);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (110, 'Hills Science Diet', 'Dry dog food for adult dogs', 50.00, 1200);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (111, 'Blue Buffalo', 'Grain-free dog food', 45.00, 900);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (112, 'Nylabone DuraChew', 'Textured chew toy for aggressive chewers', 15.00, 400);
INSERT INTO Products (product_id, product_name, description, price, stock_quantity)
VALUES (113, 'PetSafe Drinkwell Platinum Cat and Dog Water Fountain', 'Automatic water dispenser for pets', 45.00, 350);

SELECT * FROM Products;

DROP TABLE IF EXISTS Food;
CREATE TABLE Food (
    product_id INT PRIMARY KEY,
    expiration_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Food (product_id, expiration_date)
VALUES (101, '2024-01-06');
INSERT INTO Food (product_id, expiration_date)
VALUES (102, '2025-06-15');
INSERT INTO Food (product_id, expiration_date)
VALUES (105, '2025-06-15');
INSERT INTO Food (product_id, expiration_date)
VALUES (110, '2024-12-25');
INSERT INTO Food (product_id, expiration_date)
VALUES (111, '2026-09-07');

SELECT * FROM Food;

SELECT product_name, description, price, expiration_date
FROM Products p INNER JOIN Food f USING(product_id);

DROP TABLE IF EXISTS Toys;
CREATE TABLE Toys (
    product_id INT PRIMARY KEY,
    material VARCHAR(50) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Toys (product_id, material) VALUES (103, 'rubber');
INSERT INTO Toys (product_id, material) VALUES (108, 'rubber');
INSERT INTO Toys (product_id, material) VALUES (107, 'plastic');
INSERT INTO Toys (product_id, material) VALUES (112, 'silicon');

SELECT * FROM Toys;

DROP TABLE IF EXISTS Accessories;
CREATE TABLE Accessories (
    product_id INT PRIMARY KEY,
    color VARCHAR(20) NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO Accessories (product_id, color) VALUES (104, 'red');
INSERT INTO Accessories (product_id, color) VALUES (106, 'blue');
INSERT INTO Accessories (product_id, color) VALUES (109, 'white');
INSERT INTO Accessories (product_id, color) VALUES (113, 'silver');
SELECT * FROM Accessories;

SELECT product_name, description, price, expiration_date, material, color 
FROM Products p LEFT JOIN Food f USING(product_id)
LEFT JOIN Toys t USING(product_id)
LEFT JOIN Accessories a USING(product_id);

SELECT product_name, description, price, expiration_date FROM Products p INNER JOIN Food f USING(product_id)

DELIMITER //
CREATE TRIGGER update_product_stock
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
  UPDATE Products
  SET stock_quantity = stock_quantity - NEW.quantity
  WHERE product_name = NEW.product_name;
END//
DELIMITER ;

DELIMITER $$
CREATE FUNCTION fn_get_customer_order_count(customer_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE order_count INT;
    SELECT COUNT(*) INTO order_count FROM Orders WHERE user_id = customer_id;
    RETURN order_count;
END $$
DELIMITER ;

DELIMITER //

CREATE PROCEDURE check_user_type(IN c_user_id INT, OUT c_user_type VARCHAR(255))
BEGIN
  SELECT type INTO c_user_type FROM Users WHERE user_id = c_user_id;
END//

DELIMITER ;

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
	sales_id int auto_increment primary key,
    sales_date DATE,
    amount INT
);
drop event daily_sales;
CREATE EVENT daily_sales
ON SCHEDULE
    EVERY 1 DAY
DO
    INSERT INTO sales (sales_date, amount)
    SELECT DATE(order_date) AS sales_date, SUM(total_price) AS amount
    FROM Orders
    GROUP BY DATE(order_date);
    
    select * from sales;
    
DROP PROCEDURE IF EXISTS GetOrders;
DELIMITER //
CREATE PROCEDURE GetOrders(IN userId INT)
BEGIN
    SELECT order_id, order_date, product_name, quantity, total_price
    FROM Orders
    WHERE user_id = userId;
END // 
DELIMITER ;

CALL GetOrders(3);


DROP PROCEDURE get_user_EP;
DELIMITER //
CREATE PROCEDURE get_user_EP(IN email_ VARCHAR(255), IN password_ VARCHAR(255))
BEGIN
    SELECT user_id, email, password, type
    FROM Users 
    WHERE email = email_ AND password = password_;
END // 
DELIMITER ;

CALL get_user_EP('bob.johnson@example.com','mypassword');

DELIMITER //
CREATE PROCEDURE UserType(IN id INT)
BEGIN
  SELECT name, type FROM Users WHERE user_id = id;
END //
DELIMITER ;

CALL UserType(3)

DELIMITER // 
CREATE PROCEDURE insert_order (IN u_order_date DATE, IN u_user_id INT, IN u_product_name VARCHAR(100), IN u_quantity INT, IN u_total_price DECIMAL(10, 2))
BEGIN
    INSERT INTO Orders (order_date, user_id, product_name, quantity, total_price)
    VALUES (u_order_date, u_user_id, u_product_name, u_quantity, u_total_price);
END //
DELIMITER ;

SELECT DISTINCT product_name, product_id FROM Products p INNER JOIN Orders o USING (product_name) WHERE user_id = 3;

DROP TABLE IF EXISTS UserFavourites;
CREATE TABLE UserFavourites (
	user_id INT not null,
    product_id int NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE ON UPDATE CASCADE,
    primary key (user_id, product_id)
);

SELECT * FROM UserFavourites;

INSERT INTO UserFavourites VALUES (3, 101);


CREATE TABLE payment (
	payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    addressline VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    zipcode INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

SELECT * FROM payment;

DELETE FROM payment WHERE user_id = 5;



 SELECT * FROM Users;
 SELECT * FROM Products;
 SELECT * FROM Orders;
 













