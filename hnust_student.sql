/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 100131
Source Host           : localhost:3306
Source Database       : hnust_student

Target Server Type    : MYSQL
Target Server Version : 100131
File Encoding         : 65001

Date: 2018-11-15 10:52:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for hnust_student
-- ----------------------------
DROP TABLE IF EXISTS `hnust_student`;
CREATE TABLE `hnust_student` (
  `student_no` int(11) NOT NULL COMMENT '学号',
  `student_name` varchar(50) DEFAULT NULL,
  `sex` varchar(25) DEFAULT NULL,
  `xy` varchar(255) DEFAULT NULL,
  `zy` varchar(255) DEFAULT NULL,
  `class_name` varchar(255) DEFAULT NULL,
  `birthday` varchar(255) DEFAULT NULL,
  `card_no` varchar(255) DEFAULT NULL,
  `entrance_time` varchar(100) DEFAULT NULL,
  `nation` varchar(25) DEFAULT NULL,
  `native_place` varchar(255) DEFAULT NULL,
  `political` varchar(25) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `style` int(11) DEFAULT '0' COMMENT '1本部，2潇湘',
  `qq` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`student_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
