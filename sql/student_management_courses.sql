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
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `course_name` varchar(255) NOT NULL,
  `credit` float NOT NULL,
  `department` varchar(255) NOT NULL,
  `teacher_name` varchar(100) DEFAULT NULL,
  `textbook` varchar(255) DEFAULT NULL,
  `course_type` enum('必修','选修') NOT NULL DEFAULT '必修',
  `capacity` int NOT NULL DEFAULT '50',
  `status` enum('待审批','已通过','已驳回') DEFAULT '待审批',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin_comment` text,
  `teacher_id` int DEFAULT NULL,
  `remaining_capacity` int DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `coursename` (`course_name`),
  KEY `fk_teacher_id` (`teacher_id`),
  KEY `fk_teacher_name` (`teacher_name`),
  CONSTRAINT `fk_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_teacher_name` FOREIGN KEY (`teacher_name`) REFERENCES `users` (`username`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (14,'python',5,'计算机学院','邓双林','python程序设计','必修',100,'已通过','2025-04-01 10:06:34',NULL,2,95),(16,'C++',4,'计算机学院','邓双林','C++程序设计','必修',100,'已通过','2025-04-01 10:06:34',NULL,2,96),(17,'C语言',3.5,'计算机学院','邓双林','C语言程序设计','必修',80,'已通过','2025-04-01 10:06:34',NULL,2,75),(21,'你好',1,'艺术学院','邓双林','你好','必修',50,'已驳回','2025-04-01 10:38:15',NULL,2,50),(22,'大学生就业指导',1,'学生工作处','邓双林','大学生就业指导','选修',50,'已通过','2025-06-02 07:50:36','',2,48);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:59:03
