
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
CREATE DATABASE IF NOT EXISTS `perros_app` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `perros_app`;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mascotas_acogidas`
--

LOCK TABLES `mascotas_acogidas` WRITE;
/*!40000 ALTER TABLE `mascotas_acogidas` DISABLE KEYS */;
INSERT INTO `mascotas_acogidas` VALUES (1,'patas_felices','siamese',40.400000,-3.700000,'static/shelters_uploads/patas_felices/mascota1.png','2026-02-04 08:32:36'),(2,'patas_felices','beagle',40.401000,-3.702000,'static/shelters_uploads/patas_felices/mascota2.png','2026-02-04 08:32:36'),(3,'huellas','beagle',41.380000,2.170000,'static/shelters_uploads/huellas/mascota1.png','2026-02-04 08:32:36'),(4,'huellas','bengal',41.382000,2.175000,'static/shelters_uploads/huellas/mascota2.png','2026-02-04 08:32:36'),(5,'patas_felices','retriever',38.000000,-4.000000,'static/shelters_uploads/patas_felices/mascota3.png','2026-02-04 08:32:36');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mascotas_perdidas`
--

LOCK TABLES `mascotas_perdidas` WRITE;
/*!40000 ALTER TABLE `mascotas_perdidas` DISABLE KEYS */;
INSERT INTO `mascotas_perdidas` VALUES (1,'juan','labrador',40.416775,-3.703790,'static/uploads/juan/labrador1.png ','2026-02-04 08:32:36'),(2,'juan','siamese',40.418000,-3.700000,'static/uploads/juan/siamese1.png ','2026-02-04 08:32:36'),(3,'maria','beagle',41.387397,2.168568,'static/uploads/maria/beagle1.png ','2026-02-04 08:32:36'),(4,'carlos','poodle',37.389092,-5.984459,'static/uploads/carlos/poodle1.png ','2026-02-04 08:32:36');
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
INSERT INTO `protectoras` VALUES ('huellas','4321'),('patas_felices','9876');
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

-- Dump completed on 2026-02-08 11:37:34
