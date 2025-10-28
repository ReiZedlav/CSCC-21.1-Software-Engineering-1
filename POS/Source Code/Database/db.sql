
CREATE DATABASE POS

USE POS

//to do list

1. create first Users db. DONE
2. then roles. DONE

CREATE TABLE Roles(
    roleId INT AUTO_INCREMENT PRIMARY KEY,
    roleName varchar(100)
);

//insert into roles Cashier and Administrator

CREATE TABLE Users(
    userID INT AUTO_INCREMENT PRIMARY KEY,
    firstName varchar(100),
    lastName varchar(100),
    userName varchar(100) UNIQUE,
    HashedPassword varchar(100),
    roleId INT

    FOREIGN KEY (roleId) REFERENCES Roles(roleId)
);

3. Add a default Administrator and strong password default...





4. Create products db
5. Create category db
6. Create product category Many to many 

7. Create promotions db
8. Create invoice db
9. Create records db