Paso 1. Copiar el codigo SQL y ejecutar para poder crear la base de datos

Paso 2. Agregar el codigo de la informacion para poder llenar las tablas en la base de datos

Paso 3. Generar el entorno virtual (Si ya existe saltrar al siguiente)

Paso 4. Habilitar el entorno virtual

Paso 5. Instalar todas librerias necesarias para poder ejecutar el codigo

Paso 6. En la conexcion se debe de ajustar a los campos necesarios localmente del equipo

Paso 7. Usar el archivo Menu.py ya que con el se peude controlar tda la parte visual del programa 

===================================================================================================================================================

DATOS PRE HECHOS PARA LA BASE DE DATOS POR LAS TABALAS 

-- MEMBRESIA
INSERT INTO Membresia (idCodigo, Fecha_Activacion, Fecha_Vigencia, Tipo) VALUES
('MEM0000000001', '2024-01-01', '2025-01-01', 'Ejecutiva'),
('MEM0000000002', '2024-02-01', '2025-02-01', 'Dorada'),
('MEM0000000003', '2024-03-01', '2025-03-01', 'Ejecutiva'),
('MEM0000000004', '2024-04-01', '2025-04-01', 'Dorada'),
('MEM0000000005', '2024-05-01', '2025-05-01', 'Ejecutiva'),
('MEM0000000006', '2024-01-15', '2025-01-15', 'Dorada'),
('MEM0000000007', '2024-02-15', '2025-02-15', 'Ejecutiva'),
('MEM0000000008', '2024-03-15', '2025-03-15', 'Dorada'),
('MEM0000000009', '2024-04-15', '2025-04-15', 'Ejecutiva'),
('MEM0000000010', '2024-05-15', '2025-05-15', 'Dorada'),
('MEM0000000011', '2024-06-01', '2025-06-01', 'Ejecutiva'),
('MEM0000000012', '2024-06-15', '2025-06-15', 'Dorada'),
('MEM0000000013', '2024-07-01', '2025-07-01', 'Ejecutiva'),
('MEM0000000014', '2024-07-15', '2025-07-15', 'Dorada'),
('MEM0000000015', '2024-08-01', '2025-08-01', 'Ejecutiva'),
('GEN0000000000', '2000-01-01', '2099-12-31', 'Dorada');

-- CLIENTE 
INSERT INTO Cliente (idCliente, idCodigo, Nombre, Apellidos, Edad, Correo, Telefono, Direccion) VALUES
(1, 'MEM0000000001', 'Ana', 'Pérez López', 28, 'ana1@example.com', 5551234561, 'Av. Siempre Viva 123'),
(2, 'MEM0000000002', 'Luis', 'García Gómez', 35, 'luis2@example.com', 5551234562, 'Calle Falsa 456'),
(3, 'MEM0000000003', 'María', 'Rodríguez Díaz', 40, 'maria3@example.com', 5551234563, 'Reforma 789'),
(4, 'MEM0000000004', 'Carlos', 'Hernández Ruiz', 50, 'carlos4@example.com', 5551234564, 'Insurgentes 321'),
(5, 'MEM0000000005', 'Lucía', 'Martínez Vega', 22, 'lucia5@example.com', 5551234565, 'Av. Central 456'),
(6, 'MEM0000000006', 'José', 'López Hernández', 60, 'jose6@example.com', 5551234566, 'Monte Alban 987'),
(7, 'MEM0000000007', 'Laura', 'Ramírez Peña', 33, 'laura7@example.com', 5551234567, 'Col. Del Valle'),
(8, 'MEM0000000008', 'Miguel', 'Flores Silva', 27, 'miguel8@example.com', 5551234568, 'Santa Fe'),
(9, 'MEM0000000009', 'Claudia', 'Jiménez Ríos', 42, 'claudia9@example.com', 5551234569, 'Av. Universidad'),
(10, 'MEM0000000010', 'Ricardo', 'Ortega Márquez', 36, 'ricardo10@example.com', 5551234570, 'Calle 5 de Febrero'),
(11, 'MEM0000000011', 'Elena', 'Núñez Franco', 30, 'elena11@example.com', 5551234571, 'Lomas Verdes'),
(12, 'MEM0000000012', 'Fernando', 'Castro Molina', 45, 'fernando12@example.com', 5551234572, 'Av. Patriotismo'),
(13, 'MEM0000000013', 'Sara', 'Moreno Ramos', 38, 'sara13@example.com', 5551234573, 'Portales'),
(14, 'MEM0000000014', 'Jorge', 'Reyes Salinas', 41, 'jorge14@example.com', 5551234574, 'Narvarte'),
(15, 'MEM0000000015', 'Isabel', 'Soto Gálvez', 29, 'isabel15@example.com', 5551234575, 'Roma Norte'),
(16, 'GEN0000000000', 'CLIENTE', 'GENERAL', 0, 'ventas@tienda.com', 5550000000, 'CONSUMIDOR FINAL');

-- EMPLEADO 
INSERT INTO Empleado (idEmpleado, Nombre, Apellido, Edad, Puesto, Salario) VALUES
(1, 'Pedro', 'Hernández', 30, 'Cajero', 8000.00),
(2, 'Sandra', 'Gómez', 26, 'Reponedor', 7500.00),
(3, 'Hugo', 'Mendoza', 40, 'Gerente', 15000.00),
(4, 'Rosa', 'Nava', 35, 'Seguridad', 8500.00),
(5, 'David', 'Santos', 29, 'Supervisor', 12000.00),
(6, 'Martha', 'Zúñiga', 38, 'Cajero', 8100.00),
(7, 'Iván', 'Chávez', 27, 'Reponedor', 7700.00),
(8, 'Leticia', 'Miranda', 32, 'Cajero', 8000.00),
(9, 'Roberto', 'Pérez', 45, 'Gerente', 15500.00),
(10, 'Paola', 'Reyes', 28, 'Seguridad', 8600.00),
(11, 'César', 'Torres', 33, 'Supervisor', 12300.00),
(12, 'Norma', 'Vega', 31, 'Reponedor', 7400.00),
(13, 'Ángel', 'Ruiz', 34, 'Cajero', 8000.00),
(14, 'Gloria', 'Lozano', 36, 'Gerente', 15800.00),
(15, 'Julio', 'Morales', 29, 'Seguridad', 8700.00);

-- PROVEEDOR 
INSERT INTO Proveedor (idProveedor, Nombre, Apellidos, Telefono, Direccion) VALUES
(1, 'Distribuciones', 'Monarca S.A.', 5556789010, 'CDMX'),
(2, 'Proveedora', 'Del Norte', 5556789011, 'Guadalajara'),
(3, 'Central', 'Alimentos S.A.', 5556789012, 'Monterrey'),
(4, 'Productos', 'Selectos', 5556789013, 'Puebla'),
(5, 'Abastecedora', 'Tapatía', 5556789014, 'León'),
(6, 'Grupo', 'Villita', 5556789015, 'Querétaro'),
(7, 'La', 'Bodega', 5556789016, 'Toluca'),
(8, 'Mega', 'Suministros', 5556789017, 'Cancún'),
(9, 'Industrial', 'Maya', 5556789018, 'Mérida'),
(10, 'El', 'Proveeduría', 5556789019, 'Tijuana'),
(11, 'Zacatecas', 'Distribuciones', 5556789020, 'Zacatecas'),
(12, 'Sur', 'Central', 5556789021, 'Oaxaca'),
(13, 'GDL', 'Comercial', 5556789022, 'Guadalajara'),
(14, 'Bajío', 'Alimentos', 5556789023, 'León'),
(15, 'Delicias', 'S.A.', 5556789024, 'Chihuahua');

-- CATEGORIA
INSERT INTO categoria (idCategoria, Nombre) VALUES 
(1, 'Abarrotes'),
(2, 'Aceites y grasas'),
(3, 'Papelería y limpieza'),
(4, 'Detergentes y limpieza'),
(5, 'Cuidado personal'),
(6, 'Lácteos'),
(7, 'Panadería'),
(8, 'Alimentos instantáneos'),
(9, 'Bebidas'),
(10, 'Carnes frías'),
(11, 'Congelados'),
(12, 'Botanas'),
(13, 'Electrodomésticos'),
(14, 'Higiene personal'),
(15, 'Mascotas');

-- ARTICULOS
INSERT INTO articulo (idCodigo_Barra, idCategoria, Nombre, Precio, Existencia, Marca, Caracteristicas) VALUES
('7501000123457', 1, 'Arroz', 27.50, 100, 'La Merced', 'Grano largo, extra limpio'),
('7501000123464', 1, 'Frijol Negro', 29.00, 80, 'La Sierra', 'Frijol de grano entero'),
('7501000123471', 2, 'Aceite vegetal', 45.00, 60, 'Nutrioli', 'Aceite 100% vegetal'),
('7501000123488', 3, 'Papel Higiénico', 35.00, 200, 'Regio', 'Suavidad y resistencia'),
('7501000123495', 4, 'Detergente en polvo', 48.90, 90, 'Ariel', 'Rinde más por carga'),
('7501000123501', 1, 'Azúcar', 25.00, 120, 'Zulka', 'Azúcar estándar'),
('7501000123518', 5, 'Shampoo', 56.00, 70, 'Head & Shoulders', 'Control de caspa'),
('7501000123525', 6, 'Leche entera', 22.00, 150, 'Lala', 'Fortificada con vitaminas A y D'),
('7501000123532', 7, 'Pan de caja', 38.00, 100, 'Bimbo', 'Pan blanco suave'),
('7501000123549', 8, 'Sopa instantánea', 14.00, 300, 'Maruchan', 'Sabor camarón picante'),
('7501000123556', 9, 'Refresco Cola 2L', 18.00, 250, 'Coca-Cola', 'Botella retornable'),
('7501000123570', 10, 'Jamón de pierna', 85.00, 50, 'Fud', '250g, bajo en grasa'),
('7501000123587', 11, 'Pizza congelada', 79.00, 40, 'Nestlé', 'Pizza pepperoni'),
('7501000123594', 12, 'Papas fritas', 29.00, 200, 'Sabritas', 'Sabor original'),
('7501000123600', 13, 'Licuadora 600W', 599.00, 20, 'Oster', 'Vidrio resistente'),
('7501000123617', 14, 'Cereal Integral', 599.00, 30, 'Kellogg\'s', 'Alto en fibra y vitaminas');


-- PEDIDO
INSERT INTO Pedido (idPedido, idProveedor, Fecha_Pedido, Fecha_Entrega, Importe, Pago, Cambio, Estado) VALUES
(1, 1, '2025-05-01', '2025-05-05', 1000.00, 1000.00, 0.00, 'Entregado'),
(2, 1, '2025-05-02', '2025-05-06', 1200.00, 1300.00, 100.00, 'Entregado'),
(3, 2, '2025-05-03', '2025-05-07', 1500.00, 1500.00, 0.00, 'Entregado'),
(4, 2, '2025-05-04', '2025-05-08', 1750.00, 1800.00, 50.00, 'Enviado'),
(5, 3, '2025-05-05', '2025-05-10', 950.00, 1000.00, 50.00, 'Preparando'),
(6, 1, '2025-05-06', '2025-05-11', 2000.00, 2000.00, 0.00, 'Entregado'),
(7, 2, '2025-05-07', '2025-05-12', 2200.00, 2200.00, 0.00, 'Enviado'),
(8, 3, '2025-05-08', '2025-05-13', 1250.00, 1300.00, 50.00, 'Preparando'),
(9, 1, '2025-05-09', '2025-05-14', 1600.00, 1600.00, 0.00, 'Entregado'),
(10, 2, '2025-05-10', '2025-05-15', 1950.00, 2000.00, 50.00, 'Enviado'),
(11, 3, '2025-05-11', '2025-05-16', 1450.00, 1500.00, 50.00, 'Entregado'),
(12, 1, '2025-05-12', '2025-05-17', 1100.00, 1100.00, 0.00, 'Preparando'),
(13, 2, '2025-05-13', '2025-05-18', 1300.00, 1350.00, 50.00, 'Entregado'),
(14, 3, '2025-05-14', '2025-05-19', 900.00, 900.00, 0.00, 'Enviado'),
(15, 1, '2025-05-15', '2025-05-20', 1700.00, 1750.00, 50.00, 'Entregado');

-- DETALLE_PEDIDO
INSERT INTO Detalle_Pedido (idCodigo_Barra, idPedido, Cantidad, Subtotal, Precio_Unitario) VALUES
('7501000123457', 1, 50, 1375.00, 27.50),
('7501000123464', 2, 40, 1160.00, 29.00),
('7501000123471', 3, 30, 1350.00, 45.00),
('7501000123488', 4, 20, 700.00, 35.00),
('7501000123501', 5, 80, 2000.00, 25.00),
('7501000123518', 6, 60, 3360.00, 56.00),
('7501000123525', 7, 90, 1980.00, 22.00),
('7501000123532', 8, 70, 2660.00, 38.00),
('7501000123549', 9, 120, 1680.00, 14.00),
('7501000123556', 10, 100, 1800.00, 18.00),
('7501000123570', 11, 50, 4250.00, 85.00),
('7501000123587', 12, 25, 1975.00, 79.00),
('7501000123594', 13, 70, 2030.00, 29.00),
('7501000123600', 14, 60, 1320.00, 22.00),
('7501000123617', 15, 10, 5990.00, 599.00);


-- VENTA
INSERT INTO Venta (idVenta, idCliente, idCodigo, idEmpleado, Importe, Pago, Cambio, Fecha_Hora) VALUES
(1, 1, 'MEM0000000001', 1, 100.00, 120.00, 20.00, '2025-05-10'),
(2, 2, 'MEM0000000002', 2, 150.00, 200.00, 50.00, '2025-05-11'),
(3, 3, 'MEM0000000003', 3, 250.00, 300.00, 50.00, '2025-05-12'),
(4, 1, 'MEM0000000001', 2, 90.00, 100.00, 10.00, '2025-05-13'),
(5, 2, 'MEM0000000002', 1, 75.00, 100.00, 25.00, '2025-05-14'),
(6, 3, 'MEM0000000003', 3, 112.00, 120.00, 8.00, '2025-05-15'),
(7, 1, 'MEM0000000001', 1, 66.00, 70.00, 4.00, '2025-05-16'),
(8, 2, 'MEM0000000002', 2, 114.00, 120.00, 6.00, '2025-05-17'),
(9, 3, 'MEM0000000003', 3, 42.00, 50.00, 8.00, '2025-05-18'),
(10, 1, 'MEM0000000001', 1, 54.00, 60.00, 6.00, '2025-05-19'),
(11, 2, 'MEM0000000002', 2, 170.00, 200.00, 30.00, '2025-05-20'),
(12, 3, 'MEM0000000003', 3, 158.00, 160.00, 2.00, '2025-05-21'),
(13, 1, 'MEM0000000001', 1, 58.00, 60.00, 2.00, '2025-05-22'),
(14, 2, 'MEM0000000002', 2, 66.00, 70.00, 4.00, '2025-05-23'),
(15, 3, 'MEM0000000003', 3, 599.00, 600.00, 1.00, '2025-05-24');

-- DETALLES_VENTA
INSERT INTO Detalles_Venta (idVenta, idCodigo_Barra, Cantidad, Subtotal, Precio_Unitario) VALUES
(1, '7501000123457', 2, 55.00, 27.50),
(2, '7501000123464', 2, 58.00, 29.00),
(3, '7501000123471', 3, 135.00, 45.00),
(4, '7501000123488', 1, 35.00, 35.00),
(5, '7501000123501', 3, 75.00, 25.00),
(6, '7501000123518', 2, 112.00, 56.00),
(7, '7501000123525', 3, 66.00, 22.00),
(8, '7501000123532', 3, 114.00, 38.00),
(9, '7501000123549', 3, 42.00, 14.00),
(10, '7501000123556', 3, 54.00, 18.00),
(11, '7501000123570', 2, 170.00, 85.00),
(12, '7501000123587', 2, 158.00, 79.00),
(13, '7501000123594', 2, 58.00, 29.00),
(14, '7501000123600', 3, 66.00, 22.00),
(15, '7501000123617', 1, 599.00, 599.00);