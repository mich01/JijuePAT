-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.3.25-MariaDB-0ubuntu0.20.04.1 - Ubuntu 20.04
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             10.1.0.5464
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for jijue_db
CREATE DATABASE IF NOT EXISTS `jijue_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `jijue_db`;

-- Dumping structure for table jijue_db.tbl_Accessible_tests
CREATE TABLE IF NOT EXISTS `tbl_Accessible_tests` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` bigint(20) NOT NULL,
  `TestID` bigint(20) NOT NULL,
  `AdminID` bigint(20) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_AnswerMapping
CREATE TABLE IF NOT EXISTS `tbl_AnswerMapping` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `QuestionID` int(11) DEFAULT NULL,
  `AnswerID` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_AnswerOptions
CREATE TABLE IF NOT EXISTS `tbl_AnswerOptions` (
  `AnswerID` int(11) NOT NULL AUTO_INCREMENT,
  `AnswerDesc` varchar(500) NOT NULL,
  `Score` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`AnswerID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Assessment
CREATE TABLE IF NOT EXISTS `tbl_Assessment` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `TestID` int(11) NOT NULL,
  `QuestionID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `UserAdding` int(11) NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Assessors
CREATE TABLE IF NOT EXISTS `tbl_Assessors` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) NOT NULL,
  `AssessorID` int(11) NOT NULL,
  `AssignerID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Career
CREATE TABLE IF NOT EXISTS `tbl_Career` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `CareerName` varchar(7) NOT NULL,
  `Description` int(11) NOT NULL,
  `TScore1` int(11) NOT NULL,
  `TScore2` int(11) NOT NULL,
  `TScore3` int(11) NOT NULL,
  `TScore4` int(11) NOT NULL,
  `TScore5` int(11) NOT NULL,
  `TScore6` int(11) NOT NULL,
  `TScore7` int(11) NOT NULL,
  `TScore8` int(11) NOT NULL,
  `TScore9` int(11) NOT NULL,
  `TScore10` int(11) NOT NULL,
  `TScore11` int(11) NOT NULL,
  `TScore12` int(11) NOT NULL,
  `TScore13` int(11) NOT NULL,
  `TScore14` int(11) NOT NULL,
  `TScore15` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Gender
CREATE TABLE IF NOT EXISTS `tbl_Gender` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Gender` varchar(7) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_messages
CREATE TABLE IF NOT EXISTS `tbl_messages` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `Sender` bigint(20) NOT NULL DEFAULT 0,
  `Reciever` bigint(20) NOT NULL DEFAULT 0,
  `Message` text DEFAULT NULL,
  `Status` int(11) NOT NULL DEFAULT 1,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_network
CREATE TABLE IF NOT EXISTS `tbl_network` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `FromID` int(11) NOT NULL,
  `ToID` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Personality_Type
CREATE TABLE IF NOT EXISTS `tbl_Personality_Type` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `Personality_Type` varchar(50) NOT NULL DEFAULT '0',
  `Description` longtext NOT NULL,
  `Avatar` varchar(20) NOT NULL DEFAULT '0',
  `Attribute` varchar(20) NOT NULL DEFAULT '0',
  `Min` int(11) NOT NULL DEFAULT 0,
  `Max` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Questions
CREATE TABLE IF NOT EXISTS `tbl_Questions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Question` varchar(1000) NOT NULL,
  `Description` varchar(500) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `MediaSource` varchar(500) DEFAULT NULL,
  `MediaType` varchar(100) NOT NULL,
  `ModelID` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Roles
CREATE TABLE IF NOT EXISTS `tbl_Roles` (
  `Role_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Role_type` varchar(100) NOT NULL,
  `Description` varchar(100) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`Role_ID`),
  UNIQUE KEY `Role_ID` (`Role_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Status
CREATE TABLE IF NOT EXISTS `tbl_Status` (
  `Status_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Status_type` varchar(100) NOT NULL,
  `Description` varchar(100) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`Status_ID`),
  UNIQUE KEY `Status_ID` (`Status_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Summary
CREATE TABLE IF NOT EXISTS `tbl_Summary` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` int(11) NOT NULL DEFAULT 0,
  `TestID` int(11) NOT NULL DEFAULT 0,
  `Extraversion` int(11) NOT NULL DEFAULT 0,
  `Neuroticism` int(11) NOT NULL DEFAULT 0,
  `Agreeableness` int(11) NOT NULL DEFAULT 0,
  `Consientious` int(11) NOT NULL DEFAULT 0,
  `Compassion` int(11) NOT NULL DEFAULT 0,
  `Politeness` int(11) NOT NULL DEFAULT 0,
  `Industriousness` int(11) NOT NULL DEFAULT 0,
  `Orderliness` int(11) NOT NULL DEFAULT 0,
  `Enthusiasm` int(11) NOT NULL DEFAULT 0,
  `Assertiveness` int(11) NOT NULL DEFAULT 0,
  `Withdrawal` int(11) NOT NULL DEFAULT 0,
  `Volatility` int(11) NOT NULL DEFAULT 0,
  `Openess_to_Experience` int(11) NOT NULL DEFAULT 0,
  `Intellect` int(11) NOT NULL DEFAULT 0,
  `Openness` int(11) NOT NULL DEFAULT 0,
  `Anxiety` int(11) NOT NULL DEFAULT 0,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Depression` int(11) NOT NULL DEFAULT 0,
  `Anger` int(11) NOT NULL DEFAULT 0,
  `IQ` int(11) NOT NULL DEFAULT 0,
  `PTSD` int(11) NOT NULL DEFAULT 0,
  `Likable` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_Tests
CREATE TABLE IF NOT EXISTS `tbl_Tests` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Description` varchar(500) NOT NULL,
  `Status` varchar(7) NOT NULL,
  `Creator` bigint(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `TestType` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_TestStatus
CREATE TABLE IF NOT EXISTS `tbl_TestStatus` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `TestID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `DateStarted` datetime NOT NULL,
  `DateCompleted` datetime DEFAULT NULL,
  `TestStatus` varchar(50) NOT NULL,
  PRIMARY KEY (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_users
CREATE TABLE IF NOT EXISTS `tbl_users` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `User_Status` int(11) unsigned NOT NULL,
  `UserName` varchar(100) NOT NULL,
  `Sur_Name` varchar(100) NOT NULL,
  `Other_Names` varchar(100) NOT NULL,
  `Pass_word` varchar(500) NOT NULL,
  `Date_Created` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `GenderID` int(11) NOT NULL,
  `DoB` date DEFAULT NULL,
  `Role_ID` int(11) NOT NULL,
  `EmailAddress` varchar(50) DEFAULT NULL,
  `img` varchar(100) DEFAULT NULL,
  `Nationality` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ID` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.
-- Dumping structure for table jijue_db.tbl_userTests
CREATE TABLE IF NOT EXISTS `tbl_userTests` (
  `UID` int(11) NOT NULL AUTO_INCREMENT,
  `TestID` int(11) DEFAULT NULL,
  `QuestionID` int(11) DEFAULT NULL,
  `UserID` int(11) DEFAULT NULL,
  `timeCompleted` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UID`),
  KEY `UID` (`UID`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
