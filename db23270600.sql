-- MySQL Workbench Forward Engineering

-- Eliminar y recrear la base de datos COSTCO
DROP DATABASE IF EXISTS `COSTCO`;
CREATE SCHEMA IF NOT EXISTS `COSTCO` DEFAULT CHARACTER SET utf8;
USE `COSTCO`;

-- Desactivar temporalmente las restricciones
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Tabla Membresia
CREATE TABLE `Membresia` (
  `idCodigo` CHAR(13) NOT NULL,
  `Fecha_Activacion` DATE NOT NULL,
  `Fecha_Vigencia` DATE NOT NULL,
  `Tipo` ENUM('Ejecutiva', 'Dorada') NOT NULL,
  PRIMARY KEY (`idCodigo`)
) ENGINE = InnoDB;

-- Tabla Cliente
CREATE TABLE `Cliente` (
  `idCliente` INT NOT NULL AUTO_INCREMENT,
  `idCodigo` CHAR(13) NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellidos` VARCHAR(100),
  `Edad` INT,
  `Correo` VARCHAR(100) NOT NULL,
  `Telefono` VARCHAR(15) NOT NULL,
  `Direccion` TEXT,
  PRIMARY KEY (`idCliente`, `idCodigo`),
  INDEX `Membresia_idx` (`idCodigo`),
  CONSTRAINT `FK_Cliente_Membresia`
    FOREIGN KEY (`idCodigo`)
    REFERENCES `Membresia` (`idCodigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Empleado
CREATE TABLE `Empleado` (
  `idEmpleado` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellido` VARCHAR(100),
  `Edad` INT,
  `Puesto` VARCHAR(45) NOT NULL,
  `Salario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idEmpleado`)
) ENGINE = InnoDB;

-- Tabla Venta
CREATE TABLE `Venta` (
  `idVenta` INT NOT NULL AUTO_INCREMENT,
  `idCliente` INT NOT NULL,
  `idCodigo` CHAR(13) NOT NULL,
  `idEmpleado` INT NOT NULL,
  `Total` DECIMAL(10,2) NOT NULL,
  `Fecha_Hora` DATETIME,
  PRIMARY KEY (`idVenta`),
  INDEX `Cliente1_idx` (`idCliente`, `idCodigo`),
  INDEX `Empleado1_idx` (`idEmpleado`),
  CONSTRAINT `FK_Venta_Cliente`
    FOREIGN KEY (`idCliente`, `idCodigo`)
    REFERENCES `Cliente` (`idCliente`, `idCodigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Venta_Empleado`
    FOREIGN KEY (`idEmpleado`)
    REFERENCES `Empleado` (`idEmpleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Categoria
CREATE TABLE `Categoria` (
  `idCategoria` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`idCategoria`)
) ENGINE = InnoDB;

-- Tabla Articulo
CREATE TABLE `Articulo` (
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `idCategoria` INT NOT NULL,
  `Nombre` VARCHAR(150) NOT NULL,
  `Precio` DECIMAL(10,2) NOT NULL,
  `Existencia` VARCHAR(45) NOT NULL,
  `Marca` VARCHAR(45) NOT NULL,
  `Caracteristicas` TEXT,
  PRIMARY KEY (`idCodigo_Barra`),
  INDEX `Categoria1_idx` (`idCategoria`),
  CONSTRAINT `FK_Articulo_Categoria`
    FOREIGN KEY (`idCategoria`)
    REFERENCES `Categoria` (`idCategoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Historial_Precio
CREATE TABLE `Historial_Precio` (
  `idHistorial_Precio` INT NOT NULL AUTO_INCREMENT,
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `Precio_Anterior` DECIMAL(10,2) NOT NULL,
  `Precio_Nuevo` DECIMAL(10,2) NOT NULL,
  `Fecha_Cambio` DATETIME,
  PRIMARY KEY (`idHistorial_Precio`),
  INDEX `Articulo3_idx` (`idCodigo_Barra`),
  CONSTRAINT `FK_Historial_Articulo`
    FOREIGN KEY (`idCodigo_Barra`)
    REFERENCES `Articulo` (`idCodigo_Barra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Proveedor
CREATE TABLE `Proveedor` (
  `idProveedor` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellidos` VARCHAR(100),
  `Telefono` VARCHAR(15) NOT NULL,
  `Direccion` TEXT,
  PRIMARY KEY (`idProveedor`)
) ENGINE = InnoDB;

-- Tabla Pedido
CREATE TABLE `Pedido` (
  `idPedido` INT NOT NULL AUTO_INCREMENT,
  `idProveedor` INT NOT NULL,
  `Fecha_Pedido` DATETIME NOT NULL,
  `Fecha_Entrega` DATETIME NOT NULL,
  `Estado` ENUM('Preparando', 'Enviado', 'Entregado'),
  PRIMARY KEY (`idPedido`),
  INDEX `Proveedor1_idx` (`idProveedor`),
  CONSTRAINT `FK_Pedido_Proveedor`
    FOREIGN KEY (`idProveedor`)
    REFERENCES `Proveedor` (`idProveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Detalles_Venta
CREATE TABLE `Detalles_Venta` (
  `idVenta` INT NOT NULL,
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `Cantidad` INT NOT NULL,
  `Importe` DECIMAL(10,2) NOT NULL,
  `Precio_Unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idVenta`, `idCodigo_Barra`),
  INDEX `Articulo1_idx` (`idCodigo_Barra`),
  INDEX `Venta1_idx` (`idVenta`),
  CONSTRAINT `FK_Detalles_Venta_Venta`
    FOREIGN KEY (`idVenta`)
    REFERENCES `Venta` (`idVenta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Detalles_Venta_Articulo`
    FOREIGN KEY (`idCodigo_Barra`)
    REFERENCES `Articulo` (`idCodigo_Barra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Tabla Detalle_Pedido
CREATE TABLE `Detalle_Pedido` (
  `idCodigo_Barra` CHAR(13) NOT NULL,
  `idPedido` INT NOT NULL,
  `Cantidad` INT NOT NULL,
  `Importe` DECIMAL(10,2) NOT NULL,
  `Precio_Unitario` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`idCodigo_Barra`, `idPedido`),
  INDEX `Pedido1_idx` (`idPedido`),
  INDEX `Articulo2_idx` (`idCodigo_Barra`),
  CONSTRAINT `FK_Detalle_Pedido_Articulo`
    FOREIGN KEY (`idCodigo_Barra`)
    REFERENCES `Articulo` (`idCodigo_Barra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Detalle_Pedido_Pedido`
    FOREIGN KEY (`idPedido`)
    REFERENCES `Pedido` (`idPedido`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;

-- Restaurar configuraciones
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;