/*
 Navicat Premium Data Transfer

 Source Server         : Localhost - Mysql
 Source Server Type    : MySQL
 Source Server Version : 50711
 Source Host           : localhost
 Source Database       : 99

 Target Server Type    : MySQL
 Target Server Version : 50711
 File Encoding         : utf-8

 Date: 03/28/2016 23:39:33 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `table_listing`
-- ----------------------------
DROP TABLE IF EXISTS `table_listing`;
CREATE TABLE `table_listing` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `user` bigint(11) NOT NULL,
  `price` float NOT NULL,
  `listing_type` enum('rent','sale') COLLATE utf8_bin NOT NULL DEFAULT 'rent',
  `postal_code` char(6) COLLATE utf8_bin NOT NULL DEFAULT '',
  `status` enum('active','closed','deleted') COLLATE utf8_bin NOT NULL DEFAULT 'active',
  PRIMARY KEY (`id`),
  KEY `fk_user` (`user`),
  KEY `k_postalcode` (`postal_code`),
  KEY `k_price` (`price`),
  CONSTRAINT `fk_user` FOREIGN KEY (`user`) REFERENCES `table_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='listing table: store listing information';

-- ----------------------------
--  Records of `table_listing`
-- ----------------------------
BEGIN;
INSERT INTO `table_listing` VALUES ('2', '1', '11111', 'rent', '123456', 'active'), ('3', '1', '110', 'sale', '123456', 'active'), ('4', '11', '110', 'sale', '123456', 'active'), ('13', '11', '1110', 'sale', '123456', 'active');
COMMIT;

-- ----------------------------
--  Table structure for `table_user`
-- ----------------------------
DROP TABLE IF EXISTS `table_user`;
CREATE TABLE `table_user` (
  `id` bigint(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `address` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `k_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='user table: store user information';

-- ----------------------------
--  Records of `table_user`
-- ----------------------------
BEGIN;
INSERT INTO `table_user` VALUES ('1', 'qian', '', '2016-03-28 16:41:30', '2016-03-28 16:41:30', null), ('9', 'qian1', 'singapore1', '2016-03-28 21:41:29', '2016-03-28 21:41:29', null), ('10', 'qian2', 'singapore2', '2016-03-28 21:41:44', '2016-03-28 21:41:44', null), ('11', 'qian3', 'singapore3', '2016-03-28 21:41:54', '2016-03-28 21:41:54', null);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
