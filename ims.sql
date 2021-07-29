-- phpMyAdmin SQL Dump
-- version 4.4.15.9
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 02, 2019 at 11:10 AM
-- Server version: 5.6.37
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ums`
--

-- --------------------------------------------------------

--
-- Table structure for table `cashReceipts`
--

CREATE TABLE IF NOT EXISTS `cashReceipts` (
  `cashReceiptID` int(11) NOT NULL,
  `dueOrderID` int(11) DEFAULT NULL,
  `receptionistID` int(11) DEFAULT NULL,
  `duePaidDate` date DEFAULT NULL,
  `duePaidAmount` decimal(12,2) NOT NULL,
  `duePaidMode` varchar(16) NOT NULL,
  `dueReceivedFrom` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE IF NOT EXISTS `customers` (
  `customerID` int(11) NOT NULL,
  `customerName` varchar(64) NOT NULL,
  `customerEmail` varchar(128) NOT NULL,
  `customerContact` varchar(11) NOT NULL,
  `customerZip` varchar(10) NOT NULL,
  `customerCity` varchar(20) NOT NULL,
  `customerDistrict` varchar(20) NOT NULL,
  `customerState` varchar(20) NOT NULL,
  `customerCountry` varchar(20) NOT NULL,
  `customerDues` decimal(12,2) DEFAULT NULL,
  `customerDiscount` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`customerID`, `customerName`, `customerEmail`, `customerContact`, `customerZip`, `customerCity`, `customerDistrict`, `customerState`, `customerCountry`, `customerDues`, `customerDiscount`) VALUES
(1, 'CHINMAY MISHRA', 'CHINMAYMISHRA.FALNA@GMAIL.COM', '8690736210', '306116', 'FALNA', 'PALI', 'RAJASTHAN', 'INDIA', '0.00', '0.00');

-- --------------------------------------------------------

--
-- Table structure for table `orderProducts`
--

CREATE TABLE IF NOT EXISTS `orderProducts` (
  `orderProductID` int(11) NOT NULL,
  `orderID` int(11) DEFAULT NULL,
  `productID` int(11) DEFAULT NULL,
  `productQuantity` int(11) NOT NULL,
  `productStatus` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE IF NOT EXISTS `orders` (
  `orderID` int(11) NOT NULL,
  `customerID` int(11) DEFAULT NULL,
  `orderDate` date DEFAULT NULL,
  `orderDiscount` decimal(12,2) DEFAULT NULL,
  `orderTotal` decimal(12,2) NOT NULL,
  `orderNetPaid` decimal(12,2) NOT NULL,
  `orderStatus` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `productID` int(11) NOT NULL,
  `productName` varchar(64) NOT NULL,
  `productCostPrice` decimal(12,2) NOT NULL,
  `productSellPrice` decimal(12,2) NOT NULL,
  `productQuantity` int(11) NOT NULL,
  `productDiscount` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`productID`, `productName`, `productCostPrice`, `productSellPrice`, `productQuantity`, `productDiscount`) VALUES
(1, 'LENOVO LAPTOP', '30000.00', '32000.00', 200, '100.00');

-- --------------------------------------------------------

--
-- Table structure for table `receptionists`
--

CREATE TABLE IF NOT EXISTS `receptionists` (
  `receptionistID` int(11) NOT NULL,
  `receptionistName` varchar(64) NOT NULL,
  `receptionistEmail` varchar(128) NOT NULL,
  `receptionistContact` varchar(11) NOT NULL,
  `receptionistPassword` varchar(128) NOT NULL,
  `receptionistDigitalSign` varchar(64) NOT NULL,
  `receptionistRole` varchar(64) NOT NULL,
  `receptionistStatus` varchar(64) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `receptionists`
--

INSERT INTO `receptionists` (`receptionistID`, `receptionistName`, `receptionistEmail`, `receptionistContact`, `receptionistPassword`, `receptionistDigitalSign`, `receptionistRole`, `receptionistStatus`) VALUES
(1, 'CHINMAY MISHRA', 'CHINMAYMISHRA.FALNA@GMAIL.COM', '8690736210', 'chinmaymishra', 'ChinmaySignature.png', 'ADMIN', 'ACTIVATE');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cashReceipts`
--
ALTER TABLE `cashReceipts`
  ADD PRIMARY KEY (`cashReceiptID`),
  ADD KEY `dueOrderID` (`dueOrderID`),
  ADD KEY `receptionistID` (`receptionistID`);

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customerID`),
  ADD UNIQUE KEY `customerEmail` (`customerEmail`);

--
-- Indexes for table `orderProducts`
--
ALTER TABLE `orderProducts`
  ADD PRIMARY KEY (`orderProductID`),
  ADD KEY `orderID` (`orderID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`orderID`),
  ADD KEY `customerID` (`customerID`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`productID`);

--
-- Indexes for table `receptionists`
--
ALTER TABLE `receptionists`
  ADD PRIMARY KEY (`receptionistID`),
  ADD UNIQUE KEY `receptionistEmail` (`receptionistEmail`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cashReceipts`
--
ALTER TABLE `cashReceipts`
  MODIFY `cashReceiptID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `customerID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `orderProducts`
--
ALTER TABLE `orderProducts`
  MODIFY `orderProductID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `orderID` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `productID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `receptionists`
--
ALTER TABLE `receptionists`
  MODIFY `receptionistID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `cashReceipts`
--
ALTER TABLE `cashReceipts`
  ADD CONSTRAINT `cashreceipts_ibfk_1` FOREIGN KEY (`dueOrderID`) REFERENCES `orders` (`orderID`),
  ADD CONSTRAINT `cashreceipts_ibfk_2` FOREIGN KEY (`receptionistID`) REFERENCES `receptionists` (`receptionistID`);

--
-- Constraints for table `orderProducts`
--
ALTER TABLE `orderProducts`
  ADD CONSTRAINT `orderproducts_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`),
  ADD CONSTRAINT `orderproducts_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `products` (`productID`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `customers` (`customerID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
