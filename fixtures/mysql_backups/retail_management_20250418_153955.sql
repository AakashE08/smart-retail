-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: retail_management
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `accounts_user`
--

DROP TABLE IF EXISTS `accounts_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user`
--

LOCK TABLES `accounts_user` WRITE;
/*!40000 ALTER TABLE `accounts_user` DISABLE KEYS */;
INSERT INTO `accounts_user` VALUES (1,'pbkdf2_sha256$600000$LGrcWDIoZESW88yrckjYKI$I4qprtvW2+iTsAehYkSxnLfvYgrUFnlffcIgeWVPc6I=','2025-04-17 17:13:47.000000',1,'Aakash8','','','eaakash8805@gmail.com',1,1,'2025-04-08 20:06:20.000000','ADMIN'),(2,'pbkdf2_sha256$600000$6K85UppPJCeyvA0VgCijV3$hNOj+L9sdOty8pSHbgwMtOEOFHy/dyODc1l30ZLcTJs=','2025-04-17 12:19:22.773759',0,'Aakash','Aakash','E','eaakash8805@gmail.com',0,1,'2025-04-17 10:47:30.893133','CUSTOMER'),(3,'pbkdf2_sha256$600000$5FxyR9OPxAWaE7oZ7G7L3S$eRFFZEO+niQWd9a1xZT/PhJOGXaYNMrUbYuVnft7j4s=','2025-04-17 12:18:57.293938',0,'yashwanth','yashwanth','kumar','eaakash8805@gmail.com',0,1,'2025-04-17 12:16:46.578131','CUSTOMER'),(5,'pbkdf2_sha256$600000$E2G4OdRVXtgBFMfQAjVOA3$nHVwOoUOdjYQFQ/i/60Ry3vRbktOtg86sIL7VKDH+bc=',NULL,1,'ADMIN01','','','08august2005@gmail.com',1,1,'2025-04-17 17:17:37.000000','ADMIN'),(6,'pbkdf2_sha256$600000$Akdwu0St3LWdEKSuFuDtI4$jQbfYI999kfbCVUw1cyCCstSDmh+Yj2z1FkXMKVeS00=',NULL,0,'employee001','','','ae0935@srmist.edu.in',0,1,'2025-04-17 17:20:21.000000','EMPLOYEE');
/*!40000 ALTER TABLE `accounts_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_groups`
--

DROP TABLE IF EXISTS `accounts_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_groups_user_id_group_id_59c0b32f_uniq` (`user_id`,`group_id`),
  KEY `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_groups`
--

LOCK TABLES `accounts_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` (`user_id`,`permission_id`),
  KEY `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_user_user_permissions`
--

LOCK TABLES `accounts_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_userprofile`
--

DROP TABLE IF EXISTS `accounts_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `avatar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_userprofile_user_id_92240672_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_userprofile`
--

LOCK TABLES `accounts_userprofile` WRITE;
/*!40000 ALTER TABLE `accounts_userprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add category',7,'add_category'),(26,'Can change category',7,'change_category'),(27,'Can delete category',7,'delete_category'),(28,'Can view category',7,'view_category'),(29,'Can add product',8,'add_product'),(30,'Can change product',8,'change_product'),(31,'Can delete product',8,'delete_product'),(32,'Can view product',8,'view_product'),(33,'Can add inventory log',9,'add_inventorylog'),(34,'Can change inventory log',9,'change_inventorylog'),(35,'Can delete inventory log',9,'delete_inventorylog'),(36,'Can view inventory log',9,'view_inventorylog'),(37,'Can add order',10,'add_order'),(38,'Can change order',10,'change_order'),(39,'Can delete order',10,'delete_order'),(40,'Can view order',10,'view_order'),(41,'Can add order item',11,'add_orderitem'),(42,'Can change order item',11,'change_orderitem'),(43,'Can delete order item',11,'delete_orderitem'),(44,'Can view order item',11,'view_orderitem'),(45,'Can add order tracking',12,'add_ordertracking'),(46,'Can change order tracking',12,'change_ordertracking'),(47,'Can delete order tracking',12,'delete_ordertracking'),(48,'Can view order tracking',12,'view_ordertracking'),(49,'Can add bill',13,'add_bill'),(50,'Can change bill',13,'change_bill'),(51,'Can delete bill',13,'delete_bill'),(52,'Can view bill',13,'view_bill'),(53,'Can add bill item',14,'add_billitem'),(54,'Can change bill item',14,'change_billitem'),(55,'Can delete bill item',14,'delete_billitem'),(56,'Can view bill item',14,'view_billitem'),(57,'Can add return',15,'add_return'),(58,'Can change return',15,'change_return'),(59,'Can delete return',15,'delete_return'),(60,'Can view return',15,'view_return'),(61,'Can add return item',16,'add_returnitem'),(62,'Can change return item',16,'change_returnitem'),(63,'Can delete return item',16,'delete_returnitem'),(64,'Can view return item',16,'view_returnitem'),(65,'Can add return status history',17,'add_returnstatushistory'),(66,'Can change return status history',17,'change_returnstatushistory'),(67,'Can delete return status history',17,'delete_returnstatushistory'),(68,'Can view return status history',17,'view_returnstatushistory'),(69,'Can add customer profile',18,'add_customerprofile'),(70,'Can change customer profile',18,'change_customerprofile'),(71,'Can delete customer profile',18,'delete_customerprofile'),(72,'Can view customer profile',18,'view_customerprofile'),(73,'Can add cart item',19,'add_cartitem'),(74,'Can change cart item',19,'change_cartitem'),(75,'Can delete cart item',19,'delete_cartitem'),(76,'Can view cart item',19,'view_cartitem'),(77,'Can add promotion',20,'add_promotion'),(78,'Can change promotion',20,'change_promotion'),(79,'Can delete promotion',20,'delete_promotion'),(80,'Can view promotion',20,'view_promotion'),(81,'Can add used promotion',21,'add_usedpromotion'),(82,'Can change used promotion',21,'change_usedpromotion'),(83,'Can delete used promotion',21,'delete_usedpromotion'),(84,'Can view used promotion',21,'view_usedpromotion'),(85,'Can add promotion category',22,'add_promotioncategory'),(86,'Can change promotion category',22,'change_promotioncategory'),(87,'Can delete promotion category',22,'delete_promotioncategory'),(88,'Can view promotion category',22,'view_promotioncategory'),(89,'Can add promotion product',23,'add_promotionproduct'),(90,'Can change promotion product',23,'change_promotionproduct'),(91,'Can delete promotion product',23,'delete_promotionproduct'),(92,'Can view promotion product',23,'view_promotionproduct'),(93,'Can add saved report',24,'add_savedreport'),(94,'Can change saved report',24,'change_savedreport'),(95,'Can delete saved report',24,'delete_savedreport'),(96,'Can view saved report',24,'view_savedreport'),(97,'Can add User Profile',25,'add_userprofile'),(98,'Can change User Profile',25,'change_userprofile'),(99,'Can delete User Profile',25,'delete_userprofile'),(100,'Can view User Profile',25,'view_userprofile'),(101,'Can add stock',26,'add_stock'),(102,'Can change stock',26,'change_stock'),(103,'Can delete stock',26,'delete_stock'),(104,'Can view stock',26,'view_stock');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_bill`
--

DROP TABLE IF EXISTS `billing_bill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_bill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `bill_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `bill_date` datetime(6) NOT NULL,
  `sub_total` decimal(10,2) NOT NULL,
  `discount_amount` decimal(10,2) NOT NULL,
  `tax` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_by_id` bigint NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `bill_number` (`bill_number`),
  KEY `billing_bil_bill_nu_75226f_idx` (`bill_number`),
  KEY `billing_bil_custome_07844a_idx` (`customer_id`),
  KEY `billing_bil_bill_da_c33464_idx` (`bill_date`),
  KEY `billing_bil_payment_bc01cd_idx` (`payment_status`),
  KEY `billing_bill_created_by_id_6dcc4ab1_fk_accounts_user_id` (`created_by_id`),
  CONSTRAINT `billing_bill_created_by_id_6dcc4ab1_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `billing_bill_customer_id_a8a94fda_fk_accounts_user_id` FOREIGN KEY (`customer_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_bill`
--

LOCK TABLES `billing_bill` WRITE;
/*!40000 ALTER TABLE `billing_bill` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_bill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing_billitem`
--

DROP TABLE IF EXISTS `billing_billitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing_billitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `bill_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `billing_billitem_bill_id_6cd8c774_fk_billing_bill_id` (`bill_id`),
  KEY `billing_billitem_product_id_c46fc1ea_fk_inventory_product_id` (`product_id`),
  CONSTRAINT `billing_billitem_bill_id_6cd8c774_fk_billing_bill_id` FOREIGN KEY (`bill_id`) REFERENCES `billing_bill` (`id`),
  CONSTRAINT `billing_billitem_product_id_c46fc1ea_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `billing_billitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing_billitem`
--

LOCK TABLES `billing_billitem` WRITE;
/*!40000 ALTER TABLE `billing_billitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `billing_billitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers_cartitem`
--

DROP TABLE IF EXISTS `customers_cartitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_cartitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `added_on` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `customers_cartitem_customer_id_product_id_335527b6_uniq` (`customer_id`,`product_id`),
  KEY `customers_cartitem_product_id_a7fdb093_fk_inventory_product_id` (`product_id`),
  CONSTRAINT `customers_cartitem_customer_id_0475fbcc_fk_accounts_user_id` FOREIGN KEY (`customer_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `customers_cartitem_product_id_a7fdb093_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `customers_cartitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_cartitem`
--

LOCK TABLES `customers_cartitem` WRITE;
/*!40000 ALTER TABLE `customers_cartitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers_cartitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers_customerprofile`
--

DROP TABLE IF EXISTS `customers_customerprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers_customerprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `joined_date` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `customers_customerprofile_user_id_34a05092_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers_customerprofile`
--

LOCK TABLES `customers_customerprofile` WRITE;
/*!40000 ALTER TABLE `customers_customerprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `customers_customerprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-04-17 17:20:22.271976','6','employee001',1,'[{\"added\": {}}]',6,1),(2,'2025-04-17 17:20:56.974967','6','employee001',2,'[]',6,1),(3,'2025-04-17 17:21:48.795574','4','employee1',3,'',6,1),(4,'2025-04-17 17:22:58.413610','5','ADMIN01',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,1),(5,'2025-04-17 17:23:16.820818','1','Aakash8',2,'[{\"changed\": {\"fields\": [\"Role\"]}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts','user'),(25,'accounts','userprofile'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(13,'billing','bill'),(14,'billing','billitem'),(4,'contenttypes','contenttype'),(19,'customers','cartitem'),(18,'customers','customerprofile'),(7,'inventory','category'),(9,'inventory','inventorylog'),(8,'inventory','product'),(26,'inventory','stock'),(10,'orders','order'),(11,'orders','orderitem'),(12,'orders','ordertracking'),(20,'promotions','promotion'),(22,'promotions','promotioncategory'),(23,'promotions','promotionproduct'),(21,'promotions','usedpromotion'),(24,'reports','savedreport'),(15,'returns','return'),(16,'returns','returnitem'),(17,'returns','returnstatushistory'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-08 20:05:16.441745'),(2,'contenttypes','0002_remove_content_type_name','2025-04-08 20:05:16.570084'),(3,'auth','0001_initial','2025-04-08 20:05:16.979152'),(4,'auth','0002_alter_permission_name_max_length','2025-04-08 20:05:17.084901'),(5,'auth','0003_alter_user_email_max_length','2025-04-08 20:05:17.091361'),(6,'auth','0004_alter_user_username_opts','2025-04-08 20:05:17.110969'),(7,'auth','0005_alter_user_last_login_null','2025-04-08 20:05:17.124370'),(8,'auth','0006_require_contenttypes_0002','2025-04-08 20:05:17.125356'),(9,'auth','0007_alter_validators_add_error_messages','2025-04-08 20:05:17.138572'),(10,'auth','0008_alter_user_username_max_length','2025-04-08 20:05:17.149404'),(11,'auth','0009_alter_user_last_name_max_length','2025-04-08 20:05:17.159640'),(12,'auth','0010_alter_group_name_max_length','2025-04-08 20:05:17.193090'),(13,'auth','0011_update_proxy_permissions','2025-04-08 20:05:17.205850'),(14,'auth','0012_alter_user_first_name_max_length','2025-04-08 20:05:17.214574'),(15,'accounts','0001_initial','2025-04-08 20:05:17.801910'),(16,'admin','0001_initial','2025-04-08 20:05:18.030983'),(17,'admin','0002_logentry_remove_auto_add','2025-04-08 20:05:18.043444'),(18,'admin','0003_logentry_add_action_flag_choices','2025-04-08 20:05:18.049115'),(19,'inventory','0001_initial','2025-04-08 20:05:18.692925'),(20,'billing','0001_initial','2025-04-08 20:05:19.314348'),(21,'customers','0001_initial','2025-04-08 20:05:19.685782'),(22,'orders','0001_initial','2025-04-08 20:05:20.551781'),(23,'promotions','0001_initial','2025-04-08 20:05:21.221499'),(24,'reports','0001_initial','2025-04-08 20:05:21.339773'),(25,'returns','0001_initial','2025-04-08 20:05:22.364472'),(26,'sessions','0001_initial','2025-04-08 20:05:22.424467'),(27,'accounts','0002_remove_user_address_remove_user_phone_userprofile','2025-04-17 12:10:20.144433'),(28,'inventory','0002_alter_inventorylog_options_and_more','2025-04-17 17:38:16.244368');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('3vgu5mzvxkv2dllr4rbqy0nt4q69zetd','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFD:DC6zpMh4t_u_c4aZMa9b0y0KRsPyLmuj5THQ4d7m8ls','2025-04-08 21:08:27.495010'),('4eykieqdejplzf9jaslkmpqki9z7ta56','.eJxVjDsOwjAQBe_iGlmbOHhtSvqcwdqPjQMokfKpEHeHSCmgfTPzXibRtta0LXlOg5qLaczpd2OSRx53oHcab5OVaVznge2u2IMutp80P6-H-3dQaanfGrXzQtFBQVDvYqTSkCCgb0txwYdAwlA4ez5zKxEb7MB1yqIAbUHz_gDmsjgD:1u5P6D:rYNKnrPWvLdXZ8mhpZGyj52cK6gHcMVjioOaBL5McJM','2025-04-17 14:16:13.151249'),('4f6u55jmjefskcyvdqehubnuvjvtweye','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFo:OTMjLuZk64BRH4heyBzDROzTHKpkE9LYwW85Wihv37Q','2025-04-08 21:09:04.060268'),('f2gctu8skp4y5339ggm8d3ip66mbnohj','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFD:DC6zpMh4t_u_c4aZMa9b0y0KRsPyLmuj5THQ4d7m8ls','2025-04-08 21:08:27.348528'),('fq6jzcvlly9yr3a3kkjd8hdyrfoymno2','.eJxVjDsOwjAQBe_iGlmbOHhtSvqcwdqPjQMokfKpEHeHSCmgfTPzXibRtta0LXlOg5qLaczpd2OSRx53oHcab5OVaVznge2u2IMutp80P6-H-3dQaanfGrXzQtFBQVDvYqTSkCCgb0txwYdAwlA4ez5zKxEb7MB1yqIAbUHz_gDmsjgD:1u5TWU:PkY1v7Yr17HHD13i9Ko-Eq9QbAlMdwDM1V5VsT3Dv58','2025-04-17 18:59:38.478041'),('lo1wumnsc782z1lzt48u4my0c2m2u0f0','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFC:Ebp9J_Rnafv93OEhG42g5mDto1tq4QmGq7Aw-e2nrbU','2025-04-08 21:08:26.832567'),('mgp41q5ea8gxm2s7fbojstqk718lpjm4','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFD:DC6zpMh4t_u_c4aZMa9b0y0KRsPyLmuj5THQ4d7m8ls','2025-04-08 21:08:27.293436'),('zmgm5f3do65dzyi3q4n3upzwbpp9oswt','.eJxVjDsOwjAQBe_iGlkm_uyGkj5niNbeDQ4gW4qTCnF3iJQC2jcz76VG2tY8bk2WcWZ1UWd1-t0ipYeUHfCdyq3qVMu6zFHvij5o00NleV4P9-8gU8vf2oudjCMP2EEMlo0NjhDSFKyP3rBjwcQoCCB9EAcMHThEK0Ah9km9P9MZN58:1u2FFD:DC6zpMh4t_u_c4aZMa9b0y0KRsPyLmuj5THQ4d7m8ls','2025-04-08 21:08:27.124631');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_category`
--

DROP TABLE IF EXISTS `inventory_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_category`
--

LOCK TABLES `inventory_category` WRITE;
/*!40000 ALTER TABLE `inventory_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventorylog`
--

DROP TABLE IF EXISTS `inventory_inventorylog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventorylog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `reason` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  `quantity_change` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_inventoryl_created_by_id_8d5d00f5_fk_accounts_` (`created_by_id`),
  KEY `inventory_inventoryl_product_id_eba27e8c_fk_inventory` (`product_id`),
  CONSTRAINT `inventory_inventoryl_created_by_id_8d5d00f5_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `inventory_inventoryl_product_id_eba27e8c_fk_inventory` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventorylog`
--

LOCK TABLES `inventory_inventorylog` WRITE;
/*!40000 ALTER TABLE `inventory_inventorylog` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_inventorylog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_product`
--

DROP TABLE IF EXISTS `inventory_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int unsigned NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `discount` decimal(5,2) NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sku` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `alert_threshold` int unsigned NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `inventory_p_name_f6a6a1_idx` (`name`),
  KEY `inventory_p_sku_f85905_idx` (`sku`),
  KEY `inventory_p_categor_607069_idx` (`category_id`),
  KEY `inventory_p_quantit_785b60_idx` (`quantity`),
  KEY `inventory_p_expiry__8b79d9_idx` (`expiry_date`),
  CONSTRAINT `inventory_product_category_id_c907876e_fk_inventory_category_id` FOREIGN KEY (`category_id`) REFERENCES `inventory_category` (`id`),
  CONSTRAINT `inventory_product_chk_1` CHECK ((`quantity` >= 0)),
  CONSTRAINT `inventory_product_chk_2` CHECK ((`alert_threshold` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_product`
--

LOCK TABLES `inventory_product` WRITE;
/*!40000 ALTER TABLE `inventory_product` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_stock`
--

DROP TABLE IF EXISTS `inventory_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_stock` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `location` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_stock_created_by_id_463319f4_fk_accounts_user_id` (`created_by_id`),
  KEY `inventory_stock_product_id_b75f69ba_fk_inventory_product_id` (`product_id`),
  CONSTRAINT `inventory_stock_created_by_id_463319f4_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `inventory_stock_product_id_b75f69ba_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `inventory_stock_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_stock`
--

LOCK TABLES `inventory_stock` WRITE;
/*!40000 ALTER TABLE `inventory_stock` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_order`
--

DROP TABLE IF EXISTS `orders_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `order_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_date` datetime(6) NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `shipping_address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `contact_phone` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `shipping_charges` decimal(10,2) NOT NULL,
  `discount_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `payment_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `customer_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `orders_orde_order_n_f3ada5_idx` (`order_number`),
  KEY `orders_orde_custome_59b6fb_idx` (`customer_id`),
  KEY `orders_orde_order_d_d71205_idx` (`order_date`),
  KEY `orders_orde_status_c6dd84_idx` (`status`),
  KEY `orders_orde_payment_bc131d_idx` (`payment_status`),
  CONSTRAINT `orders_order_customer_id_0b76f6a4_fk_accounts_user_id` FOREIGN KEY (`customer_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_order`
--

LOCK TABLES `orders_order` WRITE;
/*!40000 ALTER TABLE `orders_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_orderitem`
--

DROP TABLE IF EXISTS `orders_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `discount_percentage` decimal(5,2) NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`),
  KEY `orders_orderitem_product_id_afe4254a_fk_inventory_product_id` (`product_id`),
  CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_orderitem_product_id_afe4254a_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `orders_orderitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_orderitem`
--

LOCK TABLES `orders_orderitem` WRITE;
/*!40000 ALTER TABLE `orders_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders_ordertracking`
--

DROP TABLE IF EXISTS `orders_ordertracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders_ordertracking` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `comments` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_id` bigint NOT NULL,
  `updated_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_ordertracking_order_id_6106ae00_fk_orders_order_id` (`order_id`),
  KEY `orders_ordertracking_updated_by_id_07a0a99a_fk_accounts_user_id` (`updated_by_id`),
  CONSTRAINT `orders_ordertracking_order_id_6106ae00_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`),
  CONSTRAINT `orders_ordertracking_updated_by_id_07a0a99a_fk_accounts_user_id` FOREIGN KEY (`updated_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders_ordertracking`
--

LOCK TABLES `orders_ordertracking` WRITE;
/*!40000 ALTER TABLE `orders_ordertracking` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders_ordertracking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_promotion`
--

DROP TABLE IF EXISTS `promotions_promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions_promotion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `discount_value` decimal(10,2) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `usage_limit` int unsigned NOT NULL,
  `usage_count` int unsigned NOT NULL,
  `min_purchase_amount` decimal(10,2) NOT NULL,
  `applies_to` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  CONSTRAINT `promotions_promotion_chk_1` CHECK ((`usage_limit` >= 0)),
  CONSTRAINT `promotions_promotion_chk_2` CHECK ((`usage_count` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_promotion`
--

LOCK TABLES `promotions_promotion` WRITE;
/*!40000 ALTER TABLE `promotions_promotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_promotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_promotioncategory`
--

DROP TABLE IF EXISTS `promotions_promotioncategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions_promotioncategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint NOT NULL,
  `promotion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `promotions_promotioncate_promotion_id_category_id_d631d352_uniq` (`promotion_id`,`category_id`),
  KEY `promotions_promotion_category_id_04dc04de_fk_inventory` (`category_id`),
  CONSTRAINT `promotions_promotion_category_id_04dc04de_fk_inventory` FOREIGN KEY (`category_id`) REFERENCES `inventory_category` (`id`),
  CONSTRAINT `promotions_promotion_promotion_id_ea49cef4_fk_promotion` FOREIGN KEY (`promotion_id`) REFERENCES `promotions_promotion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_promotioncategory`
--

LOCK TABLES `promotions_promotioncategory` WRITE;
/*!40000 ALTER TABLE `promotions_promotioncategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_promotioncategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_promotionproduct`
--

DROP TABLE IF EXISTS `promotions_promotionproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions_promotionproduct` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_id` bigint NOT NULL,
  `promotion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `promotions_promotionprod_promotion_id_product_id_ea847a36_uniq` (`promotion_id`,`product_id`),
  KEY `promotions_promotion_product_id_df0006f1_fk_inventory` (`product_id`),
  CONSTRAINT `promotions_promotion_product_id_df0006f1_fk_inventory` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `promotions_promotion_promotion_id_c3bc2266_fk_promotion` FOREIGN KEY (`promotion_id`) REFERENCES `promotions_promotion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_promotionproduct`
--

LOCK TABLES `promotions_promotionproduct` WRITE;
/*!40000 ALTER TABLE `promotions_promotionproduct` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_promotionproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `promotions_usedpromotion`
--

DROP TABLE IF EXISTS `promotions_usedpromotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `promotions_usedpromotion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `order_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `used_date` datetime(6) NOT NULL,
  `discount_amount` decimal(10,2) NOT NULL,
  `promotion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `promotions_usedpromo_promotion_id_cd18cb7d_fk_promotion` (`promotion_id`),
  CONSTRAINT `promotions_usedpromo_promotion_id_cd18cb7d_fk_promotion` FOREIGN KEY (`promotion_id`) REFERENCES `promotions_promotion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `promotions_usedpromotion`
--

LOCK TABLES `promotions_usedpromotion` WRITE;
/*!40000 ALTER TABLE `promotions_usedpromotion` DISABLE KEYS */;
/*!40000 ALTER TABLE `promotions_usedpromotion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports_savedreport`
--

DROP TABLE IF EXISTS `reports_savedreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports_savedreport` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `report_type` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `parameters` json NOT NULL,
  `is_shared` tinyint(1) NOT NULL,
  `created_by_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reports_savedreport_created_by_id_0558e77e_fk_accounts_user_id` (`created_by_id`),
  CONSTRAINT `reports_savedreport_created_by_id_0558e77e_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports_savedreport`
--

LOCK TABLES `reports_savedreport` WRITE;
/*!40000 ALTER TABLE `reports_savedreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `reports_savedreport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns_return`
--

DROP TABLE IF EXISTS `returns_return`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns_return` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `return_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `return_reason` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `requested_date` datetime(6) NOT NULL,
  `approved_date` datetime(6) DEFAULT NULL,
  `received_date` datetime(6) DEFAULT NULL,
  `completed_date` datetime(6) DEFAULT NULL,
  `refund_amount` decimal(10,2) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `approved_by_id` bigint DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `customer_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `return_number` (`return_number`),
  KEY `returns_return_approved_by_id_3c295b5c_fk_accounts_user_id` (`approved_by_id`),
  KEY `returns_return_created_by_id_89acd875_fk_accounts_user_id` (`created_by_id`),
  KEY `returns_return_customer_id_ca236a36_fk_accounts_user_id` (`customer_id`),
  KEY `returns_return_order_id_acc0b89a_fk_orders_order_id` (`order_id`),
  CONSTRAINT `returns_return_approved_by_id_3c295b5c_fk_accounts_user_id` FOREIGN KEY (`approved_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `returns_return_created_by_id_89acd875_fk_accounts_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `returns_return_customer_id_ca236a36_fk_accounts_user_id` FOREIGN KEY (`customer_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `returns_return_order_id_acc0b89a_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns_return`
--

LOCK TABLES `returns_return` WRITE;
/*!40000 ALTER TABLE `returns_return` DISABLE KEYS */;
/*!40000 ALTER TABLE `returns_return` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns_returnitem`
--

DROP TABLE IF EXISTS `returns_returnitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns_returnitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int unsigned NOT NULL,
  `reason_detail` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `order_item_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  `return_request_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `returns_returnitem_order_item_id_71656c52_fk_orders_orderitem_id` (`order_item_id`),
  KEY `returns_returnitem_product_id_25ea54fc_fk_inventory_product_id` (`product_id`),
  KEY `returns_returnitem_return_request_id_b069660a_fk_returns_r` (`return_request_id`),
  CONSTRAINT `returns_returnitem_order_item_id_71656c52_fk_orders_orderitem_id` FOREIGN KEY (`order_item_id`) REFERENCES `orders_orderitem` (`id`),
  CONSTRAINT `returns_returnitem_product_id_25ea54fc_fk_inventory_product_id` FOREIGN KEY (`product_id`) REFERENCES `inventory_product` (`id`),
  CONSTRAINT `returns_returnitem_return_request_id_b069660a_fk_returns_r` FOREIGN KEY (`return_request_id`) REFERENCES `returns_return` (`id`),
  CONSTRAINT `returns_returnitem_chk_1` CHECK ((`quantity` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns_returnitem`
--

LOCK TABLES `returns_returnitem` WRITE;
/*!40000 ALTER TABLE `returns_returnitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `returns_returnitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `returns_returnstatushistory`
--

DROP TABLE IF EXISTS `returns_returnstatushistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `returns_returnstatushistory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `comment` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `return_request_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `returns_returnstatus_created_by_id_5798eaff_fk_accounts_` (`created_by_id`),
  KEY `returns_returnstatus_return_request_id_7b771d7e_fk_returns_r` (`return_request_id`),
  CONSTRAINT `returns_returnstatus_created_by_id_5798eaff_fk_accounts_` FOREIGN KEY (`created_by_id`) REFERENCES `accounts_user` (`id`),
  CONSTRAINT `returns_returnstatus_return_request_id_7b771d7e_fk_returns_r` FOREIGN KEY (`return_request_id`) REFERENCES `returns_return` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `returns_returnstatushistory`
--

LOCK TABLES `returns_returnstatushistory` WRITE;
/*!40000 ALTER TABLE `returns_returnstatushistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `returns_returnstatushistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-18 15:39:56
