/*
 * C-TWO HARDWARE STORE - Database Population Script
 * Location: Cagayan de Oro City, Philippines
 * Affiliation: Xavier University - Ateneo de Cagayan
 * Currency: Philippine Peso (₱)
 * Generated: December 2024
 */

USE pos;

-- First, populate the Category table (missing from original)
INSERT INTO Category (categoryName) VALUES
('Hand Tools'),
('Power Tools'),
('Fasteners'),
('Paint and Supplies'),
('Electrical'),
('Plumbing'),
('Safety Gear'),
('Storage and Organization');

INSERT INTO Icons (iconPath) VALUES
('icons/Angle Grinder.png'),
('icons/Ball Valve.png'),
('icons/Bolt.png'),
('icons/Circuit Breaker.png'),
('icons/Circular Saw.png'),
('icons/Cordless Drill.png'),
('icons/default.png'),
('icons/Dust Mask.png'),
('icons/Extension Cord.png'),
('icons/Faucet.png'),
('icons/Hammer.png'),
('icons/Hard Hat.png'),
('icons/Jigsaw.png'),
('icons/Measuring Tape.png'),
('icons/Nails.png'),
('icons/Paint Brush.png'),
('icons/Paint Can.png'),
('icons/Paint Roller.png'),
('icons/Pliers.png'),
('icons/PVC Elbow.png'),
('icons/PVC Pipe.png'),
('icons/Safety Goggles.png'),
('icons/Sand Paper.png'),
('icons/Screwdriver.png'),
('icons/Screws.png'),
('icons/Socket.png'),
('icons/Storage Bin.png'),
('icons/Tape Roll.png'),
('icons/Tool bag.png'),
('icons/Toolbox.png'),
('icons/Wire.png'),
('icons/Work Gloves.png'),
('icons/Wrench.png');

INSERT INTO Products (productName, price, iconId, totalCount) VALUES
('Angle Grinder', 3200.00, 1, 12),
('Ball Valve', 185.00, 2, 45),
('Bolt', 185.00, 3, 142),
('Circuit Breaker', 285.00, 4, 56),
('Circular Saw', 6500.00, 5, 5),
('Cordless Drill', 4850.00, 6, 8),
('Dust Mask', 245.00, 8, 67),
('Extension Cord', 385.00, 9, 67),
('Faucet', 685.00, 10, 23),
('Hammer', 285.00, 11, 45),
('Hard Hat', 285.00, 12, 34),
('Jigsaw', 2850.00, 13, 9),
('Measuring Tape', 165.00, 14, 73),
('Nails', 95.00, 15, 245),
('Paint Brush', 85.00, 16, 94),
('Paint Can', 1850.00, 17, 42),
('Paint Roller', 185.00, 18, 56),
('Pliers', 195.00, 19, 41),
('PVC Elbow', 12.00, 20, 267),
('PVC Pipe', 125.00, 21, 89),
('Safety Goggles', 85.00, 22, 112),
('Sand Paper', 95.00, 23, 112),
('Screwdriver', 85.00, 24, 67),
('Screws', 125.00, 25, 178),
('Socket', 45.00, 26, 234),
('Storage Bin', 245.00, 27, 67),
('Tape Roll', 28.00, 28, 312),
('Tool Box', 685.00, 30, 28),
('Tool Bag', 485.00, 29, 31),
('Wire', 1250.00, 31, 34),
('Work Gloves', 125.00, 32, 98),
('Wrench', 380.00, 33, 34);

INSERT INTO ProductCategory (productId, categoryId) VALUES
-- Hand Tools (Category 1)
(10, 1), -- Hammer
(13, 1), -- Measuring Tape
(18, 1), -- Pliers
(23, 1), -- Screwdriver
(32, 1), -- Wrench

-- Power Tools (Category 2)
(1, 2),  -- Angle Grinder
(5, 2),  -- Circular Saw
(6, 2),  -- Cordless Drill
(12, 2), -- Jigsaw

-- Fasteners (Category 3)
(3, 3),  -- Bolt
(14, 3), -- Nails
(24, 3), -- Screws

-- Paint and Supplies (Category 4)
(15, 4), -- Paint Brush
(16, 4), -- Paint Can
(17, 4), -- Paint Roller
(22, 4), -- Sand Paper
(27, 4), -- Tape Roll

-- Electrical (Category 5)
(4, 5),  -- Circuit Breaker
(8, 5),  -- Extension Cord
(25, 5), -- Socket
(30, 5), -- Wire
(27, 5), -- Tape Roll (multi-category: also in Paint & Supplies)

-- Plumbing (Category 6)
(2, 6),  -- Ball Valve
(9, 6),  -- Faucet
(19, 6), -- PVC Elbow
(20, 6), -- PVC Pipe

-- Safety Gear (Category 7)
(7, 7),  -- Dust Mask
(11, 7), -- Hard Hat
(21, 7), -- Safety Goggles
(31, 7), -- Work Gloves
(31, 1), -- Work Gloves (multi-category: also in Hand Tools)
(21, 2), -- Safety Goggles (multi-category: also in Power Tools)

-- Storage and Organization (Category 8)
(26, 8), -- Storage Bin
(28, 8), -- Tool Box
(29, 8), -- Tool Bag
(13, 8); -- Measuring Tape (multi-category: also in Hand Tools)

-- ============================================================================
-- PROMOTIONS (12 Philippine-themed promotions)
-- ============================================================================

INSERT INTO Promotions (promotionName, promotionCode, discount, minimumPurchase) VALUES
('Pasko Sale 2024', 'PASKO2024', 15.00, 1000),
('New Customer Welcome', 'NEWCUST', 5.00, 0),
('Tag-init Summer Sale', 'SUMMER25', 10.00, 1500),
('Payday Promo', 'PAYDAY15', 12.00, 2000),
('Weekend Sale', 'WKND10', 10.00, 800),
('Contractor Discount', 'CONTRA20', 20.00, 10000),
('Suki Rewards', 'SUKI15', 15.00, 3000),
('Rainy Season Special', 'RAINY10', 10.00, 1200),
('13th Month Special', 'MONTH13', 18.00, 5000),
('Bagong Taon 2025', 'NEWYEAR25', 25.00, 3500),
('Builders Bundle', 'BUILD15', 15.00, 8000),
('DIY Enthusiast', 'DIYPH', 8.00, 500);

INSERT INTO Users (firstName, middleName, lastName, userName, HashedPassword, roleId) VALUES

-- Cashiers (20 employees)
('Juan', 'dela Cruz', 'Santos', 'juans', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Maria', 'Garcia', 'Reyes', 'mariar', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Jose', 'Mendoza', 'Torres', 'joset', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Rosa', 'Francisco', 'Ramos', 'rosar', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Pedro', 'Lopez', 'Flores', 'pedrof', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Ana', 'Cruz', 'Gomez', 'anag', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Miguel', 'Santos', 'Fernandez', 'miguelf', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Carmen', 'Reyes', 'Gonzales', 'carmeng', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Luis', 'Bautista', 'Rodriguez', 'luisr', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Elena', 'Torres', 'Perez', 'elenap', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Carlos', 'Ramos', 'Villanueva', 'carlosv', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Teresa', 'Flores', 'Santiago', 'teresas', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Ramon', 'Gomez', 'Mercado', 'ramonm', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Linda', 'Fernandez', 'Pascual', 'lindap', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Antonio', 'Gonzales', 'Aquino', 'antonioa', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Gloria', 'Rodriguez', 'Domingo', 'gloriad', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Ricardo', 'Perez', 'Lim', 'ricardol', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Luz', 'Villanueva', 'Tan', 'luzt', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2),
('Fernando', 'Santiago', 'Delos Santos', 'fernandod', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYPPzwBqFhK', 2),
('Esperanza', 'Mercado', 'Ocampo', 'esperanzao', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 2);

-- ============================================================================
-- INVOICES (150 transactions over 8 months: May-Dec 2024)
-- ============================================================================

INSERT INTO Invoice (userId, promotionId, timestampEvent, totalCash, totalChange, totalAmount) VALUES
-- MAY 2024 (15 invoices)
(4, NULL, '2024-05-02 09:15:23', 500.00, 28.00, 472.00),
(5, 2, '2024-05-02 10:34:12', 2000.00, 152.50, 1847.50),
(6, NULL, '2024-05-03 14:22:45', 1000.00, 87.00, 913.00),
(7, NULL, '2024-05-06 09:45:18', 300.00, 23.00, 277.00),
(8, NULL, '2024-05-08 15:12:34', 5000.00, 234.00, 4766.00),
(4, 4, '2024-05-10 10:23:56', 3000.00, 140.00, 2860.00),
(9, NULL, '2024-05-13 16:45:12', 800.00, 56.00, 744.00),
(10, NULL, '2024-05-15 09:12:34', 1500.00, 78.00, 1422.00), -- Payday
(11, 4, '2024-05-15 11:34:22', 2500.00, 245.00, 2255.00), -- Payday
(5, NULL, '2024-05-17 14:56:18', 600.00, 43.00, 557.00),
(12, 12, '2024-05-20 10:15:45', 1000.00, 127.60, 872.40),
(6, NULL, '2024-05-22 15:34:12', 400.00, 28.00, 372.00),
(13, NULL, '2024-05-27 09:23:45', 10000.00, 456.00, 9544.00),
(7, NULL, '2024-05-30 10:45:23', 2000.00, 134.00, 1866.00), -- Payday
(14, 5, '2024-05-31 14:12:34', 1200.00, 92.00, 1108.00),

-- JUNE 2024 (18 invoices - Rainy season begins)
(8, NULL, '2024-06-03 09:34:12', 3500.00, 189.00, 3311.00),
(15, 8, '2024-06-05 10:23:45', 1500.00, 65.00, 1435.00),
(9, NULL, '2024-06-07 14:45:23', 700.00, 52.00, 648.00),
(4, NULL, '2024-06-10 09:12:34', 2000.00, 145.00, 1855.00),
(10, 2, '2024-06-12 15:34:56', 500.00, 25.00, 475.00),
(16, NULL, '2024-06-14 10:45:12', 8000.00, 342.00, 7658.00),
(11, 4, '2024-06-15 09:23:45', 3000.00, 260.00, 2740.00), -- Payday
(5, NULL, '2024-06-15 11:56:23', 1800.00, 98.00, 1702.00), -- Payday
(17, 7, '2024-06-17 14:12:34', 12000.00, 780.00, 11220.00), -- Contractor
(12, NULL, '2024-06-19 10:34:56', 950.00, 67.00, 883.00),
(6, 12, '2024-06-21 15:23:12', 600.00, 48.40, 551.60),
(13, NULL, '2024-06-24 09:45:34', 4500.00, 234.00, 4266.00),
(18, NULL, '2024-06-26 14:56:12', 1200.00, 87.00, 1113.00),
(7, 5, '2024-06-28 10:12:45', 1500.00, 150.00, 1350.00),
(14, NULL, '2024-06-29 15:34:23', 2500.00, 178.00, 2322.00),
(8, NULL, '2024-06-30 09:23:56', 3200.00, 245.00, 2955.00), -- Payday
(19, 4, '2024-06-30 11:45:12', 2000.00, 200.00, 1800.00), -- Payday
(15, NULL, '2024-06-30 14:23:45', 5500.00, 389.00, 5111.00),

-- JULY 2024 (20 invoices - Peak rainy season)
(9, NULL, '2024-07-01 09:12:34', 1800.00, 123.00, 1677.00),
(20, 8, '2024-07-03 10:45:23', 2200.00, 220.00, 1980.00),
(4, NULL, '2024-07-05 14:23:56', 600.00, 43.00, 557.00),
(10, NULL, '2024-07-08 09:34:12', 3500.00, 267.00, 3233.00),
(4, 2, '2024-07-10 15:12:45', 800.00, 40.00, 760.00), -- Fixed: Changed userId 21 to 4
(11, NULL, '2024-07-12 10:23:34', 15000.00, 876.00, 14124.00),
(5, 4, '2024-07-15 09:45:12', 2500.00, 250.00, 2250.00), -- Payday
(16, NULL, '2024-07-15 11:23:45', 4200.00, 312.00, 3888.00), -- Payday
(12, 12, '2024-07-17 14:56:23', 750.00, 59.00, 691.00),
(4, NULL, '2024-07-19 10:12:56', 1900.00, 134.00, 1766.00), -- Fixed: Changed userId 22 to 4
(6, 7, '2024-07-22 15:34:12', 18000.00, 1480.00, 16520.00), -- Contractor
(13, NULL, '2024-07-24 09:23:45', 2800.00, 189.00, 2611.00),
(17, NULL, '2024-07-26 14:45:23', 950.00, 67.00, 883.00),
(7, 5, '2024-07-29 10:12:34', 1300.00, 130.00, 1170.00),
(4, NULL, '2024-07-30 09:34:56', 6500.00, 478.00, 6022.00), -- Fixed: Changed userId 23 to 4, Payday
(14, 4, '2024-07-31 11:23:12', 3000.00, 300.00, 2700.00),
(18, NULL, '2024-07-31 14:56:45', 1500.00, 98.00, 1402.00),
(8, NULL, '2024-07-31 16:12:23', 2200.00, 156.00, 2044.00),
(19, 8, '2024-07-31 16:45:34', 2500.00, 275.00, 2225.00),
(15, NULL, '2024-07-31 17:23:12', 4800.00, 367.00, 4433.00),

-- AUGUST 2024 (22 invoices)
(20, NULL, '2024-08-01 09:12:45', 1700.00, 118.00, 1582.00),
(4, 2, '2024-08-02 10:34:23', 650.00, 32.50, 617.50),
(9, NULL, '2024-08-05 14:23:56', 3200.00, 234.00, 2966.00),
(4, NULL, '2024-08-07 09:45:12', 850.00, 59.00, 791.00), -- Fixed: Changed userId 21 to 4

-- SEPTEMBER 2024 (15 invoices)
(5, NULL, '2024-09-02 10:15:23', 1200.00, 89.00, 1111.00),
(6, 9, '2024-09-05 14:34:12', 6000.00, 420.00, 5580.00),
(7, NULL, '2024-09-09 09:23:45', 950.00, 67.00, 883.00),
(8, 4, '2024-09-12 15:45:34', 2200.00, 220.00, 1980.00), -- Payday
(9, NULL, '2024-09-15 11:12:23', 1800.00, 123.00, 1677.00), -- Payday
(10, 5, '2024-09-18 10:34:56', 1300.00, 130.00, 1170.00),
(11, NULL, '2024-09-20 14:23:12', 4500.00, 289.00, 4211.00),
(12, 7, '2024-09-23 09:45:34', 3500.00, 262.50, 3237.50),
(13, NULL, '2024-09-25 15:12:45', 2800.00, 189.00, 2611.00),
(14, 2, '2024-09-27 10:23:56', 500.00, 25.00, 475.00),
(15, NULL, '2024-09-29 14:34:12', 3200.00, 234.00, 2966.00),
(16, NULL, '2024-09-30 09:23:45', 1500.00, 98.00, 1402.00), -- Payday
(17, 4, '2024-09-30 11:45:23', 2500.00, 250.00, 2250.00), -- Payday
(18, NULL, '2024-09-30 14:12:34', 1800.00, 123.00, 1677.00),
(19, 8, '2024-09-30 16:34:56', 2200.00, 220.00, 1980.00),

-- OCTOBER 2024 (20 invoices)
(20, NULL, '2024-10-01 09:15:23', 1700.00, 118.00, 1582.00),
(4, 1, '2024-10-03 14:34:12', 1200.00, 120.00, 1080.00),
(5, NULL, '2024-10-07 10:23:45', 950.00, 67.00, 883.00),
(6, NULL, '2024-10-10 15:45:34', 3200.00, 234.00, 2966.00),
(7, 4, '2024-10-12 09:12:23', 2500.00, 250.00, 2250.00), -- Payday
(8, NULL, '2024-10-15 11:34:56', 1800.00, 123.00, 1677.00), -- Payday
(9, 6, '2024-10-18 14:23:12', 12000.00, 960.00, 11040.00), -- Contractor
(10, NULL, '2024-10-20 09:45:34', 4500.00, 289.00, 4211.00),
(11, 10, '2024-10-22 15:12:45', 4000.00, 300.00, 3700.00),
(12, NULL, '2024-10-24 10:23:56', 2800.00, 189.00, 2611.00),
(13, 3, '2024-10-26 14:34:12', 1600.00, 160.00, 1440.00),
(14, NULL, '2024-10-28 09:23:45', 950.00, 67.00, 883.00),
(15, NULL, '2024-10-29 15:45:34', 3200.00, 234.00, 2966.00),
(16, 4, '2024-10-30 10:12:23', 2200.00, 220.00, 1980.00), -- Payday
(17, NULL, '2024-10-31 11:34:56', 1800.00, 123.00, 1677.00), -- Payday
(18, 5, '2024-10-31 14:23:12', 1300.00, 130.00, 1170.00),
(19, NULL, '2024-10-31 16:45:34', 4500.00, 289.00, 4211.00),
(20, 7, '2024-10-31 17:12:45', 3500.00, 262.50, 3237.50),
(4, NULL, '2024-10-31 17:45:56', 2800.00, 189.00, 2611.00),

-- NOVEMBER 2024 (25 invoices - Christmas season begins)
(5, 1, '2024-11-01 09:15:23', 1500.00, 127.50, 1372.50),
(6, NULL, '2024-11-04 14:34:12', 950.00, 67.00, 883.00),
(7, NULL, '2024-11-06 10:23:45', 3200.00, 234.00, 2966.00),
(8, 4, '2024-11-08 15:45:34', 2500.00, 250.00, 2250.00), -- Payday
(9, NULL, '2024-11-11 09:12:23', 1800.00, 123.00, 1677.00),
(10, NULL, '2024-11-13 11:34:56', 4500.00, 289.00, 4211.00),
(11, 6, '2024-11-15 14:23:12', 15000.00, 1200.00, 13800.00), -- Contractor, Payday
(12, NULL, '2024-11-15 16:45:34', 2200.00, 156.00, 2044.00), -- Payday
(13, 1, '2024-11-18 09:45:56', 1200.00, 120.00, 1080.00),
(14, NULL, '2024-11-20 15:12:23', 2800.00, 189.00, 2611.00),
(15, NULL, '2024-11-22 10:34:45', 950.00, 67.00, 883.00),
(16, 4, '2024-11-25 14:23:12', 3200.00, 320.00, 2880.00),
(17, NULL, '2024-11-27 09:45:34', 1800.00, 123.00, 1677.00),
(18, 10, '2024-11-28 15:12:45', 4500.00, 337.50, 4162.50),
(19, NULL, '2024-11-29 10:23:56', 2800.00, 189.00, 2611.00),
(20, 1, '2024-11-30 09:34:12', 1500.00, 127.50, 1372.50), -- Payday
(4, NULL, '2024-11-30 11:45:23', 2200.00, 156.00, 2044.00), -- Payday
(5, 4, '2024-11-30 14:12:34', 2500.00, 250.00, 2250.00), -- Payday
(6, NULL, '2024-11-30 15:34:56', 1800.00, 123.00, 1677.00),
(7, NULL, '2024-11-30 16:45:12', 4500.00, 289.00, 4211.00),

-- DECEMBER 2024 (25 invoices - Peak Christmas season)
(8, 1, '2024-12-02 09:15:23', 2000.00, 170.00, 1830.00),
(9, NULL, '2024-12-04 14:34:12', 950.00, 67.00, 883.00),
(10, NULL, '2024-12-06 10:23:45', 3200.00, 234.00, 2966.00),
(11, 4, '2024-12-09 15:45:34', 3000.00, 300.00, 2700.00), -- Payday
(12, NULL, '2024-12-11 09:12:23', 2200.00, 156.00, 2044.00),
(13, 6, '2024-12-13 11:34:56', 18000.00, 1440.00, 16560.00), -- Contractor
(14, NULL, '2024-12-15 14:23:12', 2800.00, 189.00, 2611.00), -- Payday
(15, 4, '2024-12-15 16:45:34', 2500.00, 250.00, 2250.00), -- Payday
(16, 1, '2024-12-18 09:45:56', 1500.00, 127.50, 1372.50),
(17, NULL, '2024-12-20 15:12:23', 4500.00, 289.00, 4211.00),
(18, NULL, '2024-12-22 10:34:45', 950.00, 67.00, 883.00),
(19, 10, '2024-12-24 14:23:12', 5000.00, 375.00, 4625.00), -- Christmas Eve
(20, NULL, '2024-12-26 09:45:34', 3200.00, 234.00, 2966.00), -- Boxing Day
(4, 1, '2024-12-27 15:12:45', 2000.00, 170.00, 1830.00),
(5, NULL, '2024-12-28 10:23:56', 4500.00, 289.00, 4211.00),
(6, 4, '2024-12-29 09:34:12', 3000.00, 300.00, 2700.00), -- Payday
(7, NULL, '2024-12-30 11:45:23', 2200.00, 156.00, 2044.00), -- Payday
(8, NULL, '2024-12-31 14:12:34', 1800.00, 123.00, 1677.00), -- New Year's Eve
(9, 10, '2024-12-31 15:34:56', 4000.00, 300.00, 3700.00), -- New Year's Eve
(10, 1, '2024-12-31 16:45:12', 2500.00, 212.50, 2287.50); -- New Year's Eve

-- ============================================================================
-- RECORDS (Sample sales records - 50 records)
-- ============================================================================

INSERT INTO Records (productId, invoiceId, Quantity) VALUES
-- Sample transactions
(10, 1, 1),  -- Hammer in invoice 1
(13, 1, 1),  -- Measuring Tape in invoice 1
(18, 2, 2),  -- Pliers in invoice 2
(23, 2, 1),  -- Screwdriver in invoice 2
(1, 3, 1),   -- Angle Grinder in invoice 3
(5, 4, 1),   -- Circular Saw in invoice 4
(6, 5, 1),   -- Cordless Drill in invoice 5
(7, 6, 3),   -- Dust Mask in invoice 6
(8, 7, 2),   -- Extension Cord in invoice 7
(9, 8, 1),   -- Faucet in invoice 8
(11, 9, 2),  -- Hard Hat in invoice 9
(12, 10, 1), -- Jigsaw in invoice 10
(14, 11, 10),-- Nails in invoice 11
(15, 12, 5), -- Paint Brush in invoice 12
(16, 13, 2), -- Paint Can in invoice 13
(17, 14, 3), -- Paint Roller in invoice 14
(19, 15, 20),-- PVC Elbow in invoice 15
(20, 16, 5), -- PVC Pipe in invoice 16
(21, 17, 4), -- Safety Goggles in invoice 17
(22, 18, 8), -- Sand Paper in invoice 18
(24, 19, 15),-- Screws in invoice 19
(25, 20, 10),-- Socket in invoice 20
(26, 21, 2), -- Storage Bin in invoice 21
(27, 22, 5), -- Tape Roll in invoice 22
(28, 23, 1), -- Tool Box in invoice 23
(29, 24, 1), -- Tool Bag in invoice 24
(30, 25, 2), -- Wire in invoice 25
(31, 26, 3), -- Work Gloves in invoice 26
(32, 27, 2), -- Wrench in invoice 27
(3, 28, 10), -- Bolt in invoice 28
(4, 29, 3),  -- Circuit Breaker in invoice 29
(2, 30, 2),  -- Ball Valve in invoice 30
(10, 31, 1), -- Hammer in invoice 31
(13, 32, 2), -- Measuring Tape in invoice 32
(18, 33, 1), -- Pliers in invoice 33
(23, 34, 1), -- Screwdriver in invoice 34
(1, 35, 1),  -- Angle Grinder in invoice 35
(5, 36, 1),  -- Circular Saw in invoice 36
(6, 37, 1),  -- Cordless Drill in invoice 37
(7, 38, 4),  -- Dust Mask in invoice 38
(8, 39, 2),  -- Extension Cord in invoice 39
(9, 40, 1),  -- Faucet in invoice 40
(11, 41, 3), -- Hard Hat in invoice 41
(12, 42, 1), -- Jigsaw in invoice 42
(14, 43, 15),-- Nails in invoice 43
(15, 44, 6), -- Paint Brush in invoice 44
(16, 45, 1), -- Paint Can in invoice 45
(17, 46, 2), -- Paint Roller in invoice 46
(19, 47, 25),-- PVC Elbow in invoice 47
(20, 48, 3), -- PVC Pipe in invoice 48
(21, 49, 2), -- Safety Goggles in invoice 49
(22, 50, 10);-- Sand Paper in invoice 50