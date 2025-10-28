
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
    HashedPassword varchar(100),
    roleId INT

    FOREIGN KEY (roleId) REFERENCES Roles(roleId)
);

/*3. Add a default Administrator and strong password default...*/

CREATE TABLE IF NOT EXISTS Icons(
    iconId INT AUTO_INCREMENT PRIMARY KEY,
    iconPath varchar(255)
);

CREATE TABLE IF NOT EXISTS Category(
    categoryId INT AUTO_INCREMENT,
    categoryName varchar(255)
);

CREATE TABLE IF NOT EXISTS Products(
    productId INT AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL,
    productName varchar(255),
    iconID INT,
    totalCount INT,

    FOREIGN KEY iconPath REFERENCES Icons(iconID)     
);

/* Many to many  instance*/ 

CREATE TABLE IF NOT EXISTS ProductCategory(
    productCategoryId INT AUTO_INCREMENT PRIMARY KEY,
    productId INT,
    categoryId INT,

    FOREIGN KEY productId REFERENCES Products(productId),
    FOREIGN KEY categoryId REFERENCES Category(categoryId)
);

/*Many to many instance */


7. Create promotions db
8. Create invoice db
9. Create records db