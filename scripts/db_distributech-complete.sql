-- Adminer 5.3.0 MySQL 9.3.0 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `commandes`;
CREATE TABLE `commandes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `num_commande` varchar(20) NOT NULL,
  `date_commande` date NOT NULL,
  `nb_exemplaire` int NOT NULL,
  `revendeur` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `revendeur` (`revendeur`),
  CONSTRAINT `commandes_ibfk_1` FOREIGN KEY (`revendeur`) REFERENCES `revendeurs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `commandes` (`id`, `num_commande`, `date_commande`, `nb_exemplaire`, `revendeur`) VALUES
(1,	'CMD-20250710-001',	'2025-07-10',	5,	1),
(2,	'CMD-20250710-001',	'2025-07-10',	10,	1),
(3,	'CMD-20250710-001',	'2025-07-10',	2,	1),
(4,	'CMD-20250711-001',	'2025-07-11',	3,	1),
(5,	'CMD-20250711-001',	'2025-07-11',	4,	1);

DROP TABLE IF EXISTS `commandes_produits`;
CREATE TABLE `commandes_produits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `produit` int NOT NULL,
  `commande` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_produit` (`produit`),
  KEY `idx_commande` (`commande`),
  CONSTRAINT `commandes_produits_ibfk_1` FOREIGN KEY (`commande`) REFERENCES `commandes` (`id`),
  CONSTRAINT `commandes_produits_ibfk_2` FOREIGN KEY (`produit`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `commandes_produits` (`id`, `produit`, `commande`) VALUES
(1,	101,	1),
(2,	102,	2),
(3,	105,	3),
(4,	108,	4),
(5,	103,	5);

DROP TABLE IF EXISTS `produits`;
CREATE TABLE `produits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ref_produit` varchar(50) NOT NULL,
  `nom_produit` varchar(50) NOT NULL,
  `cout_unitaire` decimal(10,1) NOT NULL,
  `quantite` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `produits` (`id`, `ref_produit`, `nom_produit`, `cout_unitaire`, `quantite`) VALUES
(101,	'OWJ3FOH3',	'Casque Bluetooth',	59.9,	50),
(102,	'KUFGZAPQ',	'Chargeur USB-C',	19.9,	80),
(103,	'CDZFEJGW',	'Enceinte Portable',	89.9,	40),
(104,	'WJ2IEKMK',	'Batterie Externe',	24.9,	60),
(105,	'TJT3VASO',	'Montre Connectée',	129.9,	20),
(106,	'KNO8ZALO',	'Webcam HD',	49.9,	35),
(107,	'0Y6DJKQX',	'Hub USB 3.0',	34.9,	25),
(108,	'W221QE7A',	'Clavier sans fil',	44.9,	30),
(109,	'VNXWJIMR',	'Souris ergonomique',	39.9,	45),
(110,	'1JJQO3XO',	'Station d\'accueil',	109.9,	15);

DROP TABLE IF EXISTS `regions`;
CREATE TABLE `regions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_region` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `regions` (`id`, `nom_region`) VALUES
(1,	'Île-de-France'),
(2,	'Occitanie'),
(3,	'Auvergne-Rhône-Alpes'),
(4,	'Bretagne');

DROP TABLE IF EXISTS `revendeurs`;
CREATE TABLE `revendeurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_revendeur` varchar(50) NOT NULL,
  `ref_revendeur` varchar(50) NOT NULL,
  `region` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region` (`region`),
  CONSTRAINT `revendeurs_ibfk_1` FOREIGN KEY (`region`) REFERENCES `regions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `revendeurs` (`id`, `nom_revendeur`, `ref_revendeur`, `region`) VALUES
(1,	'TechExpress',	'9XRLA6IT',	1),
(2,	'ElectroZone',	'OXPD7TW6',	1),
(3,	'SudTech',	'A24IQHLR',	2),
(4,	'GadgetShop',	'LQ6W6SAJ',	2),
(5,	'Connectik',	'TSZPGSRF',	3),
(6,	'Domotik+',	'NEA1LCYH',	3),
(7,	'BreizhTech',	'QQEMT9SJ',	4),
(8,	'SmartBretagne',	'GH56VRAR',	4),
(9,	'HighNord',	'NHUKEJI1',	1),
(10,	'OuestConnect',	'RFAB85T7',	4);

DROP VIEW IF EXISTS `stock_courant`;
CREATE TABLE `stock_courant` (`id` int, `nom_produit` varchar(50), `quantite` int, `nb_exemplaire` int, `stock_courant` bigint);


DROP TABLE IF EXISTS `stock_produits`;
CREATE TABLE `stock_produits` (
  `id` int NOT NULL AUTO_INCREMENT,
  `produit` int NOT NULL,
  `stock` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_produit` (`produit`),
  KEY `idx_stock` (`stock`),
  CONSTRAINT `stock_produits_ibfk_1` FOREIGN KEY (`stock`) REFERENCES `stocks` (`id`),
  CONSTRAINT `stock_produits_ibfk_2` FOREIGN KEY (`produit`) REFERENCES `produits` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `stock_produits` (`id`, `produit`, `stock`) VALUES
(1,	101,	1),
(2,	102,	2),
(3,	103,	3),
(4,	104,	4),
(5,	105,	5),
(6,	106,	6),
(7,	107,	7),
(8,	108,	8),
(9,	109,	9),
(10,	110,	10);

DROP TABLE IF EXISTS `stocks`;
CREATE TABLE `stocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `stock_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `stocks` (`id`, `stock_date`) VALUES
(1,	'2025-07-01'),
(2,	'2025-07-01'),
(3,	'2025-07-02'),
(4,	'2025-07-02'),
(5,	'2025-07-03'),
(6,	'2025-07-03'),
(7,	'2025-07-04'),
(8,	'2025-07-04'),
(9,	'2025-07-05'),
(10,	'2025-07-05');

DROP VIEW IF EXISTS `total_commande`;
CREATE TABLE `total_commande` (`num_commande` varchar(20), `id` int, `cout_unitaire` decimal(10,1), `nb_exemplaire` int, `total_commande` decimal(20,1));


DROP TABLE IF EXISTS `stock_courant`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `stock_courant` AS select `p`.`id` AS `id`,`p`.`nom_produit` AS `nom_produit`,`p`.`quantite` AS `quantite`,`c`.`nb_exemplaire` AS `nb_exemplaire`,(`p`.`quantite` - `c`.`nb_exemplaire`) AS `stock_courant` from ((`produits` `p` join `commandes_produits` `cp` on((`p`.`id` = `cp`.`produit`))) join `commandes` `c` on((`cp`.`commande` = `c`.`id`)));

DROP TABLE IF EXISTS `total_commande`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `total_commande` AS select `c`.`num_commande` AS `num_commande`,`p`.`id` AS `id`,`p`.`cout_unitaire` AS `cout_unitaire`,`c`.`nb_exemplaire` AS `nb_exemplaire`,(`p`.`cout_unitaire` * `c`.`nb_exemplaire`) AS `total_commande` from ((`produits` `p` join `commandes_produits` `cp` on((`p`.`id` = `cp`.`produit`))) join `commandes` `c` on((`cp`.`commande` = `c`.`id`)));

-- 2025-08-19 14:17:52 UTC
