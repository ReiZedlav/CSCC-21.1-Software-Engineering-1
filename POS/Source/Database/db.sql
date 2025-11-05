
CREATE DATABASE IF NOT EXISTS POS;

USE POS;

CREATE TABLE IF NOT EXISTS Roles(
    roleId INT PRIMARY KEY,
    roleName varchar(100)
);

INSERT INTO Roles VALUES
    (1,"Administrator"),
    (2,"Cashier");

CREATE TABLE IF NOT EXISTS Users(
    userId INT AUTO_INCREMENT PRIMARY KEY,
    firstName varchar(100),
    middleName varchar(100),
    lastName varchar(100),
    userName varchar(100) UNIQUE,
    HashedPassword varchar(255) NOT NULL,
    roleId INT NOT NULL,

    FOREIGN KEY (roleId) REFERENCES Roles(roleId)
);

/*3. Add a default Administrator and strong password default...*/

INSERT INTO Users (firstName,middleName,lastName,userName,HashedPassword,roleId) 
    VALUES
        ("Andrei Albertson","Lungay","Valdez","admin","admin",1);

CREATE TABLE IF NOT EXISTS Icons(
    iconId INT AUTO_INCREMENT PRIMARY KEY,
    iconPath varchar(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS Category(
    categoryId INT AUTO_INCREMENT PRIMARY KEY,
    categoryName varchar(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS Products(
    productId INT AUTO_INCREMENT PRIMARY KEY,
    productName varchar(255) NOT null,
    price DECIMAL(10,2) NOT null,
    iconId INT,
    totalCount INT NOT NULL DEFAULT 0,

    CHECK (totalCount >= 0),
    CHECK (price >= 1),

    FOREIGN KEY (iconId) REFERENCES Icons(iconId)     
);

/* Many to many  instance*/ 

CREATE TABLE IF NOT EXISTS ProductCategory(
    productCategoryId INT AUTO_INCREMENT PRIMARY KEY,
    productId INT,
    categoryId INT,

    FOREIGN KEY (productId) REFERENCES Products(productId),
    FOREIGN KEY (categoryId) REFERENCES Category(categoryId)
);

/*Many to many instance */

CREATE TABLE IF NOT EXISTS Promotions(
    promotionId INT AUTO_INCREMENT PRIMARY KEY,
    promotionName varchar(255),
    promotionCode varchar(10) UNIQUE,
    discount DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS Invoice(
    invoiceId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT, /* To identify who was the cashier*/ 
    promotionId INT DEFAULT null, /*promotion is optional*/
    timestampEvent TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    totalCash DECIMAL(10,2) NOT NULL,
    totalChange DECIMAL(10,2) NOT NULL,
    totalAmount DECIMAL(10,2) NOT NULL, 

    FOREIGN KEY (userId) REFERENCES Users(userId),
    FOREIGN KEY (promotionId) REFERENCES Promotions(promotionId)
);

CREATE TABLE IF NOT EXISTS Records(
    recordId INT AUTO_INCREMENT PRIMARY KEY,
    productId INT NOT NULL,
    invoiceId INT NOT NULL,
    Quantity INT NOT NULL,

    FOREIGN KEY (productId) REFERENCES Products(productId),
    FOREIGN KEY (invoiceId) REFERENCES Invoice(invoiceId)
);


