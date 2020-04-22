-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)

--

-- Host: localhost    Database: AWS

-- ------------------------------------------------------

-- Server version	5.7.29-0ubuntu0.18.04.1



/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;

/*!40101 SET NAMES utf8 */;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;

/*!40103 SET TIME_ZONE='+00:00' */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;



--

-- Table structure for table `COMENTARIO`

--



DROP TABLE IF EXISTS `COMENTARIO`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `COMENTARIO` (

  `usuario` varchar(20) NOT NULL,

  `ruta` varchar(800) NOT NULL,

  `contenido` varchar(1000) NOT NULL,

  KEY `FK_usuario_` (`usuario`),

  KEY `FK_ruta` (`ruta`),

  CONSTRAINT `FK_ruta` FOREIGN KEY (`ruta`) REFERENCES `VIDEO` (`ruta`),

  CONSTRAINT `FK_usuario_` FOREIGN KEY (`usuario`) REFERENCES `USUARIO` (`usuario`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;



--

-- Dumping data for table `COMENTARIO`

--



LOCK TABLES `COMENTARIO` WRITE;

/*!40000 ALTER TABLE `COMENTARIO` DISABLE KEYS */;

/*!40000 ALTER TABLE `COMENTARIO` ENABLE KEYS */;

UNLOCK TABLES;



--

-- Table structure for table `USUARIO`

--



DROP TABLE IF EXISTS `USUARIO`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `USUARIO` (

  `nombre` varchar(20) NOT NULL,

  `apellido` varchar(20) NOT NULL,

  `usuario` varchar(20) NOT NULL,

  `correo` varchar(50) NOT NULL,

  `password` varchar(257) NOT NULL,

  `color` varchar(15) NOT NULL,

  `intento` tinyint(1) DEFAULT '0',

  PRIMARY KEY (`usuario`),

  UNIQUE KEY `usuario` (`usuario`),

  UNIQUE KEY `correo` (`correo`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;



--

-- Dumping data for table `USUARIO`

--



LOCK TABLES `USUARIO` WRITE;

/*!40000 ALTER TABLE `USUARIO` DISABLE KEYS */;

INSERT INTO `USUARIO` VALUES ('Pato','Pato','Pato','Pato','c84f13b8cb9cbcda1ee1b7703db954f57ae07835b8421fd00c46fc407f2ddcef','Red',0),('Pato2','Pato2','Pato2','Pato2','c84f13b8cb9cbcda1ee1b7703db954f57ae07835b8421fd00c46fc407f2ddcef','Red',0);

/*!40000 ALTER TABLE `USUARIO` ENABLE KEYS */;

UNLOCK TABLES;



--

-- Table structure for table `VIDEO`

--



DROP TABLE IF EXISTS `VIDEO`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `VIDEO` (

  `usuarioVideo` varchar(20) NOT NULL,

  `nombreVideo` varchar(250) NOT NULL,

  `etiquetas` varchar(250) DEFAULT NULL,

  `sizeof` varchar(10) NOT NULL,

  `ruta` varchar(800) NOT NULL,

  `fecha` date NOT NULL,

  PRIMARY KEY (`usuarioVideo`,`nombreVideo`),

  UNIQUE KEY `ruta` (`ruta`),

  UNIQUE KEY `ruta_2` (`ruta`),

  CONSTRAINT `FK_usuario` FOREIGN KEY (`usuarioVideo`) REFERENCES `USUARIO` (`usuario`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;



--

-- Dumping data for table `VIDEO`

--



LOCK TABLES `VIDEO` WRITE;

/*!40000 ALTER TABLE `VIDEO` DISABLE KEYS */;

INSERT INTO `VIDEO` VALUES ('Pato','Video de Pato','#Tusmuertos','34234','rutaesa','2019-09-12'),('Pato','Video de Pato2','#Tusmuertos','34234','rutaesa2','2019-09-12'),('Pato','Video del Pato','#Tusmuertos','34234','rutaesa3','2019-09-12');

/*!40000 ALTER TABLE `VIDEO` ENABLE KEYS */;

UNLOCK TABLES;



--

-- Table structure for table `VOTO`

--



DROP TABLE IF EXISTS `VOTO`;

/*!40101 SET @saved_cs_client     = @@character_set_client */;

/*!40101 SET character_set_client = utf8 */;

CREATE TABLE `VOTO` (

  `usuario` varchar(20) NOT NULL,

  `ruta` varchar(800) NOT NULL,

  `decision` tinyint(1) DEFAULT NULL,

  PRIMARY KEY (`usuario`,`ruta`),

  KEY `FK_ruta2` (`ruta`),

  CONSTRAINT `FK_ruta2` FOREIGN KEY (`ruta`) REFERENCES `VIDEO` (`ruta`),

  CONSTRAINT `FK_usuario2` FOREIGN KEY (`usuario`) REFERENCES `USUARIO` (`usuario`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET character_set_client = @saved_cs_client */;



--

-- Dumping data for table `VOTO`

--



LOCK TABLES `VOTO` WRITE;

/*!40000 ALTER TABLE `VOTO` DISABLE KEYS */;

INSERT INTO `VOTO` VALUES ('Pato2','rutaesa',1),('Pato2','rutaesa2',0);

/*!40000 ALTER TABLE `VOTO` ENABLE KEYS */;

UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;



/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;



-- Dump completed on 2020-04-21 17:06:05
