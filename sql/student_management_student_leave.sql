-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: student_management
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `student_leave`
--

DROP TABLE IF EXISTS `student_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_leave` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `student_name` varchar(100) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `reason` text NOT NULL,
  `leave_campus` tinyint(1) NOT NULL DEFAULT '0',
  `status` enum('待通过','待销假','已销假','已驳回') NOT NULL DEFAULT '待通过',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin_comment` text,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `student_leave___fk` (`student_name`),
  CONSTRAINT `student_leave___fk` FOREIGN KEY (`student_name`) REFERENCES `users` (`username`),
  CONSTRAINT `student_leave_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_leave`
--

LOCK TABLES `student_leave` WRITE;
/*!40000 ALTER TABLE `student_leave` DISABLE KEYS */;
INSERT INTO `student_leave` VALUES (1,6,'姚龙祥','2025-03-31 11:41:00','2025-03-31 12:41:00','肚子疼',1,'已销假','2025-03-31 11:42:23',''),(2,6,'姚龙祥','2025-03-31 12:04:00','2025-03-31 13:04:00','脑袋疼',1,'已销假','2025-03-31 12:04:58',''),(3,6,'姚龙祥','2025-04-07 06:54:00','2025-04-07 07:54:00','出去玩',1,'已销假','2025-04-07 06:55:10','同意'),(4,3,'张乐乐','2025-05-10 14:51:00','2025-07-10 15:51:00','因作业过多而猝死',1,'已销假','2025-05-10 06:52:54',''),(5,3,'张乐乐','2025-05-10 15:02:00','2027-05-10 16:02:00','写作业猝死',1,'已销假','2025-05-10 07:03:37','同意'),(6,4,'杨济媛','2025-05-10 18:28:00','2025-05-10 19:28:00','困',0,'已销假','2025-05-10 10:29:21',''),(7,6,'姚龙祥','2025-06-02 15:52:00','2025-06-02 16:52:00','1111',1,'已销假','2025-06-02 07:53:19','批准'),(8,6,'姚龙祥','2025-06-04 14:58:00','2025-06-06 18:02:00','有病',1,'已销假','2025-06-04 06:58:33','同意');
/*!40000 ALTER TABLE `student_leave` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:59:02
