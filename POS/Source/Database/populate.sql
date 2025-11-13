
/*SQL Script to populate the empty database with test data */

INSERT INTO Users (firstName, middleName, lastName, userName, HashedPassword, roleId) VALUES
('John', 'A.', 'Drillman', 'johnd', 'hashed_password_1', 2),
('Jane', 'B.', 'Hammer', 'janeh', 'hashed_password_2', 2),
('Michael', 'C.', 'Screw', 'michaels', 'hashed_password_3', 2),
('Emily', 'D.', 'Wrench', 'emilyw', 'hashed_password_4', 2),
('Daniel', 'E.', 'Saw', 'daniels', 'hashed_password_5', 2),
('Olivia', 'F.', 'Pliers', 'oliviap', 'hashed_password_6', 2),
('Matthew', 'G.', 'Nail', 'matthewn', 'hashed_password_7', 2),
('Sophia', 'H.', 'Bolt', 'sophiab', 'hashed_password_8', 2),
('Andrew', 'I.', 'Sander', 'andrews', 'hashed_password_9', 2),
('Isabella', 'J.', 'Tape', 'isabellat', 'hashed_password_10', 2),
('Christopher', 'K.', 'Level', 'chrisl', 'hashed_password_11', 2),
('Mia', 'L.', 'Paint', 'miap', 'hashed_password_12', 2),
('Joshua', 'M.', 'Drill', 'joshuad', 'hashed_password_13', 2),
('Ava', 'N.', 'Sawblade', 'avas', 'hashed_password_14', 2),
('Ethan', 'O.', 'Screwdriver', 'ethans', 'hashed_password_15', 2),
('Charlotte', 'P.', 'Wrenchset', 'charlottew', 'hashed_password_16', 2),
('Alexander', 'Q.', 'Hammerhead', 'alexh', 'hashed_password_17', 2),
('Amelia', 'R.', 'Chisel', 'ameliac', 'hashed_password_18', 2),
('William', 'S.', 'Workbench', 'willw', 'hashed_password_19', 2),
('Harper', 'T.', 'Toolbox', 'harpert', 'hashed_password_20', 2);

INSERT INTO Icons (iconPath) VALUES
('icons/hammer.png'),
('icons/screwdriver.png'),
('icons/wrench.png'),
('icons/drill.png'),
('icons/saw.png'),
('icons/pliers.png'),
('icons/nails.png'),
('icons/bolts.png'),
('icons/tape.png'),
('icons/paint.png'),
('icons/paintbrush.png'),
('icons/sander.png'),
('icons/chisel.png'),
('icons/workbench.png'),
('icons/toolbox.png');

INSERT INTO Category (categoryName) VALUES
('Hand Tools'),
('Power Tools'),
('Fasteners'),
('Paint & Supplies'),
('Electrical'),
('Plumbing'),
('Safety Gear'),
('Storage & Organization');

INSERT INTO Products (productName, price, iconId, totalCount) VALUES
('Hammer', 15.00, 1, 50),
('Screwdriver Set', 25.00, 2, 40),
('Adjustable Wrench', 18.00, 3, 30),
('Cordless Drill', 80.00, 4, 20),
('Circular Saw', 120.00, 5, 15),
('Pliers', 12.00, 6, 45),
('Box of Nails', 5.00, 7, 100),
('Box of Bolts', 6.00, 8, 100),
('Electrical Tape', 3.00, 9, 60),
('White Paint 1L', 20.00, 10, 25),
('Paintbrush 3in', 7.00, 11, 50),
('Orbital Sander', 90.00, 12, 10),
('Wood Chisel', 14.00, 13, 35),
('Workbench', 200.00, 14, 5),
('Toolbox', 50.00, 15, 20);

INSERT INTO ProductCategory (productId, categoryId) VALUES
(1, 1),  
(2, 1),  
(3, 1),  
(4, 2),  
(5, 2),  
(6, 1),  
(7, 3),  
(8, 3),  
(9, 5),  
(10, 4), 
(11, 4), 
(12, 2),
(13, 1), 
(14, 8), 
(15, 8), 
(1, 5),  
(7, 1),  
(4, 1),  
(12, 1); 

INSERT INTO Promotions (promotionName, promotionCode, discount,minimumPurchase) VALUES
('Spring Sale', 'SPRING10', 10.00,100),
('Black Friday', 'BLKFRI20', 20.00,3000),
('New Customer', 'NEW5', 5.00,0),
('Weekend Special', 'WKND15', 15.00,150),
('Clearance', 'CLEAR30', 30.00,700);

INSERT INTO Invoice (userId, promotionId, totalCash, totalChange, totalAmount) VALUES
(1, 1, 150.00, 0.00, 150.00),
(2, NULL, 85.00, 5.00, 80.00),
(3, 2, 200.00, 0.00, 160.00),
(4, 3, 50.00, 0.00, 47.50),
(5, NULL, 120.00, 0.00, 120.00),
(6, 4, 75.00, 0.00, 63.75),
(7, NULL, 60.00, 0.00, 60.00),
(8, 5, 300.00, 0.00, 210.00),
(9, 1, 90.00, 0.00, 81.00),
(10, NULL, 45.00, 0.00, 45.00);

INSERT INTO Records (productId, invoiceId, Quantity) VALUES
(1, 1, 2),   
(4, 1, 1),   
(7, 2, 5),   
(10, 2, 1), 
(5, 3, 1),   
(12, 3, 1),  
(2, 4, 1),   
(3, 4, 1),   
(15, 5, 1),  
(14, 5, 1),  
(6, 6, 3),   
(8, 6, 2),   
(9, 7, 4),   
(13, 8, 2), 
(11, 8, 2), 
(1, 9, 1),   
(2, 9, 1),   
(10, 10, 1), 
(5, 10, 1);  