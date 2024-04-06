-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: leaveease
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` varchar(100) DEFAULT NULL,
  `faculty_name` varchar(200) DEFAULT NULL,
  `ThisHappened` text,
  PRIMARY KEY (`contact_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (3,'101','Tejaswi','Problem with your website please check them');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_details`
--

DROP TABLE IF EXISTS `faculty_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_details` (
  `faculty_id` int NOT NULL,
  `Username` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Phone_Number` varchar(15) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `Role` varchar(255) NOT NULL,
  `Verification` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`faculty_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_details`
--

LOCK TABLES `faculty_details` WRITE;
/*!40000 ALTER TABLE `faculty_details` DISABLE KEYS */;
INSERT INTO `faculty_details` VALUES (101,'Tejaswi','bodapatitejaswipratap8@gmail.com','Tejaswi123','7893967878','Guntur','Teacher',1),(135,'Srikanth','Srikanth123@gmail.com','Srikanth','9867899381','Guntur','Teacher',1);
/*!40000 ALTER TABLE `faculty_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ho_details`
--

DROP TABLE IF EXISTS `ho_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ho_details` (
  `AdminCode` int NOT NULL,
  `FullName` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Verification` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`AdminCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ho_details`
--

LOCK TABLES `ho_details` WRITE;
/*!40000 ALTER TABLE `ho_details` DISABLE KEYS */;
INSERT INTO `ho_details` VALUES (501,'Tejaswi Pratap','bodapatitejaswipratap8@gmail.com','Tejaswi',1);
/*!40000 ALTER TABLE `ho_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaveapplications`
--

DROP TABLE IF EXISTS `leaveapplications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaveapplications` (
  `leave_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `from` date NOT NULL,
  `to` date NOT NULL,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `reason` varchar(100) DEFAULT NULL,
  `allocated_leaves` int DEFAULT '12',
  `leaves_taken` int DEFAULT NULL,
  PRIMARY KEY (`leave_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaveapplications`
--

LOCK TABLES `leaveapplications` WRITE;
/*!40000 ALTER TABLE `leaveapplications` DISABLE KEYS */;
INSERT INTO `leaveapplications` VALUES (1,101,'2024-04-05','2024-04-30','approved','sickleave',12,25),(3,135,'2024-04-04','2024-04-19','rejected','vacation',12,15),(4,135,'2024-04-04','2024-04-09','rejected','casual',12,0),(5,101,'2024-04-18','2024-04-25','approved','casual',12,7);
/*!40000 ALTER TABLE `leaveapplications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workload`
--

DROP TABLE IF EXISTS `workload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workload` (
  `workload_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `workload_description` text NOT NULL,
  `submission_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','urgent','completed') DEFAULT NULL,
  `acceptance_date` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`workload_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `workload_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty_details` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workload`
--

LOCK TABLES `workload` WRITE;
/*!40000 ALTER TABLE `workload` DISABLE KEYS */;
INSERT INTO `workload` VALUES (6,101,'Give 2nd year students notes.','2024-04-04 10:55:00','pending','2024-04-10 10:55:00'),(7,135,'Complete the first unit for first years in all subjects','2024-04-01 11:07:00','urgent','2024-05-01 11:07:00'),(8,101,'Take students to lab','2024-04-04 11:40:00','completed','2024-04-04 11:40:00'),(9,101,'Take students to sports','2024-04-04 11:59:00','completed','2024-04-04 11:59:00');
/*!40000 ALTER TABLE `workload` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-06 12:04:47
