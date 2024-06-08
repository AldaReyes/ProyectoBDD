--	creación tablas

CREATE TABLE accesoEmpleados
(
	accesoID serial PRIMARY KEY,
	fechaAcceso date,
	empleadoID int
);

CREATE TABLE almacenes
(
	almacenID serial PRIMARY KEY,
	nombre varchar(50),
	sucursalID int,
	direccionID int
);

CREATE TABLE cambioPrecios
(
	cambioPrecioID serial PRIMARY KEY,
	precioAnterior decimal(10,2),
	precioNuevo decimal(10,2),
	fechaCambio date,
	productoID int
);

CREATE TABLE clientes
(
	clienteID serial PRIMARY KEY,
	personaID int
);

CREATE TABLE direcciones
(
	direccionID serial PRIMARY KEY,
	calle varchar(100),
	ciudad varchar(50),
	estado varchar(50),
	pais varchar(50),
	codigoPostal char(5)
);

CREATE TABLE empleados
(
	empleadoID serial PRIMARY KEY,
	personaID int
);

CREATE TABLE gastos
(
	gastoID serial PRIMARY KEY,
	monto decimal(10,2),
	fechaGasto date,
	sucursalID int,
	proveedorID int
);

CREATE TABLE inventarioAlmacenes
(
	inventarioID serial PRIMARY KEY,
	cantidad int,
	almacenID int,
	productoID int
);

CREATE TABLE inventarioSucursales
(
	inventarioID serial PRIMARY KEY,
	cantidad int,
	sucursalID int,
	productoID int
);

CREATE TABLE personas
(
	personaID serial PRIMARY KEY,
	nombre varchar(50),
	apellidoM varchar(50),
	apellidoP varchar(50),
	fechaNacimiento date,
	edad int,
	direccionID int
);

CREATE TABLE productos
(
	productoID serial PRIMARY KEY,
	nombre varchar(50),
	cantidad int,
	precio decimal(10,2),
	codigo varchar(50),
	fechaCaducidad date
);

CREATE TABLE productosVendidos
(
	ventaID int,
	productoID int,
	cantidad int,
	precioUnitario int,
	PRIMARY KEY (VentaID, ProductoID)
);

CREATE TABLE proveedores
(
	proveedorID serial PRIMARY KEY,
	personaID int
);

CREATE TABLE registroClientes
(
	registroClienteID serial PRIMARY KEY,
	cantidadCompra int,
	fechaUltimaCompra date,
	clienteID int,
	productoID int
);

CREATE TABLE sucursales
(
	sucursalID serial PRIMARY KEY,
	nombre varchar(50),
	direccionID int
);

CREATE TABLE ticketCompras
(
	ticketID serial PRIMARY KEY,
	detalles varchar(250),
	fechaCompra date,
	proveedorID int
);

CREATE TABLE ventas
(
	ventaID serial PRIMARY KEY,
	fechaVenta date,
	sucursalID int,
	clienteID int
);

--	ADD FOREIGN KEY

ALTER TABLE accesoEmpleados ADD FOREIGN KEY (empleadoID)
REFERENCES empleados (empleadoID);

ALTER TABLE almacenes ADD FOREIGN KEY (direccionID)
REFERENCES direcciones (direccionID);

ALTER TABLE almacenes ADD FOREIGN KEY (sucursalID)
REFERENCES sucursales (sucursalID);

ALTER TABLE cambioPrecios ADD FOREIGN KEY (productoID)
REFERENCES productos (productoID);

ALTER TABLE clientes ADD FOREIGN KEY (personaID)
REFERENCES personas (personaID);

ALTER TABLE empleados ADD FOREIGN KEY (personaID)
REFERENCES personas (personaID);

ALTER TABLE gastos ADD FOREIGN KEY (sucursalID)
REFERENCES sucursales (sucursalID);

ALTER TABLE gastos ADD FOREIGN KEY (proveedorID)
REFERENCES proveedores (proveedorID);

ALTER TABLE inventarioAlmacenes ADD FOREIGN KEY (almacenID)
REFERENCES almacenes (almacenID);

ALTER TABLE inventarioAlmacenes ADD FOREIGN KEY (productoID)
REFERENCES productos (productoID);

ALTER TABLE inventarioSucursales ADD FOREIGN KEY (sucursalID)
REFERENCES sucursales (sucursalID);

ALTER TABLE inventarioSucursales ADD FOREIGN KEY (productoID)
REFERENCES productos (productoID);

ALTER TABLE personas ADD FOREIGN KEY (direccionID)
REFERENCES direcciones (direccionID);

ALTER TABLE productosVendidos ADD FOREIGN KEY (productoID)
REFERENCES productos (productoID);

ALTER TABLE productosVendidos ADD FOREIGN KEY (ventaID)
REFERENCES ventas (ventaID);

ALTER TABLE proveedores ADD FOREIGN KEY (personaID)
REFERENCES personas (personaID);

ALTER TABLE registroClientes ADD FOREIGN KEY (clienteID)
REFERENCES clientes (clienteID);

ALTER TABLE registroClientes ADD FOREIGN KEY (productoID)
REFERENCES productos (productoID);

ALTER TABLE sucursales ADD FOREIGN KEY (direccionID)
REFERENCES direcciones (direccionID);

ALTER TABLE ticketCompras ADD FOREIGN KEY (proveedorID)
REFERENCES proveedores (proveedorID);

ALTER TABLE ventas ADD FOREIGN KEY (sucursalID)
REFERENCES sucursales (sucursalID);

ALTER TABLE ventas ADD FOREIGN KEY (clienteID)
REFERENCES clientes (clienteID);

-- Inserciones para la tabla direcciones
INSERT INTO direcciones (calle, ciudad, estado, pais, codigoPostal) VALUES
('Calle 1', 'Ciudad A', 'Estado A', 'Pais A', '12345'),
('Calle 2', 'Ciudad B', 'Estado B', 'Pais A', '12346'),
('Calle 3', 'Ciudad C', 'Estado C', 'Pais A', '12347'),
('Calle 4', 'Ciudad D', 'Estado D', 'Pais A', '12348'),
('Calle 5', 'Ciudad E', 'Estado E', 'Pais A', '12349'),
('Calle 6', 'Ciudad F', 'Estado F', 'Pais A', '12350'),
('Calle 7', 'Ciudad G', 'Estado G', 'Pais A', '12351'),
('Calle 8', 'Ciudad H', 'Estado H', 'Pais A', '12352'),
('Calle 9', 'Ciudad I', 'Estado I', 'Pais A', '12353'),
('Calle 10', 'Ciudad J', 'Estado J', 'Pais A', '12354');

-- Inserciones para la tabla personas
INSERT INTO personas (nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID) VALUES
('Juan', 'Perez', 'Gomez', '1980-01-01', 44, 1),
('Maria', 'Lopez', 'Diaz', '1985-02-02', 39, 2),
('Pedro', 'Martinez', 'Sanchez', '1990-03-03', 34, 3),
('Ana', 'Garcia', 'Hernandez', '1995-04-04', 29, 4),
('Luis', 'Rodriguez', 'Jimenez', '2000-05-05', 24, 5),
('Laura', 'Fernandez', 'Ruiz', '1975-06-06', 49, 6),
('Carlos', 'Gomez', 'Mendez', '1988-07-07', 35, 7),
('Carmen', 'Diaz', 'Castro', '1983-08-08', 40, 8),
('Jose', 'Hernandez', 'Morales', '1970-09-09', 53, 9),
('Marta', 'Ruiz', 'Ortega', '1965-10-10', 58, 10);

-- Inserciones para la tabla empleados
INSERT INTO empleados (personaID) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserciones para la tabla clientes
INSERT INTO clientes (personaID) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserciones para la tabla proveedores
INSERT INTO proveedores (personaID) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10);

-- Inserciones para la tabla sucursales
INSERT INTO sucursales (nombre, direccionID) VALUES
('Sucursal A', 1),
('Sucursal B', 2),
('Sucursal C', 3),
('Sucursal D', 4),
('Sucursal E', 5),
('Sucursal F', 6),
('Sucursal G', 7),
('Sucursal H', 8),
('Sucursal I', 9),
('Sucursal J', 10);

-- Inserciones para la tabla productos
INSERT INTO productos (nombre, cantidad, precio, codigo, fechaCaducidad) VALUES
('Producto 1', 100, 10.00, 'P001', '2025-01-01'),
('Producto 2', 200, 20.00, 'P002', '2025-02-02'),
('Producto 3', 300, 30.00, 'P003', '2025-03-03'),
('Producto 4', 400, 40.00, 'P004', '2025-04-04'),
('Producto 5', 500, 50.00, 'P005', '2025-05-05'),
('Producto 6', 600, 60.00, 'P006', '2025-06-06'),
('Producto 7', 700, 70.00, 'P007', '2025-07-07'),
('Producto 8', 800, 80.00, 'P008', '2025-08-08'),
('Producto 9', 900, 90.00, 'P009', '2025-09-09'),
('Producto 10', 1000, 100.00, 'P010', '2025-10-10');

-- Inserciones para la tabla almacenes
INSERT INTO almacenes (nombre, sucursalID, direccionID) VALUES
('Almacen A', 1, 1),
('Almacen B', 2, 2),
('Almacen C', 3, 3),
('Almacen D', 4, 4),
('Almacen E', 5, 5),
('Almacen F', 6, 6),
('Almacen G', 7, 7),
('Almacen H', 8, 8),
('Almacen I', 9, 9),
('Almacen J', 10, 10);

-- Inserciones para la tabla accesoEmpleados
INSERT INTO accesoEmpleados (fechaAcceso, empleadoID) VALUES
('2023-01-01', 1),
('2023-01-02', 2),
('2023-01-03', 3),
('2023-01-04', 4),
('2023-01-05', 5),
('2023-01-06', 6),
('2023-01-07', 7),
('2023-01-08', 8),
('2023-01-09', 9),
('2023-01-10', 10);

-- Inserciones para la tabla cambioPrecios
INSERT INTO cambioPrecios (precioAnterior, precioNuevo, fechaCambio, productoID) VALUES
(10.00, 15.00, '2024-01-01', 1),
(20.00, 25.00, '2024-01-02', 2),
(30.00, 35.00, '2024-01-03', 3),
(40.00, 45.00, '2024-01-04', 4),
(50.00, 55.00, '2024-01-05', 5),
(60.00, 65.00, '2024-01-06', 6),
(70.00, 75.00, '2024-01-07', 7),
(80.00, 85.00, '2024-01-08', 8),
(90.00, 95.00, '2024-01-09', 9),
(100.00, 105.00, '2024-01-10', 10);

-- Inserciones para la tabla gastos
INSERT INTO gastos (monto, fechaGasto, sucursalID, proveedorID) VALUES
(1000.00, '2023-01-01', 1, 1),
(2000.00, '2023-01-02', 2, 2),
(3000.00, '2023-01-03', 3, 3),
(4000.00, '2023-01-04', 4, 4),
(5000.00, '2023-01-05', 5, 5),
(6000.00, '2023-01-06', 6, 6),
(7000.00, '2023-01-07', 7, 7),
(8000.00, '2023-01-08', 8, 8),
(9000.00, '2023-01-09', 9, 9),
(10000.00, '2023-01-10', 10, 10);

-- Inserciones para la tabla inventarioAlmacenes
INSERT INTO inventarioAlmacenes (cantidad, almacenID, productoID) VALUES
(100, 1, 1),
(200, 2, 2),
(300, 3, 3),
(400, 4, 4),
(500, 5, 5),
(600, 6, 6),
(700, 7, 7),
(800, 8, 8),
(900, 9, 9),
(1000, 10, 10);

-- Inserciones para la tabla inventarioSucursales
INSERT INTO inventarioSucursales (cantidad, sucursalID, productoID) VALUES
(100, 1, 1),
(200, 2, 2),
(300, 3, 3),
(400, 4, 4),
(500, 5, 5),
(600, 6, 6),
(700, 7, 7),
(800, 8, 8),
(900, 9, 9),
(1000, 10, 10);

-- Inserciones para la tabla ventas
INSERT INTO ventas (fechaVenta, sucursalID, clienteID) VALUES
('2023-01-01', 1, 1),
('2023-01-02', 2, 2),
('2023-01-03', 3, 3),
('2023-01-04', 4, 4),
('2023-01-05', 5, 5),
('2023-01-06', 6, 6),
('2023-01-07', 7, 7),
('2023-01-08', 8, 8),
('2023-01-09', 9, 9),
('2023-01-10', 10, 10);

-- Inserciones para la tabla productosVendidos
INSERT INTO productosVendidos (ventaID, productoID, cantidad, precioUnitario) VALUES
(1, 1, 10, 15),
(2, 2, 20, 25),
(3, 3, 30, 35),
(4, 4, 40, 45),
(5, 5, 50, 55),
(6, 6, 60, 65),
(7, 7, 70, 75),
(8, 8, 80, 85),
(9, 9, 90, 95),
(10, 10, 100, 105);

-- Inserciones para la tabla registroClientes
INSERT INTO registroClientes (cantidadCompra, fechaUltimaCompra, clienteID, productoID) VALUES
(1, '2023-01-01', 1, 1),
(2, '2023-01-02', 2, 2),
(3, '2023-01-03', 3, 3),
(4, '2023-01-04', 4, 4),
(5, '2023-01-05', 5, 5),
(6, '2023-01-06', 6, 6),
(7, '2023-01-07', 7, 7),
(8, '2023-01-08', 8, 8),
(9, '2023-01-09', 9, 9),
(10, '2023-01-10', 10, 10);

-- Inserciones para la tabla ticketCompras
INSERT INTO ticketCompras (detalles, fechaCompra, proveedorID) VALUES
('Compra 1', '2023-01-01', 1),
('Compra 2', '2023-01-02', 2),
('Compra 3', '2023-01-03', 3),
('Compra 4', '2023-01-04', 4),
('Compra 5', '2023-01-05', 5),
('Compra 6', '2023-01-06', 6),
('Compra 7', '2023-01-07', 7),
('Compra 8', '2023-01-08', 8),
('Compra 9', '2023-01-09', 9),
('Compra 10', '2023-01-10', 10);

CREATE OR REPLACE FUNCTION calcular_edad(fechaNacimiento DATE) RETURNS INT AS $$
DECLARE
    edad INT;
BEGIN
    SELECT DATE_PART('year', AGE(fechaNacimiento)) INTO edad;
    RETURN edad;
END;
$$ LANGUAGE plpgsql;

