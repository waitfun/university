/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 100131
Source Host           : localhost:3306
Source Database       : hnust_student

Target Server Type    : MYSQL
Target Server Version : 100131
File Encoding         : 65001

Date: 2018-11-15 10:52:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hnust_teacher
-- ----------------------------
DROP TABLE IF EXISTS `hnust_teacher`;
CREATE TABLE `hnust_teacher` (
  `teacher_no` int(11) NOT NULL,
  `teacher_name` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `native_place` varchar(255) DEFAULT NULL,
  `sex` varchar(25) DEFAULT NULL,
  `qq` varchar(100) DEFAULT NULL,
  `card_no` varchar(100) DEFAULT NULL,
  `nation` varchar(25) DEFAULT NULL,
  `profess` varchar(100) DEFAULT NULL,
  `jion_time` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`teacher_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
