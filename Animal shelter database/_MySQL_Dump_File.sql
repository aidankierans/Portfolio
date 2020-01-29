CREATE DATABASE  IF NOT EXISTS `shelter` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `shelter`;
-- MySQL dump 10.13  Distrib 5.7.27, for Win64 (x86_64)
--
-- Host: localhost    Database: shelter
-- ------------------------------------------------------
-- Server version	5.7.27-log

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
-- Table structure for table `adopted`
--

DROP TABLE IF EXISTS `adopted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adopted` (
  `human_id` bigint(20) unsigned NOT NULL,
  `id_number` mediumint(8) unsigned NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date DEFAULT NULL,
  KEY `human_id` (`human_id`,`id_number`),
  KEY `FK_AnimalAdopted` (`id_number`),
  CONSTRAINT `FK_AnimalAdopted` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON UPDATE CASCADE,
  CONSTRAINT `FK_CustomerAdopted` FOREIGN KEY (`human_id`) REFERENCES `customer` (`human_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adopted`
--

LOCK TABLES `adopted` WRITE;
/*!40000 ALTER TABLE `adopted` DISABLE KEYS */;
INSERT INTO `adopted` VALUES (4,2,'2019-08-08',NULL);
/*!40000 ALTER TABLE `adopted` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animal`
--

DROP TABLE IF EXISTS `animal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animal` (
  `id_number` mediumint(8) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `birth_date` date NOT NULL,
  `date_sheltered` date NOT NULL,
  `gender` enum('Male','Female','n/a') DEFAULT NULL,
  `sexed` tinyint(1) unsigned NOT NULL,
  `microchip_id` decimal(10,0) unsigned DEFAULT NULL,
  `diet` varchar(256) DEFAULT NULL,
  `weight` decimal(4,1) unsigned NOT NULL,
  `special_needs` varchar(256) DEFAULT NULL,
  `is_deceased` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `origin` varchar(256) DEFAULT NULL,
  `behavior_notes` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id_number`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal`
--

LOCK TABLES `animal` WRITE;
/*!40000 ALTER TABLE `animal` DISABLE KEYS */;
INSERT INTO `animal` VALUES (1,'Lucy','2015-02-03','2017-02-04','Female',0,NULL,NULL,100.0,NULL,0,'alley way',NULL),(2,'Martin','2018-12-12','2019-01-15','Male',0,NULL,NULL,5.4,NULL,0,'playground','gets hyper easily'),(3,'Sassy','2018-03-06','2018-05-18','Female',0,NULL,'tuna for lunch, milk for both breakfast and dinner',20.3,NULL,0,NULL,'very picky with her food'),(4,'Thomas O Maley','2015-07-17','2017-04-17','Male',0,NULL,NULL,50.2,NULL,0,'alley cat',NULL),(5,'Bolt','2015-04-24','2016-05-15','Male',0,NULL,NULL,100.5,NULL,0,'RACC',NULL);
/*!40000 ALTER TABLE `animal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bit`
--

DROP TABLE IF EXISTS `bit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bit` (
  `human_id` bigint(20) unsigned NOT NULL,
  `id_number` mediumint(8) unsigned NOT NULL,
  `n_times` tinyint(4) NOT NULL,
  KEY `human_id` (`human_id`),
  KEY `id_number` (`id_number`),
  CONSTRAINT `FK_AnimalBit` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_PersonBit` FOREIGN KEY (`human_id`) REFERENCES `person` (`human_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bit`
--

LOCK TABLES `bit` WRITE;
/*!40000 ALTER TABLE `bit` DISABLE KEYS */;
INSERT INTO `bit` VALUES (4,2,4);
/*!40000 ALTER TABLE `bit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cat`
--

DROP TABLE IF EXISTS `cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat` (
  `id_number` mediumint(8) unsigned NOT NULL,
  `breed` enum('unknown','persian','maine coon','exotic','siamese','abyssinian','ragdoll','birman','american shorthair','oriental','sphinx') NOT NULL,
  PRIMARY KEY (`id_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cat`
--

LOCK TABLES `cat` WRITE;
/*!40000 ALTER TABLE `cat` DISABLE KEYS */;
INSERT INTO `cat` VALUES (3,'persian'),(4,'birman');
/*!40000 ALTER TABLE `cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cat_immunizations`
--

DROP TABLE IF EXISTS `cat_immunizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cat_immunizations` (
  `id_number` mediumint(8) unsigned NOT NULL,
  `i_date` date NOT NULL,
  `type` enum('rabies','feline distemper','feline herpesvirus','calicivirus','feline leukemia virus','bordetella') NOT NULL,
  KEY `id_number` (`id_number`,`i_date`,`type`),
  CONSTRAINT `FK_CatCat_Immunizations` FOREIGN KEY (`id_number`) REFERENCES `cat` (`id_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cat_immunizations`
--

LOCK TABLES `cat_immunizations` WRITE;
/*!40000 ALTER TABLE `cat_immunizations` DISABLE KEYS */;
INSERT INTO `cat_immunizations` VALUES (3,'2019-11-11','rabies'),(4,'2019-03-30','feline distemper');
/*!40000 ALTER TABLE `cat_immunizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `human_id` bigint(20) unsigned NOT NULL,
  `allowed_to_adopt` tinyint(1) unsigned NOT NULL DEFAULT 1,
  `has_young_children` tinyint(1) unsigned NOT NULL DEFAULT 0,
  `sex` enum('please ask','male','female') NOT NULL DEFAULT 'please ask',
  PRIMARY KEY (`human_id`),
  CONSTRAINT `FK_PersonCustomer` FOREIGN KEY (`human_id`) REFERENCES `person` (`human_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES 
(4, 1, 0,'female'), 
(1, 1, 1, 'female'),
(2, 1, 1, 'male'), 
(3, 1, 0, 'male'); 

/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dog`
--

DROP TABLE IF EXISTS `dog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dog` (
  `id_number` mediumint(8) unsigned NOT NULL,
  `breed` enum('unknown','labrador retriever','yorkshire terrier','german shepherd','beagle','boxer','dachsund','english bulldog','poodle','shih tzu','golden retriever','bernese mountain dog') NOT NULL,
  PRIMARY KEY (`id_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dog`
--

LOCK TABLES `dog` WRITE;
/*!40000 ALTER TABLE `dog` DISABLE KEYS */;
INSERT INTO `dog` VALUES (1,'beagle'),(2,'german shepherd');
/*!40000 ALTER TABLE `dog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dog_immunizations`
--

DROP TABLE IF EXISTS `dog_immunizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dog_immunizations` (
  `id_number` mediumint(8) unsigned NOT NULL,
  `i_date` date NOT NULL,
  `type` enum('rabies 1-year','rabies 3-year','distemper','parvovirus','cav-1','cav-2','parainfluenza','bordetella bronchiseptica','lyme disease','leptospirosis','canine influenza') NOT NULL,
  KEY `id_number` (`id_number`,`i_date`,`type`),
  CONSTRAINT `FK_DogDog_Immunizations` FOREIGN KEY (`id_number`) REFERENCES `dog` (`id_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dog_immunizations`
--

LOCK TABLES `dog_immunizations` WRITE;
/*!40000 ALTER TABLE `dog_immunizations` DISABLE KEYS */;
INSERT INTO `dog_immunizations` VALUES (1,'2019-07-15','rabies 1-year'),(2,'2019-06-26','rabies 3-year');
/*!40000 ALTER TABLE `dog_immunizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employee` (
  `human_id` bigint(20) unsigned NOT NULL,
  `ssn` decimal(9,0) unsigned NOT NULL,
  `job_title` enum('medical','kennel','adoption','admission','volunteer','trainer','hr manager') NOT NULL,
  `salary` int(10) unsigned NOT NULL,
  PRIMARY KEY (`human_id`),
  CONSTRAINT `FK_PersonEmployee` FOREIGN KEY (`human_id`) REFERENCES `person` (`human_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,333333333,'medical',25),(2,444444444,'adoption',15),(3,666666666,'admission',15),(5,222222222,'kennel',7),(6,111111111,'volunteer',0),(7,555555555,'trainer',20),(8,777777777,'hr manager',17);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee_info_changes`
--

DROP TABLE IF EXISTS `employee_info_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employee_info_changes` (
  `human_id` bigint(20) unsigned NOT NULL,
  `changed_by` varchar(93) NOT NULL,
  `time_occurred` datetime NOT NULL,
  `old_job_title` enum('medical','kennel','adoption','admission','volunteer','trainer') NOT NULL,
  `new_job_title` enum('medical','kennel','adoption','admission','volunteer','trainer') NOT NULL,
  `old_salary` int(10) unsigned NOT NULL,
  `new_salary` int(10) unsigned NOT NULL,
  KEY `changed_by` (`changed_by`,`time_occurred`),
  KEY `FK_EmployeeLog` (`human_id`),
  CONSTRAINT `FK_EmployeeLog` FOREIGN KEY (`human_id`) REFERENCES `employee` (`human_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee_info_changes`
--

LOCK TABLES `employee_info_changes` WRITE;
/*!40000 ALTER TABLE `employee_info_changes` DISABLE KEYS */;
/*!40000 ALTER TABLE `employee_info_changes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `incompatible`
--

DROP TABLE IF EXISTS `incompatible`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `incompatible` (
  `id_number` mediumint(8) unsigned NOT NULL,
  `should_avoid` enum('men','small_children','cats','dogs','rodents','birds','reptiles') DEFAULT NULL,
  KEY `id_number` (`id_number`,`should_avoid`),
  CONSTRAINT `FK_AnimalIncompatible` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `incompatible`
--

LOCK TABLES `incompatible` WRITE;
/*!40000 ALTER TABLE `incompatible` DISABLE KEYS */;
INSERT INTO `incompatible` VALUES (2,'small_children'),(3,'dogs'),(4,'small_children');
/*!40000 ALTER TABLE `incompatible` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical`
--

DROP TABLE IF EXISTS `medical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `medical` (
  `human_id` bigint(20) unsigned NOT NULL,
  `certification` enum('certificate','degree','license') NOT NULL,
  PRIMARY KEY (`human_id`),
  CONSTRAINT `FK_EmployeeMedical` FOREIGN KEY (`human_id`) REFERENCES `employee` (`human_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical`
--

LOCK TABLES `medical` WRITE;
/*!40000 ALTER TABLE `medical` DISABLE KEYS */;
INSERT INTO `medical` VALUES (1,'degree');
/*!40000 ALTER TABLE `medical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `human_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `birth_date` date NOT NULL,
  `phone_number` decimal(10,0) unsigned DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `street_number` mediumint(8) unsigned NOT NULL,
  `street_name` varchar(16) NOT NULL,
  `apt_number` mediumint(8) unsigned DEFAULT NULL,
  `city` varchar(24) NOT NULL,
  `state` enum('AA','AE','AK','AL','AP','AZ','AR','CA','CO','CT','DC','DL','FL','FM','GA','GU','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MH','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','PR','PW','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY') NOT NULL,
  `zip` decimal(5,0) unsigned NOT NULL,
  PRIMARY KEY (`human_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES 
(1,'laura','smith','1977-03-03',NULL,NULL,12345,'Main ST',NULL,'Richmond','VA',23323),
(2,'john','wilde','1990-04-23',NULL,NULL,54321,'Cary St',NULL,'Richmond','VA',23323),
(3,'ryan','williams','1998-07-15',NULL,NULL,23456,'Bread St',NULL,'Richmond','VA',23323),
(4,'janet','carter','1989-11-29',NULL,NULL,608,'Franklin St',NULL,'Richmond','VA',23323),
(5,'moby','dick','1965-06-16',NULL,NULL,555,'Belvidere St',NULL,'Richmond','VA',23321),
(6,'alexander','dumas','1988-08-13',NULL,NULL,3,'N Muskateer St',NULL,'Richmond','VA',23323),
(7,'conan','doyle','1992-09-18',NULL,NULL,15,'Sherlock Ave',NULL,'Richmond','VA',23323),
(8,'stephen','king','1973-03-29',NULL,NULL,28,'Cary St',NULL,'Richmond','VA',23322);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pet_types_owned`
--

DROP TABLE IF EXISTS `pet_types_owned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pet_types_owned` (
  `human_id` bigint(20) unsigned NOT NULL,
  `pet_type` enum('dog','cat','rodent','bird','reptile','other') NOT NULL,
  KEY `human_id` (`human_id`,`pet_type`),
  CONSTRAINT `FK_CustomerPetTO` FOREIGN KEY (`human_id`) REFERENCES `customer` (`human_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pet_types_owned`
--

LOCK TABLES `pet_types_owned` WRITE;
/*!40000 ALTER TABLE `pet_types_owned` DISABLE KEYS */;
INSERT INTO `pet_types_owned` VALUES (4,'dog');
/*!40000 ALTER TABLE `pet_types_owned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescribed`
--

DROP TABLE IF EXISTS `prescribed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prescribed` (
  `human_id` bigint(20) unsigned NOT NULL,
  `id_number` mediumint(8) unsigned NOT NULL,
  `prescription` varchar(256) NOT NULL,
  `date_written` date NOT NULL,
  KEY `human_id` (`human_id`,`id_number`),
  KEY `FK_AnimalPrescribed` (`id_number`),
  CONSTRAINT `FK_AnimalPrescribed` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON UPDATE CASCADE,
  CONSTRAINT `FK_MedicalPrescribed` FOREIGN KEY (`human_id`) REFERENCES `medical` (`human_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescribed`
--

LOCK TABLES `prescribed` WRITE;
/*!40000 ALTER TABLE `prescribed` DISABLE KEYS */;
INSERT INTO `prescribed` VALUES (4,2,'pills','2019-03-18');
/*!40000 ALTER TABLE `prescribed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserved`
--

DROP TABLE IF EXISTS `reserved`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reserved` (
  `human_id` bigint(20) unsigned NOT NULL,
  `id_number` mediumint(8) unsigned NOT NULL,
  `r_date` date NOT NULL,
  KEY `human_id` (`human_id`,`id_number`),
  KEY `FK_AnimalReserved` (`id_number`),
  CONSTRAINT `FK_AnimalReserved` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON UPDATE CASCADE,
  CONSTRAINT `FK_CustomerReserved` FOREIGN KEY (`human_id`) REFERENCES `customer` (`human_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserved`
--

LOCK TABLES `reserved` WRITE;
/*!40000 ALTER TABLE `reserved` DISABLE KEYS */;
INSERT INTO `reserved` VALUES (4,1,'2019-01-31'),(4,2,'0000-00-00'),(4,4,'2019-01-28');
/*!40000 ALTER TABLE `reserved` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treated`
--

DROP TABLE IF EXISTS `treated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `treated` (
  `human_id` bigint(20) unsigned NOT NULL,
  `id_number` mediumint(8) unsigned NOT NULL,
  `t_date` date NOT NULL,
  `symptoms` varchar(256) NOT NULL,
  `procedures` varchar(256) NOT NULL,
  KEY `human_id` (`human_id`,`id_number`),
  KEY `FK_AnimalTreated` (`id_number`),
  CONSTRAINT `FK_AnimalTreated` FOREIGN KEY (`id_number`) REFERENCES `animal` (`id_number`) ON UPDATE CASCADE,
  CONSTRAINT `FK_MedicalTreated` FOREIGN KEY (`human_id`) REFERENCES `medical` (`human_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treated`
--

LOCK TABLES `treated` WRITE;
/*!40000 ALTER TABLE `treated` DISABLE KEYS */;
INSERT INTO `treated` VALUES (1,1,'2019-05-15','broken leg','stitches and a cast');
/*!40000 ALTER TABLE `treated` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed