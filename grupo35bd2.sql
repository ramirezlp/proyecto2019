-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 09-12-2019 a las 22:08:05
-- Versión del servidor: 5.5.24-log
-- Versión de PHP: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `grupo35`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administracion_orquesta`
--

CREATE TABLE IF NOT EXISTS `administracion_orquesta` (
  `titulo` varchar(100) DEFAULT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `mail_contacto` varchar(100) DEFAULT NULL,
  `sitio_activo` tinyint(1) DEFAULT '1',
  `elementos_por_pagina` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `administracion_orquesta`
--

INSERT INTO `administracion_orquesta` (`titulo`, `descripcion`, `mail_contacto`, `sitio_activo`, `elementos_por_pagina`, `id`, `created`) VALUES
('Orquesta Escuela de Berisso', 'Buenos Aires', 'orquestaBerisso@escuela.com', 1, 2, 1, '2019-10-27 05:53:58');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_taller_ciclo_lectivo_dia`
--

CREATE TABLE IF NOT EXISTS `asistencia_taller_ciclo_lectivo_dia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ciclo_lectivo_taller_horario` int(11) DEFAULT NULL,
  `estudiante_id` int(11) DEFAULT NULL,
  `dia` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ciclo_lectivo_taller_horario` (`ciclo_lectivo_taller_horario`),
  KEY `estudiante_id` (`estudiante_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `asistencia_taller_ciclo_lectivo_dia`
--

INSERT INTO `asistencia_taller_ciclo_lectivo_dia` (`id`, `ciclo_lectivo_taller_horario`, `estudiante_id`, `dia`) VALUES
(1, 42, 3, '2019-12-09 18:59:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `barrio`
--

CREATE TABLE IF NOT EXISTS `barrio` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=26 ;

--
-- Volcado de datos para la tabla `barrio`
--

INSERT INTO `barrio` (`id`, `nombre`) VALUES
(1, 'Barrio Náutico'),
(2, 'Barrio Obrero'),
(3, 'Berisso'),
(4, 'Barrio Solidaridad'),
(5, 'Barrio Obrero'),
(6, 'Barrio Bco. Pcia.'),
(7, 'Barrio J.B. Justo'),
(8, 'Barrio Obrero'),
(9, 'El Carmen'),
(10, 'El Labrador'),
(11, 'Ensenada'),
(12, 'La Hermosura'),
(13, 'La PLata'),
(14, 'Los Talas'),
(15, 'Ringuelet'),
(16, 'Tolosa'),
(17, 'Villa Alba'),
(18, 'Villa Arguello'),
(19, 'Villa B. C'),
(20, 'Villa Elvira'),
(21, 'Villa Nueva'),
(22, 'Villa Paula'),
(23, 'Villa Progreso'),
(24, 'Villa San Carlos'),
(25, 'Villa Zula');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo`
--

CREATE TABLE IF NOT EXISTS `ciclo_lectivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_ini` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `semestre` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- Volcado de datos para la tabla `ciclo_lectivo`
--

INSERT INTO `ciclo_lectivo` (`id`, `fecha_ini`, `fecha_fin`, `semestre`) VALUES
(1, '2019-11-05 00:00:00', '2019-11-15 00:00:00', 1),
(2, '2013-04-02 00:00:00', '2019-02-01 00:00:00', 2),
(3, '2019-08-03 00:00:00', '2019-12-02 00:00:00', 2),
(4, '2019-06-06 00:00:00', '2019-12-30 00:00:00', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo_taller`
--

CREATE TABLE IF NOT EXISTS `ciclo_lectivo_taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taller_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `nucleo_id` int(255) DEFAULT NULL,
  `ciclo_lectivo_taller_horario_id` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_ciclo_lectivo_taller_ciclo_lectivo_id` (`ciclo_lectivo_id`),
  KEY `FK_ciclo_lectivo_taller_taller_id` (`taller_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=12 ;

--
-- Volcado de datos para la tabla `ciclo_lectivo_taller`
--

INSERT INTO `ciclo_lectivo_taller` (`id`, `taller_id`, `ciclo_lectivo_id`, `nucleo_id`, `ciclo_lectivo_taller_horario_id`) VALUES
(1, 2, 2, 2, 1),
(2, 1, 1, 2, 2),
(8, 2, 1, NULL, NULL),
(9, 2, 3, NULL, NULL),
(10, 2, 4, NULL, NULL),
(11, 1, 4, 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo_taller_horario`
--

CREATE TABLE IF NOT EXISTS `ciclo_lectivo_taller_horario` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `ciclo_lectivo_taller_id` int(255) NOT NULL,
  `horario_id` int(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=43 ;

--
-- Volcado de datos para la tabla `ciclo_lectivo_taller_horario`
--

INSERT INTO `ciclo_lectivo_taller_horario` (`id`, `ciclo_lectivo_taller_id`, `horario_id`) VALUES
(35, 0, 5),
(36, 1, 1),
(37, 1, 3),
(38, 1, 2),
(39, 1, 4),
(40, 2, 4),
(41, 2, 1),
(42, 11, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clase_taller_ciclo_lectivo`
--

CREATE TABLE IF NOT EXISTS `clase_taller_ciclo_lectivo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taller_ciclo_lectivo_id` int(11) DEFAULT NULL,
  `dia_semana` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `taller_ciclo_lectivo_id` (`taller_ciclo_lectivo_id`),
  KEY `dia_semana` (`dia_semana`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dia_semana`
--

CREATE TABLE IF NOT EXISTS `dia_semana` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dia` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docente`
--

CREATE TABLE IF NOT EXISTS `docente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero_documento` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_genero_docente_id` (`genero_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `docente`
--

INSERT INTO `docente` (`id`, `apellido`, `nombre`, `fecha_nac`, `localidad_id`, `domicilio`, `genero_id`, `tipo_doc_id`, `numero_documento`, `tel`) VALUES
(2, 'dvcsd', 'casc', '1999-01-01', 1, 'calle 123', 1, 1, 10011111, ''),
(6, 'sandler', 'hola2', '2017-12-01', 1, 'calle 123', 1, 1, 553543, '2216458766');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docente_responsable_taller`
--

CREATE TABLE IF NOT EXISTS `docente_responsable_taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docente_id` int(11) DEFAULT NULL,
  `ciclo_lectivo_taller_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `docente_id` (`docente_id`),
  KEY `ciclo_lectivo_taller_id` (`ciclo_lectivo_taller_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `docente_responsable_taller`
--

INSERT INTO `docente_responsable_taller` (`id`, `docente_id`, `ciclo_lectivo_taller_id`) VALUES
(1, 2, 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escuela`
--

CREATE TABLE IF NOT EXISTS `escuela` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=157 ;

--
-- Volcado de datos para la tabla `escuela`
--

INSERT INTO `escuela` (`id`, `nombre`, `direccion`, `telefono`) VALUES
(1, '502', NULL, NULL),
(2, 'Albert Thomas', NULL, NULL),
(3, 'Anexa', NULL, NULL),
(4, 'Anexo T. Speroni', NULL, NULL),
(5, 'Basiliana', NULL, NULL),
(6, 'Basiliano', NULL, NULL),
(7, 'Bellas Artes', NULL, NULL),
(8, 'Canossiano', NULL, NULL),
(9, 'Castañeda', NULL, NULL),
(10, 'Col. Nacional', NULL, NULL),
(11, 'Conquista Cristiana', NULL, NULL),
(12, 'Dardo Rocha N° 24', NULL, NULL),
(13, 'E.E.M.N° 2', NULL, NULL),
(14, 'E.M. N°26', NULL, NULL),
(15, 'E.P. Municipal N° 2', NULL, NULL),
(16, 'EE N° 2', NULL, NULL),
(17, 'EEE N° 501', NULL, NULL),
(18, 'EEE N°501', NULL, NULL),
(19, 'EEM N° 1', NULL, NULL),
(20, 'EEM N° 26 L.P', NULL, NULL),
(21, 'EEM N°128', NULL, NULL),
(22, 'EEM N°2', NULL, NULL),
(23, 'EES N° 10', NULL, NULL),
(24, 'EES N° 14', NULL, NULL),
(25, 'EES N° 4', NULL, NULL),
(26, 'EES N° 4 Berisso', NULL, NULL),
(27, 'EES N° 4 El Pino', NULL, NULL),
(28, 'EEST N° 1 bsso', NULL, NULL),
(29, 'EET Nº 1', NULL, NULL),
(30, 'EET Nº1', NULL, NULL),
(31, 'EGB N°25', NULL, NULL),
(32, 'EM N° 2', NULL, NULL),
(33, 'EMM N° 3', NULL, NULL),
(34, 'EP N° 1 L.P-', NULL, NULL),
(35, 'EP N° 11', NULL, NULL),
(36, 'EP N° 129', NULL, NULL),
(37, 'EP N° 14', NULL, NULL),
(38, 'EP N° 15', NULL, NULL),
(39, 'EP N° 17', NULL, NULL),
(40, 'EP N° 18', NULL, NULL),
(41, 'EP N° 19', NULL, NULL),
(42, 'EP N° 2', NULL, NULL),
(43, 'EP N° 20', NULL, NULL),
(44, 'EP N° 22', NULL, NULL),
(45, 'EP N° 25', NULL, NULL),
(46, 'EP N° 27', NULL, NULL),
(47, 'EP N° 3', NULL, NULL),
(48, 'EP N° 37 LP', NULL, NULL),
(49, 'EP N° 43', NULL, NULL),
(50, 'EP N° 45', NULL, NULL),
(51, 'EP N° 5', NULL, NULL),
(52, 'EP N° 6', NULL, NULL),
(53, 'EP N° 65 La Plata', NULL, NULL),
(54, 'EP N° 7', NULL, NULL),
(55, 'EPB N° 10', NULL, NULL),
(56, 'EPB N° 14', NULL, NULL),
(57, 'EPB N° 15', NULL, NULL),
(58, 'EPB N° 19', NULL, NULL),
(59, 'EPB N° 2', NULL, NULL),
(60, 'EPB N° 20', NULL, NULL),
(61, 'EPB N° 24', NULL, NULL),
(62, 'EPB N° 25', NULL, NULL),
(63, 'EPB N° 45', NULL, NULL),
(64, 'EPB N° 5', NULL, NULL),
(65, 'EPB N° 55', NULL, NULL),
(66, 'EPB N° 6', NULL, NULL),
(67, 'EPB N° 65', NULL, NULL),
(68, 'EPB N° 8', NULL, NULL),
(69, 'ESB N° 10', NULL, NULL),
(70, 'ESB N° 11', NULL, NULL),
(71, 'ESB N° 14', NULL, NULL),
(72, 'ESB N° 3', NULL, NULL),
(73, 'ESB N° 61', NULL, NULL),
(74, 'ESB N° 66', NULL, NULL),
(75, 'ESB N° 8', NULL, NULL),
(76, 'ESB N° 9', NULL, NULL),
(77, 'ESC N° 10', NULL, NULL),
(78, 'ESC N° 13', NULL, NULL),
(79, 'ESC N° 19', NULL, NULL),
(80, 'ESC N° 2', NULL, NULL),
(81, 'ESC N° 20', NULL, NULL),
(82, 'ESC N° 22', NULL, NULL),
(83, 'ESC N° 23', NULL, NULL),
(84, 'ESC N° 24', NULL, NULL),
(85, 'ESC N° 25', NULL, NULL),
(86, 'ESC N° 27', NULL, NULL),
(87, 'ESC N° 3', NULL, NULL),
(88, 'ESC N° 43', NULL, NULL),
(89, 'ESC N° 45', NULL, NULL),
(90, 'ESC N° 5', NULL, NULL),
(91, 'ESC N° 501', NULL, NULL),
(92, 'ESC N° 6', NULL, NULL),
(93, 'ESC N° 66', NULL, NULL),
(94, 'ESC N° 7', NULL, NULL),
(95, 'ESC N° 8', NULL, NULL),
(96, 'ESC N°11', NULL, NULL),
(97, 'ESC N°17', NULL, NULL),
(98, 'ESC N°19', NULL, NULL),
(99, 'ESC N°3', NULL, NULL),
(100, 'ESC N°7', NULL, NULL),
(101, 'ESC de Arte', NULL, NULL),
(102, 'ESS N° 4', NULL, NULL),
(103, 'Enseñanza Media', NULL, NULL),
(104, 'Especial N° 502', NULL, NULL),
(105, 'Estrada', NULL, NULL),
(106, 'FACULTAD', NULL, NULL),
(107, 'INDUSTRIAL', NULL, NULL),
(108, 'Italiana', NULL, NULL),
(109, 'J 904', NULL, NULL),
(110, 'J. Manuel Strada', NULL, NULL),
(111, 'Jacarandá', NULL, NULL),
(112, 'Jardín Euforion', NULL, NULL),
(113, 'Jardín N° 903', NULL, NULL),
(114, 'Jardín N° 907', NULL, NULL),
(115, 'JoaquinV.Gonzalez', NULL, NULL),
(116, 'Lola Mora sec', NULL, NULL),
(117, 'Lujan Sierra', NULL, NULL),
(118, 'MUNICIOAL 11', NULL, NULL),
(119, 'María Auxiliadora', NULL, NULL),
(120, 'María Reina', NULL, NULL),
(121, 'Media 2 España', NULL, NULL),
(122, 'Media N 1', NULL, NULL),
(123, 'Mercedita de S.Martin', NULL, NULL),
(124, 'Monseñor Alberti', NULL, NULL),
(125, 'Mtro Luis MKEY', NULL, NULL),
(126, 'Mñor. Rasore', NULL, NULL),
(127, 'N1 Francisco', NULL, NULL),
(128, 'Normal 2', NULL, NULL),
(129, 'Normal 3 LP', NULL, NULL),
(130, 'Normal n 2', NULL, NULL),
(131, 'Ntra Sra Lourdes', NULL, NULL),
(132, 'Ntra. Sra. del Valle', NULL, NULL),
(133, 'PSICOLOGIA', NULL, NULL),
(134, 'Parroquial', NULL, NULL),
(135, 'Pasos del Libertedor', NULL, NULL),
(136, 'Ped 61', NULL, NULL),
(137, 'Pedagogica', NULL, NULL),
(138, 'SEC N° 8', NULL, NULL),
(139, 'SEC N°17', NULL, NULL),
(140, 'San Simón', NULL, NULL),
(141, 'Santa Rosa', NULL, NULL),
(142, 'Sra de Fátima', NULL, NULL),
(143, 'Sta Margarita', NULL, NULL),
(144, 'Sta Ro. de Lima', NULL, NULL),
(145, 'Sta Rosa', NULL, NULL),
(146, 'Sta Rosa Lima', NULL, NULL),
(147, 'Sta. R. de Lima', NULL, NULL),
(148, 'Sta. Rosa de lima', NULL, NULL),
(149, 'Técnica N° 1', NULL, NULL),
(150, 'Técnica N° 1 Berisso', NULL, NULL),
(151, 'Técnica N° 5', NULL, NULL),
(152, 'Técnica N° 7', NULL, NULL),
(153, 'UCALP', NULL, NULL),
(154, 'UNLP', NULL, NULL),
(155, 'UTN', NULL, NULL),
(156, 'Universitas', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE IF NOT EXISTS `estudiante` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `nivel_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `escuela_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `documento` int(11) NOT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `barrio_id` int(11) NOT NULL,
  `lugar_de_nacimiento` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `responsable` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `numero_contacto` int(255) NOT NULL,
  `email_contacto` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_nivel_id` (`nivel_id`),
  KEY `FK_genero_estudiante_id` (`genero_id`),
  KEY `FK_escuela_id` (`escuela_id`),
  KEY `FK_barrio_id` (`barrio_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=5 ;

--
-- Volcado de datos para la tabla `estudiante`
--

INSERT INTO `estudiante` (`id`, `apellido`, `nombre`, `fecha_nacimiento`, `localidad_id`, `nivel_id`, `domicilio`, `genero_id`, `escuela_id`, `tipo_doc_id`, `documento`, `telefono`, `barrio_id`, `lugar_de_nacimiento`, `responsable`, `numero_contacto`, `email_contacto`) VALUES
(2, 'njn', 'scac', '2018-01-01', 1, 4, 'calle 123', 1, 2, 1, -1, '2216458766', 6, 'La Plata', 'Padre', 0, ''),
(3, 'dc', 'cas', '2016-12-31', 1, 1, 'calle 123', 1, 1, 1, 77744888, '6464464464', 6, 'La Plata', 'Padre', 2147483647, 'casccasc@vfdv.com'),
(4, 'khbkh', 'dcsdc|', '2017-12-31', 1, 7, 'calle 123', 1, 3, 1, 3535, '68686', 6, 'La Plata', 'Madre', 97987999, 'cascas@fff.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_ciclo_lectivo_taller`
--

CREATE TABLE IF NOT EXISTS `estudiante_ciclo_lectivo_taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estudiante_id` int(11) DEFAULT NULL,
  `ciclo_lectivo_taller_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estudiante_id` (`estudiante_id`),
  KEY `ciclo_lectivo_taller_id` (`ciclo_lectivo_taller_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `estudiante_ciclo_lectivo_taller`
--

INSERT INTO `estudiante_ciclo_lectivo_taller` (`id`, `estudiante_id`, `ciclo_lectivo_taller_id`) VALUES
(1, 2, 1),
(2, 3, 11),
(3, 4, 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_taller`
--

CREATE TABLE IF NOT EXISTS `estudiante_taller` (
  `estudiante_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL,
  PRIMARY KEY (`estudiante_id`,`ciclo_lectivo_id`,`taller_id`),
  KEY `FK_estudiante_taller_ciclo_lectivo_id` (`ciclo_lectivo_id`),
  KEY `FK_estudiante_taller_taller_id` (`taller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE IF NOT EXISTS `genero` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `genero`
--

INSERT INTO `genero` (`id`, `nombre`) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Otro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horario`
--

CREATE TABLE IF NOT EXISTS `horario` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `dia` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Volcado de datos para la tabla `horario`
--

INSERT INTO `horario` (`id`, `dia`) VALUES
(1, 'lunes'),
(2, 'martes'),
(3, 'miercoles'),
(4, 'jueves'),
(5, 'viernes'),
(6, 'sabado'),
(7, 'domingo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instrumento`
--

CREATE TABLE IF NOT EXISTS `instrumento` (
  `numero_inventario` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_instrumento_id` int(11) NOT NULL,
  `imagen` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`numero_inventario`),
  KEY `FK_tipo_instrumento_id` (`tipo_instrumento_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `instrumento`
--

INSERT INTO `instrumento` (`numero_inventario`, `nombre`, `tipo_instrumento_id`, `imagen`) VALUES
('ABC123', 'GUITARRA ELECTRICA', 1, '1542113135_776401_1542116070_noticia_normal.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `issues`
--

CREATE TABLE IF NOT EXISTS `issues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(30) DEFAULT NULL,
  `description` text,
  `category_id` int(10) NOT NULL,
  `status_id` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `status_id` (`status_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Volcado de datos para la tabla `issues`
--

INSERT INTO `issues` (`id`, `email`, `description`, `category_id`, `status_id`) VALUES
(5, 'aslgo', 'asdas', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nivel`
--

CREATE TABLE IF NOT EXISTS `nivel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=13 ;

--
-- Volcado de datos para la tabla `nivel`
--

INSERT INTO `nivel` (`id`, `nombre`) VALUES
(1, 'I'),
(2, 'II'),
(3, 'III'),
(4, 'IV'),
(5, 'V'),
(6, 'VI'),
(7, 'VII'),
(8, 'VIII'),
(9, 'IX'),
(10, 'X'),
(11, 'XI'),
(12, 'XII');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nucleo`
--

CREATE TABLE IF NOT EXISTS `nucleo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `latitud` float DEFAULT NULL,
  `longitud` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `nucleo`
--

INSERT INTO `nucleo` (`id`, `nombre`, `direccion`, `telefono`, `latitud`, `longitud`) VALUES
(1, 'nucleo1', 'calle 123', '4654654654', NULL, NULL),
(2, 'nucleo2', 'calle 321', '8854654654', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

CREATE TABLE IF NOT EXISTS `permiso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=22 ;

--
-- Volcado de datos para la tabla `permiso`
--

INSERT INTO `permiso` (`id`, `nombre`) VALUES
(1, 'usuario_index'),
(2, 'usuario_new'),
(3, 'usuario_destroy'),
(4, 'usuario_update'),
(5, 'usuario_show'),
(6, 'configuracion_update'),
(7, 'docente_new'),
(8, 'docente_index'),
(9, 'docente_destroy'),
(10, 'docente_update'),
(11, 'docente_show'),
(12, 'estudiante_index'),
(13, 'estudiante_destroy'),
(14, 'estudiante_update'),
(15, 'estudiante_new'),
(16, 'estudiante_show'),
(17, 'administracion_new'),
(18, 'administracion_index'),
(19, 'administracion_show'),
(20, 'administracion_update'),
(21, 'administracion_destroy');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preceptor`
--

CREATE TABLE IF NOT EXISTS `preceptor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preceptor_nucleo`
--

CREATE TABLE IF NOT EXISTS `preceptor_nucleo` (
  `preceptor_id` int(11) NOT NULL,
  `nucleo_id` int(11) NOT NULL,
  PRIMARY KEY (`preceptor_id`,`nucleo_id`),
  KEY `FK_nucleo_id` (`nucleo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable`
--

CREATE TABLE IF NOT EXISTS `responsable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_genero_responsable_id` (`genero_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable_estudiante`
--

CREATE TABLE IF NOT EXISTS `responsable_estudiante` (
  `responsable_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  PRIMARY KEY (`responsable_id`,`estudiante_id`),
  KEY `FK_estudiante_id` (`estudiante_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE IF NOT EXISTS `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'administrador'),
(2, 'preceptor'),
(3, 'docente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE IF NOT EXISTS `rol_tiene_permiso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=25 ;

--
-- Volcado de datos para la tabla `rol_tiene_permiso`
--

INSERT INTO `rol_tiene_permiso` (`id`, `rol_id`, `permiso_id`) VALUES
(1, 1, 1),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 2),
(8, 1, 12),
(9, 1, 13),
(10, 1, 14),
(11, 1, 15),
(12, 1, 16),
(13, 1, 17),
(14, 1, 18),
(15, 1, 19),
(16, 1, 20),
(17, 1, 21),
(18, 1, 7),
(19, 1, 8),
(20, 1, 9),
(21, 1, 10),
(22, 1, 11),
(23, 3, 8),
(24, 3, 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE IF NOT EXISTS `taller` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre_corto` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `taller`
--

INSERT INTO `taller` (`id`, `nombre`, `nombre_corto`) VALUES
(1, 'taller guitarra', 'T_Guitarra'),
(2, 'taller violin', 'T_Violin'),
(3, 'taller_piano', 'T_Piano');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_instrumento`
--

CREATE TABLE IF NOT EXISTS `tipo_instrumento` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `tipo_instrumento`
--

INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES
(1, 'Cuerda'),
(2, 'Viento'),
(3, 'Percucion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=13 ;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `email`, `username`, `password`, `activo`, `updated_at`, `deleted_at`, `first_name`, `last_name`) VALUES
(1, 'root@root.com', 'root', 'pbkdf2:sha256:150000$I1H0Bio1$35490d74caa06f9a42f49bc537fb5b7cf28fda9b20969ad45ff40b8c27dd89e5', 1, '2019-10-22 00:31:22', NULL, 'root', 'root'),
(3, 'edicion25@mail.com', 'edicion25@mail.com', 'edicion25@mail.com', 1, '2019-10-26 19:09:23', NULL, 'edicion25@mail.com', 'edicion25@mail.com'),
(7, 'AgustinRoot@mail.com', 'juan', 'pbkdf2:sha256:150000$cXCoGSsB$23a147531a635e73ccc290f1946f78e8f1063f7f5030a5681c4eb84efce9bf61', 1, '2019-10-31 04:56:25', NULL, 'Agustin', 'Ramirez'),
(8, 'TomasRoot@mail.com', 'Tomas', 'pbkdf2:sha256:150000$YCw8l3AG$6ad4ba9d3f1c376b72eaeb1c69eecac505ac50ad111d1635f4c4d49dd1e175f5', 1, '2019-10-31 04:57:32', NULL, 'Tomas', 'Sandler'),
(9, 'JulianRoot@mail.com', 'Julian', 'pbkdf2:sha256:150000$cwYhgoxE$3931cfbeb7acfacb5f688fd998c285b392d4589b9132e0ad68affb874169d5fc', 1, '2019-10-31 04:58:09', NULL, 'Julian', 'Villega'),
(10, 'dgh@fb.com', 'Dg', 'fgh', 1, '2019-11-05 00:15:41', NULL, 'Dyy', 'Fgh'),
(11, 'pepe@gmail.com', 'pepe123', 'pbkdf2:sha256:150000$RqlVbzsp$abb48f8707382d6d3ccd7db3a3a954357093ca6150d0a45112262fc7e7ebcfc9', 0, '2019-11-11 03:06:14', NULL, 'pepe', 'pepep'),
(12, 'pepe@gmail.coma', 'pepe321', 'pbkdf2:sha256:150000$iXseDja0$39afc8ac2ca8402a8f5d9bfdbf4df2e29d660ada7b903a2c0dacfa5017d8e149', 1, '2019-11-20 19:28:32', NULL, 'pepe', 'popo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_tiene_rol`
--

CREATE TABLE IF NOT EXISTS `usuario_tiene_rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=14 ;

--
-- Volcado de datos para la tabla `usuario_tiene_rol`
--

INSERT INTO `usuario_tiene_rol` (`id`, `usuario_id`, `rol_id`) VALUES
(1, 1, 1),
(3, 5, 1),
(6, 9, 1),
(8, 7, 2),
(9, 11, 1),
(10, 11, 2),
(11, 11, 3),
(12, 10, 2),
(13, 8, 3);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencia_taller_ciclo_lectivo_dia`
--
ALTER TABLE `asistencia_taller_ciclo_lectivo_dia`
  ADD CONSTRAINT `asistencia_taller_ciclo_lectivo_dia_ibfk_1` FOREIGN KEY (`ciclo_lectivo_taller_horario`) REFERENCES `ciclo_lectivo_taller_horario` (`id`),
  ADD CONSTRAINT `asistencia_taller_ciclo_lectivo_dia_ibfk_2` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`);

--
-- Filtros para la tabla `ciclo_lectivo_taller`
--
ALTER TABLE `ciclo_lectivo_taller`
  ADD CONSTRAINT `FK_ciclo_lectivo_taller_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_ciclo_lectivo_taller_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `clase_taller_ciclo_lectivo`
--
ALTER TABLE `clase_taller_ciclo_lectivo`
  ADD CONSTRAINT `clase_taller_ciclo_lectivo_ibfk_1` FOREIGN KEY (`taller_ciclo_lectivo_id`) REFERENCES `ciclo_lectivo_taller` (`id`),
  ADD CONSTRAINT `clase_taller_ciclo_lectivo_ibfk_2` FOREIGN KEY (`dia_semana`) REFERENCES `dia_semana` (`id`);

--
-- Filtros para la tabla `docente`
--
ALTER TABLE `docente`
  ADD CONSTRAINT `FK_genero_docente_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`);

--
-- Filtros para la tabla `docente_responsable_taller`
--
ALTER TABLE `docente_responsable_taller`
  ADD CONSTRAINT `docente_responsable_taller_ibfk_1` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`),
  ADD CONSTRAINT `docente_responsable_taller_ibfk_2` FOREIGN KEY (`ciclo_lectivo_taller_id`) REFERENCES `ciclo_lectivo_taller` (`id`);

--
-- Filtros para la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `FK_barrio_id` FOREIGN KEY (`barrio_id`) REFERENCES `barrio` (`id`),
  ADD CONSTRAINT `FK_escuela_id` FOREIGN KEY (`escuela_id`) REFERENCES `escuela` (`id`),
  ADD CONSTRAINT `FK_genero_estudiante_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`),
  ADD CONSTRAINT `FK_nivel_id` FOREIGN KEY (`nivel_id`) REFERENCES `nivel` (`id`);

--
-- Filtros para la tabla `estudiante_ciclo_lectivo_taller`
--
ALTER TABLE `estudiante_ciclo_lectivo_taller`
  ADD CONSTRAINT `estudiante_ciclo_lectivo_taller_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `estudiante_ciclo_lectivo_taller_ibfk_2` FOREIGN KEY (`ciclo_lectivo_taller_id`) REFERENCES `ciclo_lectivo_taller` (`id`);

--
-- Filtros para la tabla `estudiante_taller`
--
ALTER TABLE `estudiante_taller`
  ADD CONSTRAINT `FK_estudiante_taller_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_estudiante_taller_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `FK_estudiante_taller_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `preceptor_nucleo`
--
ALTER TABLE `preceptor_nucleo`
  ADD CONSTRAINT `FK_nucleo_id` FOREIGN KEY (`nucleo_id`) REFERENCES `nucleo` (`id`),
  ADD CONSTRAINT `FK_preceptor_id` FOREIGN KEY (`preceptor_id`) REFERENCES `preceptor` (`id`);

--
-- Filtros para la tabla `responsable`
--
ALTER TABLE `responsable`
  ADD CONSTRAINT `FK_genero_responsable_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`);

--
-- Filtros para la tabla `responsable_estudiante`
--
ALTER TABLE `responsable_estudiante`
  ADD CONSTRAINT `FK_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `FK_responsable_id` FOREIGN KEY (`responsable_id`) REFERENCES `responsable` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
