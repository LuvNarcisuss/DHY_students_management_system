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
-- Table structure for table `student_courses`
--

DROP TABLE IF EXISTS `student_courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student_courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `student_name` varchar(255) NOT NULL,
  `course_id` int NOT NULL,
  `course_name` varchar(255) NOT NULL,
  `status` enum('已选','未选') DEFAULT '未选',
  `score` int DEFAULT NULL,
  `gpa` decimal(3,1) DEFAULT NULL,
  `usual_score` int DEFAULT NULL,
  `final_score` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`course_id`),
  KEY `student_name` (`student_name`),
  KEY `course_id` (`course_id`),
  KEY `course_name` (`course_name`),
  CONSTRAINT `student_courses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_courses_ibfk_2` FOREIGN KEY (`student_name`) REFERENCES `users` (`username`) ON DELETE CASCADE,
  CONSTRAINT `student_courses_ibfk_3` FOREIGN KEY (`course_id`) REFERENCES `courses` (`id`) ON DELETE CASCADE,
  CONSTRAINT `student_courses_ibfk_4` FOREIGN KEY (`course_name`) REFERENCES `courses` (`course_name`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student_courses`
--

LOCK TABLES `student_courses` WRITE;
/*!40000 ALTER TABLE `student_courses` DISABLE KEYS */;
INSERT INTO `student_courses` VALUES (9,6,'姚龙祥',17,'C语言','已选',75,2.5,90,65),(10,6,'姚龙祥',16,'C++','已选',82,3.2,78,85),(11,6,'姚龙祥',14,'python','已选',86,3.6,80,90),(14,3,'张乐乐',16,'C++','已选',NULL,NULL,NULL,NULL),(15,3,'张乐乐',17,'C语言','已选',NULL,NULL,NULL,NULL),(16,3,'张乐乐',14,'python','已选',82,3.2,100,70),(17,4,'杨济媛',16,'C++','已选',NULL,NULL,NULL,NULL),(18,4,'杨济媛',17,'C语言','已选',NULL,NULL,NULL,NULL),(19,9,'杨艳雯',16,'C++','已选',NULL,NULL,NULL,NULL),(20,9,'杨艳雯',17,'C语言','已选',NULL,NULL,NULL,NULL),(21,9,'杨艳雯',14,'python','已选',94,4.4,100,90),(22,8,'黄一方',14,'python','已选',80,3.0,80,80),(23,8,'黄一方',22,'大学生就业指导','已选',NULL,NULL,NULL,NULL),(24,6,'姚龙祥',22,'大学生就业指导','已选',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `student_courses` ENABLE KEYS */;
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
