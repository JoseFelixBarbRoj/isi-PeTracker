CREATE DATABASE  IF NOT EXISTS `perros_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `perros_app`;
-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: perros_app
-- ------------------------------------------------------
-- Server version	9.2.0

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
-- Table structure for table `mascotas_acogidas`
--

DROP TABLE IF EXISTS `mascotas_acogidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mascotas_acogidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `protectora` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `raza` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitud` decimal(9,6) DEFAULT NULL,
  `longitud` decimal(9,6) DEFAULT NULL,
  `path_imagen` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_imagen_por_protectora` (`protectora`,`path_imagen`),
  CONSTRAINT `fk_perros_protectora` FOREIGN KEY (`protectora`) REFERENCES `protectoras` (`nombre`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mascotas_acogidas`
--

LOCK TABLES `mascotas_acogidas` WRITE;
/*!40000 ALTER TABLE `mascotas_acogidas` DISABLE KEYS */;
INSERT INTO `mascotas_acogidas` VALUES (1,'patas_felices','siamese',40.400000,-3.700000,'static/shelter_uploads/patas_felices/mascota1.png','2026-02-04 08:32:36'),(2,'patas_felices','beagle',40.401000,-3.702000,'static/shelter_uploads/patas_felices/mascota2.png','2026-02-04 08:32:36'),(3,'huellas','beagle',41.380000,2.170000,'static/shelter_uploads/huellas/mascota1.png','2026-02-04 08:32:36'),(4,'huellas','bengal',41.382000,2.175000,'static/shelter_uploads/huellas/mascota2.png','2026-02-04 08:32:36'),(5,'patas_felices','retriever',38.000000,-4.000000,'static/shelter_uploads/patas_felices/mascota3.png','2026-02-04 08:32:36'),(24,'huellas','beagle',38.901000,-3.901000,'static/shelters_uploads/huellas/beagle1.png','2026-03-04 16:53:59'),(25,'huellas','beagle',38.902000,-3.902000,'static/shelters_uploads/huellas/beagle10.png','2026-03-04 16:53:59'),(26,'huellas','bengal',38.903000,-3.903000,'static/shelters_uploads/huellas/bengal1.png','2026-03-04 16:53:59'),(27,'huellas','bengal',38.904000,-3.904000,'static/shelters_uploads/huellas/bengal10.png','2026-03-04 16:53:59'),(28,'huellas','boxer',38.905000,-3.905000,'static/shelters_uploads/huellas/boxer1.png','2026-03-04 16:53:59'),(29,'huellas','boxer',38.906000,-3.906000,'static/shelters_uploads/huellas/boxer10.png','2026-03-04 16:53:59'),(30,'huellas','british_shorthair',38.907000,-3.907000,'static/shelters_uploads/huellas/british_shorthair1.png','2026-03-04 16:53:59'),(31,'huellas','british_shorthair',38.908000,-3.908000,'static/shelters_uploads/huellas/british_shorthair10.png','2026-03-04 16:53:59'),(32,'huellas','bulldog',38.909000,-3.909000,'static/shelters_uploads/huellas/bulldog1.png','2026-03-04 16:53:59'),(33,'huellas','bulldog',38.910000,-3.910000,'static/shelters_uploads/huellas/bulldog10.png','2026-03-04 16:53:59'),(34,'huellas','chihuahua',38.911000,-3.911000,'static/shelters_uploads/huellas/chihuahua1.png','2026-03-04 16:53:59'),(35,'huellas','chihuahua',38.912000,-3.912000,'static/shelters_uploads/huellas/chihuahua10.png','2026-03-04 16:53:59'),(36,'huellas','dachshund',38.913000,-3.913000,'static/shelters_uploads/huellas/dachshund1.png','2026-03-04 16:53:59'),(37,'huellas','dachshund',38.914000,-3.914000,'static/shelters_uploads/huellas/dachshund10.png','2026-03-04 16:53:59'),(38,'huellas','doberman',38.915000,-3.915000,'static/shelters_uploads/huellas/doberman1.png','2026-03-04 16:53:59'),(39,'huellas','doberman',38.916000,-3.916000,'static/shelters_uploads/huellas/doberman10.png','2026-03-04 16:53:59'),(40,'huellas','husky',38.917000,-3.917000,'static/shelters_uploads/huellas/husky1.png','2026-03-04 16:53:59'),(41,'huellas','husky',38.918000,-3.918000,'static/shelters_uploads/huellas/husky10.png','2026-03-04 16:53:59'),(42,'huellas','labrador',38.919000,-3.919000,'static/shelters_uploads/huellas/labrador1.png','2026-03-04 16:53:59'),(43,'huellas','labrador',38.920000,-3.920000,'static/shelters_uploads/huellas/labrador10.png','2026-03-04 16:53:59'),(44,'huellas','maine_coon',38.921000,-3.921000,'static/shelters_uploads/huellas/maine_coon1.png','2026-03-04 16:53:59'),(45,'huellas','maine_coon',38.922000,-3.922000,'static/shelters_uploads/huellas/maine_coon10.png','2026-03-04 16:53:59'),(46,'huellas','persian',38.923000,-3.923000,'static/shelters_uploads/huellas/persian1.png','2026-03-04 16:53:59'),(47,'huellas','persian',38.924000,-3.924000,'static/shelters_uploads/huellas/persian10.png','2026-03-04 16:53:59'),(48,'huellas','pomeranian',38.925000,-3.925000,'static/shelters_uploads/huellas/pomeranian1.png','2026-03-04 16:53:59'),(49,'huellas','pomeranian',38.926000,-3.926000,'static/shelters_uploads/huellas/pomeranian10.png','2026-03-04 16:53:59'),(50,'huellas','poodle',38.927000,-3.927000,'static/shelters_uploads/huellas/poodle1.png','2026-03-04 16:53:59'),(51,'huellas','poodle',38.928000,-3.928000,'static/shelters_uploads/huellas/poodle10.png','2026-03-04 16:53:59'),(52,'huellas','ragdoll',38.929000,-3.929000,'static/shelters_uploads/huellas/ragdoll1.png','2026-03-04 16:53:59'),(53,'huellas','ragdoll',38.930000,-3.930000,'static/shelters_uploads/huellas/ragdoll10.png','2026-03-04 16:53:59'),(54,'huellas','retriever',38.931000,-3.931000,'static/shelters_uploads/huellas/retriever1.png','2026-03-04 16:53:59'),(55,'huellas','retriever',38.932000,-3.932000,'static/shelters_uploads/huellas/retriever10.png','2026-03-04 16:53:59'),(56,'huellas','siamese',38.933000,-3.933000,'static/shelters_uploads/huellas/siamese1.png','2026-03-04 16:53:59'),(57,'huellas','siamese',38.934000,-3.934000,'static/shelters_uploads/huellas/siamese10.png','2026-03-04 16:53:59'),(58,'huellas','spaniel',38.935000,-10.935000,'static/shelters_uploads/huellas/spaniel1.png','2026-03-04 16:53:59'),(59,'huellas','spaniel',38.936000,-3.936000,'static/shelters_uploads/huellas/spaniel10.png','2026-03-04 16:53:59'),(60,'patas_felices','beagle',38.881000,-3.881000,'static/shelters_uploads/patas_felices/beagle100.png','2026-03-04 16:54:23'),(61,'patas_felices','beagle',38.882000,-3.882000,'static/shelters_uploads/patas_felices/beagle101.png','2026-03-04 16:54:23'),(62,'patas_felices','bengal',38.883000,-3.883000,'static/shelters_uploads/patas_felices/bengal100.png','2026-03-04 16:54:23'),(63,'patas_felices','bengal',38.884000,-3.884000,'static/shelters_uploads/patas_felices/bengal101.png','2026-03-04 16:54:23'),(64,'patas_felices','boxer',38.885000,-3.885000,'static/shelters_uploads/patas_felices/boxer100.png','2026-03-04 16:54:23'),(65,'patas_felices','boxer',38.886000,-3.886000,'static/shelters_uploads/patas_felices/boxer101.png','2026-03-04 16:54:23'),(66,'patas_felices','british_shorthair',38.887000,-3.887000,'static/shelters_uploads/patas_felices/british_shorthair100.png','2026-03-04 16:54:23'),(67,'patas_felices','british_shorthair',38.888000,-3.888000,'static/shelters_uploads/patas_felices/british_shorthair101.png','2026-03-04 16:54:23'),(68,'patas_felices','bulldog',38.889000,-3.889000,'static/shelters_uploads/patas_felices/bulldog100.png','2026-03-04 16:54:23'),(69,'patas_felices','bulldog',38.890000,-3.890000,'static/shelters_uploads/patas_felices/bulldog101.png','2026-03-04 16:54:23'),(70,'patas_felices','chihuahua',38.891000,-3.891000,'static/shelters_uploads/patas_felices/chihuahua100.png','2026-03-04 16:54:23'),(71,'patas_felices','chihuahua',38.892000,-3.892000,'static/shelters_uploads/patas_felices/chihuahua101.png','2026-03-04 16:54:23'),(72,'patas_felices','dachshund',38.893000,-3.893000,'static/shelters_uploads/patas_felices/dachshund100.png','2026-03-04 16:54:23'),(73,'patas_felices','dachshund',38.894000,-3.894000,'static/shelters_uploads/patas_felices/dachshund101.png','2026-03-04 16:54:23'),(74,'patas_felices','doberman',38.895000,-3.895000,'static/shelters_uploads/patas_felices/doberman100.png','2026-03-04 16:54:23'),(75,'patas_felices','doberman',38.896000,-3.896000,'static/shelters_uploads/patas_felices/doberman101.png','2026-03-04 16:54:23'),(76,'patas_felices','husky',38.897000,-3.897000,'static/shelters_uploads/patas_felices/husky100.png','2026-03-04 16:54:23'),(77,'patas_felices','husky',38.898000,-3.898000,'static/shelters_uploads/patas_felices/husky101.png','2026-03-04 16:54:23'),(78,'patas_felices','labrador',38.899000,-3.899000,'static/shelters_uploads/patas_felices/labrador100.png','2026-03-04 16:54:23'),(79,'patas_felices','labrador',38.900000,-3.900000,'static/shelters_uploads/patas_felices/labrador101.png','2026-03-04 16:54:23'),(80,'patas_felices','maine_coon',38.901000,-3.901000,'static/shelters_uploads/patas_felices/maine_coon100.png','2026-03-04 16:54:23'),(81,'patas_felices','maine_coon',38.902000,-3.902000,'static/shelters_uploads/patas_felices/maine_coon101.png','2026-03-04 16:54:23'),(82,'patas_felices','persian',38.903000,-3.903000,'static/shelters_uploads/patas_felices/persian100.png','2026-03-04 16:54:23'),(83,'patas_felices','persian',38.904000,-3.904000,'static/shelters_uploads/patas_felices/persian101.png','2026-03-04 16:54:23'),(84,'patas_felices','pomeranian',38.905000,-3.905000,'static/shelters_uploads/patas_felices/pomeranian100.png','2026-03-04 16:54:23'),(85,'patas_felices','pomeranian',38.906000,-3.906000,'static/shelters_uploads/patas_felices/pomeranian101.png','2026-03-04 16:54:23'),(86,'patas_felices','poodle',38.907000,-3.907000,'static/shelters_uploads/patas_felices/poodle100.png','2026-03-04 16:54:23'),(87,'patas_felices','poodle',38.908000,-3.908000,'static/shelters_uploads/patas_felices/poodle101.png','2026-03-04 16:54:23'),(88,'patas_felices','ragdoll',38.909000,-3.909000,'static/shelters_uploads/patas_felices/ragdoll100.png','2026-03-04 16:54:23'),(89,'patas_felices','ragdoll',38.910000,-3.910000,'static/shelters_uploads/patas_felices/ragdoll101.png','2026-03-04 16:54:23'),(90,'patas_felices','retriever',38.911000,-3.911000,'static/shelters_uploads/patas_felices/retriever100.png','2026-03-04 16:54:23'),(91,'patas_felices','retriever',38.912000,-3.912000,'static/shelters_uploads/patas_felices/retriever101.png','2026-03-04 16:54:23'),(92,'patas_felices','siamese',38.913000,-3.913000,'static/shelters_uploads/patas_felices/siamese100.png','2026-03-04 16:54:23'),(93,'patas_felices','siamese',38.914000,-3.914000,'static/shelters_uploads/patas_felices/siamese101.png','2026-03-04 16:54:23'),(94,'patas_felices','spaniel',38.915000,-3.915000,'static/shelters_uploads/patas_felices/spaniel100.png','2026-03-04 16:54:23'),(95,'patas_felices','spaniel',38.916000,-3.916000,'static/shelters_uploads/patas_felices/spaniel101.png','2026-03-04 16:54:23'),(96,'huellas','pomeranian',38.996413,-3.926405,'/static/shelters_uploads/huellas/1_20260314_190203.png','2026-03-14 17:57:34');
/*!40000 ALTER TABLE `mascotas_acogidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mascotas_perdidas`
--

DROP TABLE IF EXISTS `mascotas_perdidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mascotas_perdidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `raza` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `latitud` decimal(9,6) DEFAULT NULL,
  `longitud` decimal(9,6) DEFAULT NULL,
  `path_imagen` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_perros_usuario` (`username`),
  CONSTRAINT `fk_perros_usuario` FOREIGN KEY (`username`) REFERENCES `usuarios` (`nombre`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mascotas_perdidas`
--

LOCK TABLES `mascotas_perdidas` WRITE;
/*!40000 ALTER TABLE `mascotas_perdidas` DISABLE KEYS */;
INSERT INTO `mascotas_perdidas` VALUES (1,'juan','Labrador',40.416775,-3.703790,'static/uploads/juan/labrador1.png ','2026-02-04 08:32:36'),(2,'juan','Pastor Alemán',40.418000,-3.700000,'static/uploads/juan/pastor1.png ','2026-02-04 08:32:36'),(3,'maria','Beagle',41.387397,2.168568,'static/uploads/maria/beagle1.png ','2026-02-04 08:32:36'),(4,'carlos','Mestizo',37.389092,-5.984459,'static/uploads/carlos/mestizo1.png ','2026-02-04 08:32:36'),(47,'carlos','husky',38.993920,-3.928883,'/static/uploads/carlos/bengal100_20260305_185246.png','2026-03-05 16:43:13'),(48,'carlos','husky',38.996415,-3.926412,'/static/uploads/carlos/7_20260314_190506.png','2026-03-14 17:57:34');
/*!40000 ALTER TABLE `mascotas_perdidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `protectoras`
--

DROP TABLE IF EXISTS `protectoras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `protectoras` (
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contraseña_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `protectoras`
--

LOCK TABLES `protectoras` WRITE;
/*!40000 ALTER TABLE `protectoras` DISABLE KEYS */;
INSERT INTO `protectoras` VALUES ('huellas','4321'),('patas_felices','9876'),('Refugio Huellas','dummyhash123');
/*!40000 ALTER TABLE `protectoras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contraseña_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES ('carlos','1234'),('juan','abcd'),('maria','5678');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-15 12:20:17
