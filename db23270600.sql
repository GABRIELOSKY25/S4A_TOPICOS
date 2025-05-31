-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema COSTCO
-- -----------------------------------------------------
DROP DATABASE IF EXISTS `COSTCO`;
CREATE SCHEMA IF NOT EXISTS `COSTCO` DEFAULT CHARACTER SET utf8 ;
USE `COSTCO`;

-- Membresia
CREATE TABLE `Membresia` (
  `idCodigo` CHAR(13) NOT NULL,
  `Fecha_Activacion` DATE NOT NULL,
  `Fecha_Vigencia` DATE NOT NULL,
  `Tipo` ENUM('Ejecutiva', 'Dorada') NOT NULL,
  PRIMARY KEY (`idCodigo`)
) ENGINE=InnoDB;

-- Cliente
CREATE TABLE `Cliente` (
  `idCliente` INT NOT NULL,
  `idCodigo` CHAR(13) NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellidos` VARCHAR(100),
  `Edad` INT(3),
  `Correo` VARCHAR(100) NOT NULL,
  `Telefono` BIGINT NOT NULL,
  `Direccion` TEXT,
  PRIMARY KEY (`idCliente`, `idCodigo`),
  FOREIGN KEY (`idCodigo`) REFERENCES `Membresia` (`idCodigo`)
) ENGINE=InnoDB;

-- Empleado
CREATE TABLE `Empleado` (
  `idEmpleado` INT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellido` VARCHAR(100),
  `Edad` INT(3),
  `Puesto` VARCHAR(45) NOT NULL,
  `Salario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idEmpleado`)
) ENGINE=InnoDB;

-- Categoria
CREATE TABLE `Categoria` (
  `idCategoria` INT NOT NULL,
  `Nombre` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`idCategoria`)
) ENGINE=InnoDB;

-- Articulo
CREATE TABLE `Articulo` (
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `idCategoria` INT NOT NULL,
  `Nombre` VARCHAR(150) NOT NULL,
  `Precio` DECIMAL(10,2) NOT NULL,
  `Existencia` VARCHAR(45) NOT NULL,
  `Marca` VARCHAR(45) NOT NULL,
  `Caracteristicas` TEXT,
  PRIMARY KEY (`idCodigo_Barra`),
  FOREIGN KEY (`idCategoria`) REFERENCES `Categoria` (`idCategoria`)
) ENGINE=InnoDB;

-- Historial_Precio
CREATE TABLE `Historial_Precio` (
  `idHistorial_Precio` INT NOT NULL,
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `Precio_Anterior` DECIMAL(10,2) NOT NULL,
  `Precio_Nuevo` DECIMAL(10,2) NOT NULL,
  `Fecha_Cambio` DATETIME,
  PRIMARY KEY (`idHistorial_Precio`),
  FOREIGN KEY (`idCodigo_Barra`) REFERENCES `Articulo` (`idCodigo_Barra`)
) ENGINE=InnoDB;

-- Proveedor
CREATE TABLE `Proveedor` (
  `idProveedor` INT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellidos` VARCHAR(100),
  `Telefono` BIGINT NOT NULL,
  `Direccion` TEXT,
  PRIMARY KEY (`idProveedor`)
) ENGINE=InnoDB;

-- Pedido
CREATE TABLE `Pedido` (
  `idPedido` INT NOT NULL,
  `idProveedor` INT NOT NULL,
  `Fecha_Pedido` DATETIME NOT NULL,
  `Fecha_Entrega` DATETIME NOT NULL,
  `Importe` DECIMAL(10,2) NOT NULL,
  `Pago` DECIMAL(10,2) NOT NULL,
  `Cambio` DECIMAL(10,2) NOT NULL,
  `Estado` ENUM('Preparando', 'Enviado', 'Entregado'),
  PRIMARY KEY (`idPedido`),
  FOREIGN KEY (`idProveedor`) REFERENCES `Proveedor` (`idProveedor`)
) ENGINE=InnoDB;

-- Detalle_Pedido
CREATE TABLE `Detalle_Pedido` (
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `idPedido` INT NOT NULL,
  `Cantidad` INT NOT NULL,
  `Subtotal` DECIMAL(10,2) NOT NULL,
  `Precio_Unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idCodigo_Barra`, `idPedido`),
  FOREIGN KEY (`idCodigo_Barra`) REFERENCES `Articulo` (`idCodigo_Barra`),
  FOREIGN KEY (`idPedido`) REFERENCES `Pedido` (`idPedido`)
) ENGINE=InnoDB;

-- Venta
CREATE TABLE `Venta` (
  `idVenta` INT NOT NULL,
  `idCliente` INT NOT NULL,
  `idCodigo` CHAR(13) NOT NULL,
  `idEmpleado` INT NOT NULL,
  `Importe` DECIMAL(10,2) NOT NULL,
  `Pago` DECIMAL(10,2) NOT NULL,
  `Cambio` DECIMAL(10,2) NOT NULL,
  `Fecha_Hora` DATE,
  PRIMARY KEY (`idVenta`),
  FOREIGN KEY (`idCliente`, `idCodigo`) REFERENCES `Cliente` (`idCliente`, `idCodigo`),
  FOREIGN KEY (`idEmpleado`) REFERENCES `Empleado` (`idEmpleado`)
) ENGINE=InnoDB;

-- Detalles_Venta
CREATE TABLE `Detalles_Venta` (
  `idVenta` INT NOT NULL,
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `Cantidad` INT NOT NULL,
  `Subtotal` DECIMAL(10,2) NOT NULL,
  `Precio_Unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idVenta`, `idCodigo_Barra`),
  FOREIGN KEY (`idVenta`) REFERENCES `Venta` (`idVenta`),
  FOREIGN KEY (`idCodigo_Barra`) REFERENCES `Articulo` (`idCodigo_Barra`)
) ENGINE=InnoDB;

-- Restaurar configuración anterior
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;