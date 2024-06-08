import psycopg2
from datetime import datetime

class Registro_datos:
    def __init__(self):
        self.conexion = psycopg2.connect(
            host='localhost',
            database='Proyecto', 
            user='postgres',
            password='Alda240497'
        )
  # CRUD pa
    
    # Métodos CRUD para la tabla accesoEmpleados
    def inserta_acceso_empleado(self, fechaAcceso, empleadoID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO accesoEmpleados (fechaAcceso, empleadoID) 
                 VALUES (%s, %s)'''
        cur.execute(sql, (fechaAcceso, empleadoID))
        self.conexion.commit()
        cur.close()

    def buscar_acceso_empleados(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM accesoEmpleados"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_acceso_empleado(self, accesoID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM accesoEmpleados WHERE accesoID = %s"
        cur.execute(sql, (accesoID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_acceso_empleado(self, accesoID, fechaAcceso, empleadoID):
        cur = self.conexion.cursor()
        sql = '''UPDATE accesoEmpleados SET fechaAcceso = %s, empleadoID = %s
                 WHERE accesoID = %s'''
        cur.execute(sql, (fechaAcceso, empleadoID, accesoID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla almacenes
    def inserta_almacen(self, nombre, sucursalID, direccionID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO almacenes (nombre, sucursalID, direccionID) 
                 VALUES (%s, %s, %s)'''
        cur.execute(sql, (nombre, sucursalID, direccionID))
        self.conexion.commit()
        cur.close()

    def buscar_almacenes(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM almacenes"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_almacen(self, almacenID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM almacenes WHERE almacenID = %s"
        cur.execute(sql, (almacenID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_almacen(self, almacenID, nombre, sucursalID, direccionID):
        cur = self.conexion.cursor()
        sql = '''UPDATE almacenes SET nombre = %s, sucursalID = %s, direccionID = %s
                 WHERE almacenID = %s'''
        cur.execute(sql, (nombre, sucursalID, direccionID, almacenID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla cambioPrecios
    def inserta_cambio_precio(self, precioAnterior, precioNuevo, fechaCambio, productoID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO cambioPrecios (precioAnterior, precioNuevo, fechaCambio, productoID) 
                 VALUES (%s, %s, %s, %s)'''
        cur.execute(sql, (precioAnterior, precioNuevo, fechaCambio, productoID))
        self.conexion.commit()
        cur.close()

    def buscar_cambio_precios(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM cambioPrecios"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_cambio_precio(self, cambioPrecioID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM cambioPrecios WHERE cambioPrecioID = %s"
        cur.execute(sql, (cambioPrecioID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_cambio_precio(self, cambioPrecioID, precioAnterior, precioNuevo, fechaCambio, productoID):
        cur = self.conexion.cursor()
        sql = '''UPDATE cambioPrecios SET precioAnterior = %s, precioNuevo = %s, fechaCambio = %s, productoID = %s
                 WHERE cambioPrecioID = %s'''
        cur.execute(sql, (precioAnterior, precioNuevo, fechaCambio, productoID, cambioPrecioID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla clientes
    def inserta_cliente(self, personaID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO clientes (personaID) 
                 VALUES (%s)'''
        cur.execute(sql, (personaID,))
        self.conexion.commit()
        cur.close()

    def buscar_clientes(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM clientes"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_cliente(self, clienteID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM clientes WHERE clienteID = %s"
        cur.execute(sql, (clienteID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_cliente(self, clienteID, personaID):
        cur = self.conexion.cursor()
        sql = '''UPDATE clientes SET personaID = %s
                 WHERE clienteID = %s'''
        cur.execute(sql, (personaID, clienteID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla direcciones
    def inserta_direccion(self, calle, ciudad, estado, pais, codigoPostal):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO direcciones (calle, ciudad, estado, pais, codigoPostal) 
                 VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(sql, (calle, ciudad, estado, pais, codigoPostal))
        self.conexion.commit()
        cur.close()

    def buscar_direcciones(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM direcciones"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_direccion(self, direccionID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM direcciones WHERE direccionID = %s"
        cur.execute(sql, (direccionID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_direccion(self, direccionID, calle, ciudad, estado, pais, codigoPostal):
        cur = self.conexion.cursor()
        sql = '''UPDATE direcciones SET calle = %s, ciudad = %s, estado = %s, pais = %s, codigoPostal = %s
                 WHERE direccionID = %s'''
        cur.execute(sql, (calle, ciudad, estado, pais, codigoPostal, direccionID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla empleados
    def inserta_empleado(self, personaID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO empleados (personaID) 
                 VALUES (%s)'''
        cur.execute(sql, (personaID,))
        self.conexion.commit()
        cur.close()

    def buscar_empleados(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM empleados"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_empleado(self, empleadoID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM empleados WHERE empleadoID = %s"
        cur.execute(sql, (empleadoID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_empleado(self, empleadoID, personaID):
        cur = self.conexion.cursor()
        sql = '''UPDATE empleados SET personaID = %s
                 WHERE empleadoID = %s'''
        cur.execute(sql, (personaID, empleadoID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla gastos
    def inserta_gasto(self, monto, fechaGasto, sucursalID, proveedorID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO gastos (monto, fechaGasto, sucursalID, proveedorID) 
                 VALUES (%s, %s, %s, %s)'''
        cur.execute(sql, (monto, fechaGasto, sucursalID, proveedorID))
        self.conexion.commit()
        cur.close()

    def buscar_gastos(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM gastos"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_gasto(self, gastoID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM gastos WHERE gastoID = %s"
        cur.execute(sql, (gastoID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_gasto(self, gastoID, monto, fechaGasto, sucursalID, proveedorID):
        cur = self.conexion.cursor()
        sql = '''UPDATE gastos SET monto = %s, fechaGasto = %s, sucursalID = %s, proveedorID = %s
                 WHERE gastoID = %s'''
        cur.execute(sql, (monto, fechaGasto, sucursalID, proveedorID, gastoID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla inventarioAlmacenes
    def inserta_inventario_almacen(self, cantidad, almacenID, productoID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO inventarioAlmacenes (cantidad, almacenID, productoID) 
                 VALUES (%s, %s, %s)'''
        cur.execute(sql, (cantidad, almacenID, productoID))
        self.conexion.commit()
        cur.close()

    def buscar_inventario_almacenes(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM inventarioAlmacenes"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_inventario_almacen(self, inventarioID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM inventarioAlmacenes WHERE inventarioID = %s"
        cur.execute(sql, (inventarioID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_inventario_almacen(self, inventarioID, cantidad, almacenID, productoID):
        cur = self.conexion.cursor()
        sql = '''UPDATE inventarioAlmacenes SET cantidad = %s, almacenID = %s, productoID = %s
                 WHERE inventarioID = %s'''
        cur.execute(sql, (cantidad, almacenID, productoID, inventarioID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla inventarioSucursales
    def inserta_inventario_sucursal(self, cantidad, sucursalID, productoID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO inventarioSucursales (cantidad, sucursalID, productoID) 
                 VALUES (%s, %s, %s)'''
        cur.execute(sql, (cantidad, sucursalID, productoID))
        self.conexion.commit()
        cur.close()

    def buscar_inventario_sucursales(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM inventarioSucursales"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_inventario_sucursal(self, inventarioID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM inventarioSucursales WHERE inventarioID = %s"
        cur.execute(sql, (inventarioID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_inventario_sucursal(self, inventarioID, cantidad, sucursalID, productoID):
        cur = self.conexion.cursor()
        sql = '''UPDATE inventarioSucursales SET cantidad = %s, sucursalID = %s, productoID = %s
                 WHERE inventarioID = %s'''
        cur.execute(sql, (cantidad, sucursalID, productoID, inventarioID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla personas
    def inserta_persona(self, nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO personas (nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID) 
                 VALUES (%s, %s, %s, %s, %s, %s)'''
        cur.execute(sql, (nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID))
        self.conexion.commit()
        cur.close()

    def buscar_personas(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM personas"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_persona(self, personaID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM personas WHERE personaID = %s"
        cur.execute(sql, (personaID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_persona(self, personaID, nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID):
        cur = self.conexion.cursor()
        sql = '''UPDATE personas SET nombre = %s, apellidoM = %s, apellidoP = %s, fechaNacimiento = %s, edad = %s, direccionID = %s
                 WHERE personaID = %s'''
        cur.execute(sql, (nombre, apellidoM, apellidoP, fechaNacimiento, edad, direccionID, personaID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla productos
    def inserta_producto(self, nombre, cantidad, precio, codigo, fechaCaducidad):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO productos (nombre, cantidad, precio, codigo, fechaCaducidad) 
                 VALUES (%s, %s, %s, %s, %s)'''
        cur.execute(sql, (nombre, cantidad, precio, codigo, fechaCaducidad))
        self.conexion.commit()
        cur.close()

    def buscar_productos(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM productos"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_producto(self, productoID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM productos WHERE productoID = %s"
        cur.execute(sql, (productoID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom
    
    def busca_1_producto(self, productoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM productos WHERE productoID = %s"
        cur.execute(sql, (productoID,))
        nombrex = cur.fetchall()
        cur.close()     
        return nombrex

    def actualiza_producto(self, productoID, nombre, cantidad, precio, codigo, fechaCaducidad):
        cur = self.conexion.cursor()
        sql = '''UPDATE productos SET nombre = %s, cantidad = %s, precio = %s, codigo = %s, fechaCaducidad = %s
                 WHERE productoID = %s'''
        cur.execute(sql, (nombre, cantidad, precio, codigo, fechaCaducidad, productoID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla productosVendidos
    def inserta_producto_vendido(self, ventaID, productoID, cantidad, precioUnitario):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO productosVendidos (ventaID, productoID, cantidad, precioUnitario) 
                 VALUES (%s, %s, %s, %s)'''
        cur.execute(sql, (ventaID, productoID, cantidad, precioUnitario))
        self.conexion.commit()
        cur.close()

    def buscar_productos_vendidos(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM productosVendidos"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_producto_vendido(self, ventaID, productoID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM productosVendidos WHERE ventaID = %s AND productoID = %s"
        cur.execute(sql, (ventaID, productoID))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_producto_vendido(self, ventaID, productoID, cantidad, precioUnitario):
        cur = self.conexion.cursor()
        sql = '''UPDATE productosVendidos SET cantidad = %s, precioUnitario = %s
                 WHERE ventaID = %s AND productoID = %s'''
        cur.execute(sql, (cantidad, precioUnitario, ventaID, productoID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla proveedores
    def inserta_proveedor(self, personaID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO proveedores (personaID) 
                 VALUES (%s)'''
        cur.execute(sql, (personaID,))
        self.conexion.commit()
        cur.close()

    def buscar_proveedores(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM proveedores"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_proveedor(self, proveedorID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM proveedores WHERE proveedorID = %s"
        cur.execute(sql, (proveedorID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_proveedor(self, proveedorID, personaID):
        cur = self.conexion.cursor()
        sql = '''UPDATE proveedores SET personaID = %s
                 WHERE proveedorID = %s'''
        cur.execute(sql, (personaID, proveedorID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla registroClientes
    def inserta_registro_cliente(self, cantidadCompra, fechaUltimaCompra, clienteID, productoID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO registroClientes (cantidadCompra, fechaUltimaCompra, clienteID, productoID) 
                 VALUES (%s, %s, %s, %s)'''
        cur.execute(sql, (cantidadCompra, fechaUltimaCompra, clienteID, productoID))
        self.conexion.commit()
        cur.close()

    def buscar_registro_clientes(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM registroClientes"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_registro_cliente(self, registroClienteID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM registroClientes WHERE registroClienteID = %s"
        cur.execute(sql, (registroClienteID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_registro_cliente(self, registroClienteID, cantidadCompra, fechaUltimaCompra, clienteID, productoID):
        cur = self.conexion.cursor()
        sql = '''UPDATE registroClientes SET cantidadCompra = %s, fechaUltimaCompra = %s, clienteID = %s, productoID = %s
                 WHERE registroClienteID = %s'''
        cur.execute(sql, (cantidadCompra, fechaUltimaCompra, clienteID, productoID, registroClienteID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla sucursales
    def inserta_sucursal(self, nombre, direccionID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO sucursales (nombre, direccionID) 
                 VALUES (%s, %s)'''
        cur.execute(sql, (nombre, direccionID))
        self.conexion.commit()
        cur.close()

    def buscar_sucursales(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM sucursales"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_sucursal(self, sucursalID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM sucursales WHERE sucursalID = %s"
        cur.execute(sql, (sucursalID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_sucursal(self, sucursalID, nombre, direccionID):
        cur = self.conexion.cursor()
        sql = '''UPDATE sucursales SET nombre = %s, direccionID = %s
                 WHERE sucursalID = %s'''
        cur.execute(sql, (nombre, direccionID, sucursalID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla ticketCompras
    def inserta_ticket_compra(self, detalles, fechaCompra, proveedorID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO ticketCompras (detalles, fechaCompra, proveedorID) 
                 VALUES (%s, %s, %s)'''
        cur.execute(sql, (detalles, fechaCompra, proveedorID))
        self.conexion.commit()
        cur.close()

    def buscar_ticket_compras(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM ticketCompras"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_ticket_compra(self, ticketID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM ticketCompras WHERE ticketID = %s"
        cur.execute(sql, (ticketID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_ticket_compra(self, ticketID, detalles, fechaCompra, proveedorID):
        cur = self.conexion.cursor()
        sql = '''UPDATE ticketCompras SET detalles = %s, fechaCompra = %s, proveedorID = %s
                 WHERE ticketID = %s'''
        cur.execute(sql, (detalles, fechaCompra, proveedorID, ticketID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    # Métodos CRUD para la tabla ticketVentas
    def inserta_ticket_venta(self, total, fechaVenta, empleadoID, clienteID):
        cur = self.conexion.cursor()
        sql = '''INSERT INTO ventas (total, fechaVenta, empleadoID, clienteID) 
                 VALUES (%s, %s, %s, %s)'''
        cur.execute(sql, (total, fechaVenta, empleadoID, clienteID))
        self.conexion.commit()
        cur.close()

    def buscar_ticket_ventas(self):
        cursor = self.conexion.cursor()
        sql = "SELECT * FROM ventas"
        cursor.execute(sql)
        registro = cursor.fetchall()
        cursor.close()
        return registro

    def elimina_ticket_venta(self, ticketID):
        cur = self.conexion.cursor()
        sql = "DELETE FROM ventas WHERE ticketID = %s"
        cur.execute(sql, (ticketID,))
        nom = cur.rowcount
        self.conexion.commit()
        cur.close()
        return nom

    def actualiza_ticket_venta(self, ticketID, total, fechaVenta, empleadoID, clienteID):
        cur = self.conexion.cursor()
        sql = '''UPDATE ventas SET total = %s, fechaVenta = %s, empleadoID = %s, clienteID = %s
                 WHERE ticketID = %s'''
        cur.execute(sql, (total, fechaVenta, empleadoID, clienteID, ticketID))
        act = cur.rowcount
        self.conexion.commit()
        cur.close()
        return act

    def buscar_registro(self, tabla, campo, valor):
        cursor = self.conexion.cursor()
        # Construir la consulta SQL con los nombres de la tabla y el campo
        sql = f"SELECT * FROM {tabla} WHERE {campo} = %s"
        # Ejecutar la consulta con el valor del campo
        cursor.execute(sql, (valor,))
        resultado = cursor.fetchone()
        return resultado is not None

    def busca_1_acceso_empleado(self, accesoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM accesoEmpleados WHERE accesoID = %s"
        cur.execute(sql, (accesoID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_almacen(self, almacenID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM almacenes WHERE almacenID = %s"
        cur.execute(sql, (almacenID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_cambio_precio(self, cambioPrecioID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM cambioPrecios WHERE cambioPrecioID = %s"
        cur.execute(sql, (cambioPrecioID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_cliente(self, clienteID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM clientes WHERE clienteID = %s"
        cur.execute(sql, (clienteID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_direccion(self, direccionID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM direcciones WHERE direccionID = %s"
        cur.execute(sql, (direccionID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_empleado(self, empleadoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM empleados WHERE empleadoID = %s"
        cur.execute(sql, (empleadoID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_gasto(self, gastoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM gastos WHERE gastoID = %s"
        cur.execute(sql, (gastoID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_inventario_almacen(self, inventarioID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM inventarioAlmacenes WHERE inventarioID = %s"
        cur.execute(sql, (inventarioID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_inventario_sucursal(self, inventarioID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM inventarioSucursales WHERE inventarioID = %s"
        cur.execute(sql, (inventarioID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_persona(self, personaID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM personas WHERE personaID = %s"
        cur.execute(sql, (personaID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_producto(self, productoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM productos WHERE productoID = %s"
        cur.execute(sql, (productoID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_producto_vendido(self, ventaID, productoID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM productosVendidos WHERE ventaID = %s AND productoID = %s"
        cur.execute(sql, (ventaID, productoID))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_proveedor(self, proveedorID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM proveedores WHERE proveedorID = %s"
        cur.execute(sql, (proveedorID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_registro_cliente(self, registroClienteID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM registroClientes WHERE registroClienteID = %s"
        cur.execute(sql, (registroClienteID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_sucursal(self, sucursalID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM sucursales WHERE sucursalID = %s"
        cur.execute(sql, (sucursalID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_ticket_compra(self, ticketID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM ticketCompras WHERE ticketID = %s"
        cur.execute(sql, (ticketID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def busca_1_venta(self, ventaID):
        cur = self.conexion.cursor()
        sql = "SELECT * FROM ventas WHERE ventaID = %s"
        cur.execute(sql, (ventaID,))
        registro = cur.fetchall()
        cur.close()
        return registro

    def vista_ventas_por_sucursal(self):
        cursor = self.conexion.cursor()
        
        # Crear la vista
        sql_create_view = """
        CREATE OR REPLACE VIEW reporte_ventas_sucursal AS 
        SELECT 
            s.nombre AS sucursal,
            SUM(pv.cantidad) AS cantidad_total_productos,
            SUM(pv.cantidad * pv.precioUnitario) AS monto_total_ventas
        FROM 
            ventas v
        JOIN 
            sucursales s ON v.sucursalID = s.sucursalID
        JOIN 
            productosVendidos pv ON v.ventaID = pv.ventaID
        GROUP BY 
            s.nombre;
        """
        cursor.execute(sql_create_view)
        
        # Consultar los datos de la vista
        sql_select_view = """
        SELECT * FROM reporte_ventas_sucursal;
        """
        cursor.execute(sql_select_view)
        registro = cursor.fetchall()
        
        cursor.close()
        return registro

    def vista_cambio_de_precios(self):
        cursor = self.conexion.cursor()
        
        # Crear la vista
        sql_create_view = """
        CREATE OR REPLACE VIEW reporte_cambios_precios AS
        SELECT 
            p.nombre AS producto,
            cp.precioAnterior,
            cp.precioNuevo,
            cp.fechaCambio
        FROM 
            cambioPrecios cp
        JOIN 
            productos p ON cp.productoID = p.productoID
        ORDER BY 
            cp.fechaCambio DESC;
        """
        cursor.execute(sql_create_view)
        
        # Consultar los datos de la vista
        sql_select_view = """
        SELECT * FROM reporte_cambios_precios;
        """
        cursor.execute(sql_select_view)
        registro = cursor.fetchall()
        
        cursor.close()
        return registro

    def vista_inventario_por_almacen(self):        
        cursor = self.conexion.cursor()
        
        # Crear la vista
        sql_create_view = """
        CREATE OR REPLACE VIEW reporte_inventario_almacen AS
        SELECT 
            a.nombre AS almacen,
            p.nombre AS producto,
            ia.cantidad
        FROM 
            inventarioAlmacenes ia
        JOIN 
            almacenes a ON ia.almacenID = a.almacenID
        JOIN 
            productos p ON ia.productoID = p.productoID
        ORDER BY 
            a.nombre, p.nombre;
        """
        cursor.execute(sql_create_view)
        
        # Consultar los datos de la vista
        sql_select_view = """
        SELECT * FROM reporte_inventario_almacen;
        """
        cursor.execute(sql_select_view)
        registro = cursor.fetchall()
        
        cursor.close()
        return registro

    def vista_datos_de_cliente(self):
        cursor = self.conexion.cursor()
        
        # Crear la vista
        sql_create_view = """
        CREATE OR REPLACE VIEW reporte_clientes_con_edad AS
        SELECT 
            c.clienteID,
            p.nombre,
            p.apellidoP,
            p.apellidoM,
            p.fechaNacimiento,
            calcular_edad(p.fechaNacimiento) AS edad_calculada,
            d.calle,
            d.ciudad,
            d.estado,
            d.pais,
            d.codigoPostal
        FROM 
            clientes c
        JOIN 
            personas p ON c.personaID = p.personaID
        JOIN 
            direcciones d ON p.direccionID = d.direccionID;
        """
        cursor.execute(sql_create_view)
        
        # Consultar los datos de la vista
        sql_select_view = """
        SELECT * FROM reporte_clientes_con_edad;
        """
        cursor.execute(sql_select_view)
        registro = cursor.fetchall()
        
        cursor.close()
        return registro


# Ejemplo de uso
if __name__ == "__main__":
    registro = Registro_datos()
    # Ejemplo de inserción en productos
    registro.inserta_producto('carro', 1, 10.5,'ssdf','2023-01-01')
    productos = registro.buscar_productos()
    print(productos)
 