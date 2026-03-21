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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('student','teacher','admin') NOT NULL,
  `gender` enum('男','女','其他') NOT NULL,
  `birthdate` date DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `classname` varchar(100) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `avatar` varchar(255) DEFAULT '/static/images/default_avatar.jpg',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'冯榆婷','$2b$12$8WaLyAggK6EZIqIToKbfaON8J9/.UnSny1HCVwbmAX.vLbESHA8OS','admin','女','2004-11-04','护理学院','护理学','23级','7班','None','None','None@123.com','2025-05-11 10:13:12','/static/uploads/avatars/1_mmexport1733495846997_edit_172569053519584.jpg'),(2,'邓双林','$2b$12$WhGkTdFpA5Qw5gC0y1wOIedVUl8r5n1u4IZc5TuRx0AjO5gK2n11u','teacher','男','2005-08-29','计算机学院','人工智能','23级','1班','None','18782722735','18782722735@139.com','2025-05-16 03:16:16','/static/uploads/avatars/2__20231004111659.jpg'),(3,'张乐乐','$2b$12$J9PgRwIjzOTaljB4ZZ1NKe1o8TRzWXptQ6L/.PPZtgul1fcKyVKOC','student','男','2004-07-15','艺术学院','视觉传达','23级','4班',NULL,'15882701123','zll20050715@outlook.com','2025-05-10 06:58:14','/static/uploads/avatars/3_7d1eb041091a3dbc116bb4d11fc81a3371616266015266905.jpg'),(4,'杨济媛','$2b$12$k0.hDgHzAHOb6qC37HFxAuk0WOj9GIp4dw//EZuvSl1MvTiBIoLe6','student','女','2004-10-22','计算机学院','软件工程','24级','1班',NULL,'15882745559','3226009816@qq.com','2025-05-10 10:32:58','/static/uploads/avatars/4_QC2(1).jpg'),(6,'姚龙祥','$2b$12$iMAOMz84ZQt/vrqhgYdojeDFekjf34oUs6NJnHXFKd.7Fs2v5UtjW','student','男','2005-10-10','计算机学院','人工智能','23级','1班',NULL,'12345677894','264432180@qq.com','2025-05-12 09:22:18','/static/uploads/avatars/6_1697678938189_tempCrop.jpg'),(8,'黄一方','$2b$12$4Y07nLong2p5A6k3FPbvhO02Rn5XEtlZuL8MDbWqG.LpjsKS7A/6C','student','男','2005-10-10','计算机学院','人工智能','23级','1班',NULL,'12345677814','26443215180@qq.com','2025-06-02 08:55:36','/static/images/男生.png'),(9,'杨艳雯','$2b$12$80953lNIhFZtMbT6.8ld..Lm1RaqCooKGSWGsxRklSHHmO20guwYO','student','女','2005-10-10','计算机学院','人工智能','23级','1班',NULL,'18782722165','26443215480@qq.com','2025-04-14 08:59:24','/static/images/女生.png');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-17 19:59:01
