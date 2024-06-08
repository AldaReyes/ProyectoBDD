from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from conexionBD import *
from datetime import datetime
import sys

def centrar_ventana(window, width=800, height=600):
    screen_rect = QDesktopWidget().availableGeometry(window)
    screen_width = screen_rect.width()
    screen_height = screen_rect.height()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.setGeometry(x, y, width, height)

class Portada(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenido")
        centrar_ventana(self)

        layout = QVBoxLayout(self)

        label1 = QLabel("Bienvenido a StockMaster", self)
        label1.setFont(QFont("Times New Roman", 27))
        layout.addWidget(label1, alignment=Qt.AlignCenter)

        label2 = QLabel(
            "Universidad Autonoma de Mexico\nEscuela de Estudios Superiores Acatlan\n\n\nProyecto de Bases de Datos\n\n\nARTEAGA REYES ALDAIR\n GARCIA ALVARADO JOSE IYAQUIBALAM \n GONZÁLEZ ORDAZ ARIEL \n MADRIGAL GONZALEZ CYNTHIA", self)
        label2.setFont(QFont("Times New Roman", 17))
        label2.setWordWrap(True)
        label2.setAlignment(Qt.AlignCenter)
        layout.addWidget(label2, alignment=Qt.AlignCenter)

        self.button_next = QPushButton("Siguiente", self)
        self.button_next.clicked.connect(self.cerrar_portada)
        layout.addWidget(self.button_next, alignment=Qt.AlignCenter)

    def cerrar_portada(self):
        self.close()
        self.siguiente_panel = Interfaz()
        self.siguiente_panel.show()

# Clase Interfaz
class Interfaz(QWidget):
    registro_datos = Registro_datos()
    
    def verificar_Precios(self, cadena):
        try:
            float(cadena)
            return True
        except ValueError:
            return False
    
    def buscar_Producto(self):
        str_id = self.txt_Leer_Busqueda_ID_Producto.text().strip()
        if str_id != '':
            if str_id.isdigit():
                productoID = int(str_id)
                producto = self.registro_datos.busca_1_producto(productoID)
                
                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Producto.clearContents()
                
                if producto:
                    self.tblw_Leer_Tabla_Producto.setRowCount(1)
                    for col_idx, col_data in enumerate(producto[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Producto.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Producto.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)
  
    def crear_Producto(self):
        # Extraer los datos de la interfaz
        str_nombre = self.txt_Crear_Nombre_Producto.text().strip()
        str_codigo = self.txt_Crear_Codigo_Producto.text().strip()
        str_cantidad = self.txt_Crear_Cantidad_Producto.text().strip()
        str_precio = self.txt_Crear_Precio_Producto.text().strip()
        str_caducidad = self.de_Crear_Fecha_Caducidad_Producto.text().strip()

        # Verificar que los campos no estén vacíos
        if str_nombre != '' and str_codigo != '' and str_precio != '' and str_cantidad != '':
            # Verificar que el precio sea válido y la cantidad sea un número
            if self.verificar_Precios(str_precio) and str_cantidad.isdigit():
                # Verificar si el ID ya existe en la base de datos
                if self.registro_datos.buscar_registro('productos', 'codigo', str_codigo):
                    self.seleccion_MessageBox(3)
                else:
                    # Insertar los datos en la base de datos
                    self.registro_datos.inserta_producto(str_nombre, str_cantidad, str_precio, str_codigo, str_caducidad)
                    print("Producto insertado correctamente en la base de datos.")
                    # Limpiar los campos de entrada de texto
                    self.txt_Crear_Nombre_Producto.clear()
                    self.txt_Crear_Codigo_Producto.clear()
                    self.txt_Crear_Cantidad_Producto.clear()
                    self.txt_Crear_Precio_Producto.clear()
                    self.de_Crear_Fecha_Caducidad_Producto.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)
        
    def habilitar_actualizar_producto(self):
        str_id = self.txt_Modificar_Busqueda_ID_Producto.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_producto(str_id):
                if str_id.isdigit():
                    # Obtener los datos del producto
                    producto = self.registro_datos.busca_1_producto(str_id)
                    # Desempaquetar los datos
                    id_producto, nombre, cantidad, precio, codigo, fecha_caducidad = producto[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Nombre_Producto.setDisabled(False)
                    self.txt_Modificar_Codigo_Producto.setDisabled(False)
                    self.txt_Modificar_Cantidad_Producto.setDisabled(False)
                    self.txt_Modificar_Precio_Producto.setDisabled(False)
                    self.de_Modificar_Fecha_Caducidad_Producto.setDisabled(False) 
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Modificar_Busqueda_ID_Producto.setText(str(id_producto))
                    self.txt_Modificar_Nombre_Producto.setText(nombre)
                    self.txt_Modificar_Codigo_Producto.setText(codigo)
                    self.txt_Modificar_Cantidad_Producto.setText(str(cantidad))
                    self.txt_Modificar_Precio_Producto.setText(str(precio))
                    self.de_Modificar_Fecha_Caducidad_Producto.setDate(fecha_caducidad)
                else:
                    self.seleccion_MessageBox(2)  
            else:
                self.seleccion_MessageBox(4)          
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)
   
    def actualizar_Producto(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Producto.text().strip()
        str_nombre = self.txt_Modificar_Nombre_Producto.text().strip()
        str_codigo = self.txt_Modificar_Codigo_Producto.text().strip()
        str_cantidad = self.txt_Modificar_Cantidad_Producto.text().strip()
        str_precio = self.txt_Modificar_Precio_Producto.text().strip()
        str_caducidad = self.de_Modificar_Fecha_Caducidad_Producto.text().strip()
        if str_id != '' and str_nombre != '' and str_codigo != '' and str_precio != '' and str_cantidad != '':
            # Verificar que el precio sea válido y la cantidad sea un número
            if self.verificar_Precios(str_precio) and str_cantidad.isdigit():
                    # Insertar los datos en la base de datos
                    self.registro_datos.actualiza_producto(str_id, str_nombre, str_cantidad, str_precio, str_codigo, str_caducidad)
                    print("Producto actualizado correctamente en la base de datos.")
                    # Limpiar los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Producto.clear()
                    self.txt_Modificar_Nombre_Producto.clear()
                    self.txt_Modificar_Codigo_Producto.clear()
                    self.txt_Modificar_Cantidad_Producto.clear()
                    self.txt_Modificar_Precio_Producto.clear()
                    self.de_Modificar_Fecha_Caducidad_Producto.clear()
            else:
                    self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)
    
    def buscar_eliminar_producto(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Producto.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_producto(str_id):
                if str_id.isdigit():
                    # Obtener los datos del producto
                    producto = self.registro_datos.busca_1_producto(str_id)
                    # Desempaquetar los datos
                    id_producto, nombre, cantidad, precio, codigo, fecha_caducidad = producto[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Nombre_Producto.setDisabled(True)
                    self.txt_Eliminar_Codigo_Producto.setDisabled(True)
                    self.txt_Eliminar_Cantidad_Producto.setDisabled(True)
                    self.txt_Eliminar_Precio_Producto.setDisabled(True)
                    self.de_Eliminar_Fecha_Caducidad_Producto.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Producto.setText(str(id_producto))
                    self.txt_Eliminar_Nombre_Producto.setText(nombre)
                    self.txt_Eliminar_Codigo_Producto.setText(codigo)
                    self.txt_Eliminar_Cantidad_Producto.setText(str(cantidad))
                    self.txt_Eliminar_Precio_Producto.setText(str(precio))
                    self.de_Eliminar_Fecha_Caducidad_Producto.setDate(fecha_caducidad)
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Nombre_Producto.setReadOnly(True)
                    self.txt_Eliminar_Codigo_Producto.setReadOnly(True)
                    self.txt_Eliminar_Cantidad_Producto.setReadOnly(True)
                    self.txt_Eliminar_Precio_Producto.setReadOnly(True)
                    self.de_Eliminar_Fecha_Caducidad_Producto.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2) 
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_producto(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Producto.text().strip()
        str_nombre = self.txt_Eliminar_Nombre_Producto.text().strip()
        str_codigo = self.txt_Eliminar_Codigo_Producto.text().strip()
        str_cantidad = self.txt_Eliminar_Cantidad_Producto.text().strip()
        str_precio = self.txt_Eliminar_Precio_Producto.text().strip()
        str_caducidad = self.de_Eliminar_Fecha_Caducidad_Producto.text().strip()
        
        # Verificar que los campos no estén vacíos
        if str_id != '' and str_nombre != '' and str_codigo != '' and str_precio != '' and str_cantidad != '':
            # Verificar que el precio sea válido y la cantidad sea un número
            if self.verificar_Precios(str_precio) and str_cantidad.isdigit():
                # Insertar los datos en la base de datos
                self.registro_datos.elimina_producto(str_id)
                print("Producto eliminado correctamente de la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Eliminar_Busqueda_ID_Producto.clear()
                self.txt_Eliminar_Nombre_Producto.clear()
                self.txt_Eliminar_Codigo_Producto.clear()
                self.txt_Eliminar_Cantidad_Producto.clear()
                self.txt_Eliminar_Precio_Producto.clear()
                self.de_Eliminar_Fecha_Caducidad_Producto.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)
            
    def buscar_InventarioAlmacenes(self):
        str_id = self.txt_Leer_Busqueda_ID_InvAlm.text().strip()
        if str_id != '':
            if str_id.isdigit():
                inventarioID = int(str_id)
                inventario = self.registro_datos.busca_1_inventario_almacen(inventarioID)
                
                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_InvAlm.clearContents()
                
                if inventario:
                    self.tblw_Leer_Tabla_InvAlm.setRowCount(1)
                    for col_idx, col_data in enumerate(inventario[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_InvAlm.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_InvAlm.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_InventarioAlmacenes(self):
        # Extraer los datos de la interfaz
        str_cantidad = self.txt_Crear_Cantidad_InvAlm.text().strip()
        str_id_almacen = self.txt_Crear_ID_Almacen_InvAlm.text().strip()
        str_id_producto = self.txt_Crear_ID_Producto_InvAlm.text().strip()

        # Verificar que los campos no estén vacíos
        if str_cantidad != '' and str_id_almacen != '' and str_id_producto != '':
            # Verificar que la cantidad sea un número
            if str_cantidad.isdigit():
                # Verificar si el inventario ya existe en la base de datos
                if self.registro_datos.buscar_inventario_almacenes(str_id_almacen, str_id_producto):
                    self.seleccion_MessageBox(3)
                else:
                    # Insertar los datos en la base de datos
                    self.registro_datos.inserta_inventario_almacen(str_cantidad, str_id_almacen, str_id_producto)
                    print("Inventario insertado correctamente en la base de datos.")
                    # Limpiar los campos de entrada de texto
                    self.txt_Crear_Cantidad_InvAlm.clear()
                    self.txt_Crear_ID_Almacen_InvAlm.clear()
                    self.txt_Crear_ID_Producto_InvAlm.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_InventarioAlmacenes(self):
        str_id = self.txt_Modificar_ID_Inventario_InvAlm.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_inventario_almacen(str_id):
                if str_id.isdigit():
                    # Obtener los datos del inventario
                    inventario = self.registro_datos.busca_1_inventario_almacen(str_id)
                    # Desempaquetar los datos
                    id_inventario, cantidad, id_almacen, id_producto = inventario[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Cantidad_InvAlm.setDisabled(False)
                    self.txt_Modificar_ID_Almacen_InvAlm.setDisabled(False)
                    self.txt_Modificar_ID_Producto_InvAlm.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Modificar_ID_Inventario_InvAlm.setText(str(id_inventario))
                    self.txt_Modificar_Cantidad_InvAlm.setText(str(cantidad))
                    self.txt_Modificar_ID_Almacen_InvAlm.setText(str(id_almacen))
                    self.txt_Modificar_ID_Producto_InvAlm.setText(str(id_producto))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def actualizar_InventarioAlmacenes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_ID_Inventario_InvAlm.text().strip()
        str_cantidad = self.txt_Modificar_Cantidad_InvAlm.text().strip()
        str_id_almacen = self.txt_Modificar_ID_Almacen_InvAlm.text().strip()
        str_id_producto = self.txt_Modificar_ID_Producto_InvAlm.text().strip()
        
        # Verificar que los campos no estén vacíos
        if str_id != '' and str_cantidad != '' and str_id_almacen != '' and str_id_producto != '':
            # Verificar que la cantidad sea un número
            if str_cantidad.isdigit():
                # Actualizar los datos en la base de datos
                self.registro_datos.actualiza_inventario_almacen(str_id, str_cantidad, str_id_almacen, str_id_producto)
                print("Inventario actualizado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_ID_Inventario_InvAlm.clear()
                self.txt_Modificar_Cantidad_InvAlm.clear()
                self.txt_Modificar_ID_Almacen_InvAlm.clear()
                self.txt_Modificar_ID_Producto_InvAlm.clear()
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def buscar_eliminar_InventarioAlmacenes(self):
        str_id = self.txt_Eliminar_ID_Inventario_InvAlm.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_inventario_almacen(str_id):
                if str_id.isdigit():
                    # Obtener los datos del inventario
                    inventario = self.registro_datos.busca_1_inventario_almacen(str_id)
                    # Desempaquetar los datos
                    id_inventario, cantidad, id_almacen, id_producto = inventario[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Cantidad_InvAlm.setDisabled(True)
                    self.txt_Eliminar_ID_Almacen_InvAlm.setDisabled(True)
                    self.txt_Eliminar_ID_Producto_InvAlm.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_ID_Inventario_InvAlm.setText(str(id_inventario))
                    self.txt_Eliminar_Cantidad_InvAlm.setText(str(cantidad))
                    self.txt_Eliminar_ID_Almacen_InvAlm.setText(str(id_almacen))
                    self.txt_Eliminar_ID_Producto_InvAlm.setText(str(id_producto))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Cantidad_InvAlm.setReadOnly(True)
                    self.txt_Eliminar_ID_Almacen_InvAlm.setReadOnly(True)
                    self.txt_Eliminar_ID_Producto_InvAlm.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def eliminar_InventarioAlmacenes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_ID_Inventario_InvAlm.text().strip()
        str_cantidad = self.txt_Eliminar_Cantidad_InvAlm.text().strip()
        str_id_almacen = self.txt_Eliminar_ID_Almacen_InvAlm.text().strip()
        str_id_producto = self.txt_Eliminar_ID_Producto_InvAlm.text().strip()
        
        # Verificar que los campos no estén vacíos
        if str_id != '' and str_cantidad != '' and str_id_almacen != '' and str_id_producto != '':
            # Verificar que la cantidad sea un número
            if str_cantidad.isdigit():
                # Eliminar el inventario de la base de datos
                self.registro_datos.elimina_inventario_almacen(str_id)
                print("Inventario eliminado correctamente de la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Eliminar_ID_Inventario_InvAlm.clear()
                self.txt_Eliminar_Cantidad_InvAlm.clear()
                self.txt_Eliminar_ID_Almacen_InvAlm.clear()
                self.txt_Eliminar_ID_Producto_InvAlm.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(1)

    def buscar_accesoEmpleados(self):
        str_id = self.txt_Leer_Busqueda_ID_AccEmpl.text().strip()
        if str_id != '':
            if str_id.isdigit():
                accesoID = int(str_id)
                acceso = self.registro_datos.busca_1_acceso_empleado(accesoID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_AccEmpl.clearContents()

                if acceso:
                    self.tblw_Leer_Tabla_AccEmpl.setRowCount(1)
                    for col_idx, col_data in enumerate(acceso[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_AccEmpl.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_AccEmpl.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_accesoEmpleados(self):
        # Extraer los datos de la interfaz
        str_id_empleado = self.txt_Crear_ID_Empleado_AccEmpl.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id_empleado != '':
            # Verificar si el ID ya existe en la base de datos
            if self.registro_datos.buscar_registro('accesos', 'id_empleado', str_id_empleado):
                self.seleccion_MessageBox(3)
            else:
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_acceso_empleado(str_id_empleado)
                print("Acceso insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_ID_Empleado_AccEmpl.clear()
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_accesoEmpleados(self):
        str_id = self.txt_Modificar_Busqueda_ID_AccEmpl.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_acceso_empleado(str_id):
                if str_id.isdigit():
                    # Obtener los datos del acceso
                    acceso = self.registro_datos.busca_1_acceso_empleado(str_id)
                    # Desempaquetar los datos
                    id_acceso, id_empleado = acceso[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Empleado_AccEmpl.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_AccEmpl.setText(str(id_acceso))
                    self.txt_Modificar_ID_Empleado_AccEmpl.setText(str(id_empleado))
                else:
                    self.seleccion_MessageBox(2)  
            else:
                self.seleccion_MessageBox(4)          
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_accesoEmpleados(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_AccEmpl.text().strip()
        str_id_empleado = self.txt_Modificar_ID_Empleado_AccEmpl.text().strip()

        if str_id != '' and str_id_empleado != '':
            # Insertar los datos en la base de datos
            self.registro_datos.actualiza_acceso_empleado(str_id, str_id_empleado)
            print("Acceso actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_AccEmpl.clear()
            self.txt_Modificar_ID_Empleado_AccEmpl.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_accesoEmpleados(self):
        str_id = self.txt_Eliminar_Busqueda_ID_AccEmpl.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_acceso_empleado(str_id):
                if str_id.isdigit():
                    # Obtener los datos del acceso
                    acceso = self.registro_datos.busca_1_acceso_empleado(str_id)
                    # Desempaquetar los datos
                    id_acceso, id_empleado = acceso[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_ID_Empleado_AccEmpl.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_AccEmpl.setText(str(id_acceso))
                    self.txt_Eliminar_ID_Empleado_AccEmpl.setText(str(id_empleado))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_ID_Empleado_AccEmpl.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2) 
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_accesoEmpleados(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_AccEmpl.text().strip()
        str_id_empleado = self.txt_Eliminar_ID_Empleado_AccEmpl.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_id_empleado != '':
            # Insertar los datos en la base de datos
            self.registro_datos.elimina_acceso_empleado(str_id)
            print("Acceso eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_AccEmpl.clear()
            self.txt_Eliminar_ID_Empleado_AccEmpl.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)


    def buscar_Almacenes(self):
        str_id = self.txt_Leer_Busqueda_ID_LocAlm.text().strip()
        if str_id != '':
            if str_id.isdigit():
                almacenID = int(str_id)
                almacen = self.registro_datos.busca_1_almacen(almacenID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_LocAlm.clearContents()

                if almacen:
                    self.tblw_Leer_Tabla_LocAlm.setRowCount(1)
                    for col_idx, col_data in enumerate(almacen[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_LocAlm.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_LocAlm.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Almacenes(self):
        # Extraer los datos de la interfaz
        str_nombre = self.txt_Crear_Nombre_LocAlm.text().strip()
        str_id_sucursal = self.txt_Crear_ID_Sucursal_LocAlm.text().strip()
        str_id_direccion = self.txt_Crear_ID_Direccion_LocAlm.text().strip()

        # Verificar que los campos no estén vacíos
        if str_nombre != '' and str_id_sucursal != '' and str_id_direccion != '':
            # Insertar los datos en la base de datos
            self.registro_datos.inserta_almacen(str_nombre, str_id_sucursal, str_id_direccion)
            print("Almacén insertado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Crear_Nombre_LocAlm.clear()
            self.txt_Crear_ID_Sucursal_LocAlm.clear()
            self.txt_Crear_ID_Direccion_LocAlm.clear()
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Almacenes(self):
        str_id = self.txt_Modificar_Busqueda_ID_LocAlm.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_almacen(str_id):
                if str_id.isdigit():
                    # Obtener los datos del almacén
                    almacen = self.registro_datos.busca_1_almacen(str_id)
                    # Desempaquetar los datos
                    id_almacen, nombre, id_sucursal, id_direccion = almacen[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Nombre_LocAlm.setDisabled(False)
                    self.txt_Modificar_ID_Sucursal_LocAlm.setDisabled(False)
                    self.txt_Modificar_ID_Direccion_LocAlm.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_LocAlm.setText(str(id_almacen))
                    self.txt_Modificar_Nombre_LocAlm.setText(nombre)
                    self.txt_Modificar_ID_Sucursal_LocAlm.setText(str(id_sucursal))
                    self.txt_Modificar_ID_Direccion_LocAlm.setText(str(id_direccion))
                else:
                    self.seleccion_MessageBox(2)  
            else:
                self.seleccion_MessageBox(4)          
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Almacenes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_LocAlm.text().strip()
        str_nombre = self.txt_Modificar_Nombre_LocAlm.text().strip()
        str_id_sucursal = self.txt_Modificar_ID_Sucursal_LocAlm.text().strip()
        str_id_direccion = self.txt_Modificar_ID_Direccion_LocAlm.text().strip()

        if str_id != '' and str_nombre != '' and str_id_sucursal != '' and str_id_direccion != '':
            # Insertar los datos en la base de datos
            self.registro_datos.actualiza_almacen(str_id, str_nombre, str_id_sucursal, str_id_direccion)
            print("Almacén actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_LocAlm.clear()
            self.txt_Modificar_Nombre_LocAlm.clear()
            self.txt_Modificar_ID_Sucursal_LocAlm.clear()
            self.txt_Modificar_ID_Direccion_LocAlm.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Almacenes(self):
        str_id = self.txt_Eliminar_Busqueda_ID_LocAlm.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_almacen(str_id):
                if str_id.isdigit():
                    # Obtener los datos del almacén
                    almacen = self.registro_datos.busca_1_almacen(str_id)
                    # Desempaquetar los datos
                    id_almacen, nombre, id_sucursal, id_direccion = almacen[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Nombre_LocAlm.setDisabled(True)
                    self.txt_Eliminar_ID_Sucursal_LocAlm.setDisabled(True)
                    self.txt_Eliminar_ID_Direccion_LocAlm.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_LocAlm.setText(str(id_almacen))
                    self.txt_Eliminar_Nombre_LocAlm.setText(nombre)
                    self.txt_Eliminar_ID_Sucursal_LocAlm.setText(str(id_sucursal))
                    self.txt_Eliminar_ID_Direccion_LocAlm.setText(str(id_direccion))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Nombre_LocAlm.setReadOnly(True)
                    self.txt_Eliminar_ID_Sucursal_LocAlm.setReadOnly(True)
                    self.txt_Eliminar_ID_Direccion_LocAlm.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2) 
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Almacenes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_LocAlm.text().strip()
        str_nombre = self.txt_Eliminar_Nombre_LocAlm.text().strip()
        str_id_sucursal = self.txt_Eliminar_ID_Sucursal_LocAlm.text().strip()
        str_id_direccion = self.txt_Eliminar_ID_Direccion_LocAlm.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_nombre != '' and str_id_sucursal != '' and str_id_direccion != '':
            # Insertar los datos en la base de datos
            self.registro_datos.elimina_almacen(str_id)
            print("Almacén eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_LocAlm.clear()
            self.txt_Eliminar_Nombre_LocAlm.clear()
            self.txt_Eliminar_ID_Sucursal_LocAlm.clear()
            self.txt_Eliminar_ID_Direccion_LocAlm.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)


    def buscar_Clientes(self):
        str_id = self.txt_Leer_Busqueda_ID_Cliente.text().strip()
        if str_id != '':
            if str_id.isdigit():
                clienteID = int(str_id)
                cliente = self.registro_datos.busca_1_cliente(clienteID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Cliente.clearContents()

                if cliente:
                    self.tblw_Leer_Tabla_Cliente.setRowCount(1)
                    for col_idx, col_data in enumerate(cliente[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Cliente.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Cliente.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Clientes(self):
        # Extraer los datos de la interfaz
        str_id_persona = self.txt_Crear_ID_Persona_Cliente.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id_persona != '':
            # Insertar los datos en la base de datos
            self.registro_datos.inserta_cliente(str_id_persona)
            print("Cliente insertado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Crear_ID_Persona_Cliente.clear()
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Clientes(self):
        str_id = self.txt_Modificar_Busqueda_ID_Cliente.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_cliente(str_id):
                if str_id.isdigit():
                    # Obtener los datos del cliente
                    cliente = self.registro_datos.busca_1_cliente(str_id)
                    # Desempaquetar los datos
                    id_cliente, id_persona = cliente[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Persona_Cliente.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Cliente.setText(str(id_cliente))
                    self.txt_Modificar_ID_Persona_Cliente.setText(str(id_persona))
                else:
                    self.seleccion_MessageBox(2)  
            else:
                self.seleccion_MessageBox(4)          
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Clientes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Cliente.text().strip()
        str_id_persona = self.txt_Modificar_ID_Persona_Cliente.text().strip()

        if str_id != '' and str_id_persona != '':
            # Insertar los datos en la base de datos
            self.registro_datos.actualiza_cliente(str_id, str_id_persona)
            print("Cliente actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_Cliente.clear()
            self.txt_Modificar_ID_Persona_Cliente.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Clientes(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Cliente.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_cliente(str_id):
                if str_id.isdigit():
                    # Obtener los datos del cliente
                    cliente = self.registro_datos.busca_1_cliente(str_id)
                    # Desempaquetar los datos
                    id_cliente, id_persona = cliente[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_ID_Persona_Cliente.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Cliente.setText(str(id_cliente))
                    self.txt_Eliminar_ID_Persona_Cliente.setText(str(id_persona))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_ID_Persona_Cliente.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2) 
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Clientes(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Cliente.text().strip()
        str_id_persona = self.txt_Eliminar_ID_Persona_Cliente.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_id_persona != '':
            # Insertar los datos en la base de datos
            self.registro_datos.elimina_cliente(str_id)
            print("Cliente eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Cliente.clear()
            self.txt_Eliminar_ID_Persona_Cliente.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

     
    def buscar_Direcciones(self):
        str_id = self.txt_Leer_Busqueda_ID_Direccion.text().strip()
        if str_id != '':
            if str_id.isdigit():
                direccionID = int(str_id)
                direccion = self.registro_datos.busca_1_direccion(direccionID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Direccion.clearContents()

                if direccion:
                    self.tblw_Leer_Tabla_Direccion.setRowCount(1)
                    for col_idx, col_data in enumerate(direccion[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Direccion.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Direccion.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Direcciones(self):
        # Extraer los datos de la interfaz
        str_calle = self.txt_Crear_Calle_Direccion.text().strip()
        str_ciudad = self.txt_Crear_Ciudad_Direccion.text().strip()
        str_estado = self.txt_Crear_Estado_Direccion.text().strip()
        str_pais = self.txt_Crear_Pais_Direccion.text().strip()
        str_codigo_postal = self.txt_Crear_CodigoPostal_Direccion.text().strip()

        # Verificar que los campos no estén vacíos
        if str_calle != '' and str_ciudad != '' and str_estado != '' and str_pais != '' and str_codigo_postal != '':
            # Insertar los datos en la base de datos
            self.registro_datos.inserta_direccion(str_calle, str_ciudad, str_estado, str_pais, str_codigo_postal)
            print("Dirección insertada correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Crear_Calle_Direccion.clear()
            self.txt_Crear_Ciudad_Direccion.clear()
            self.txt_Crear_Estado_Direccion.clear()
            self.txt_Crear_Pais_Direccion.clear()
            self.txt_Crear_CodigoPostal_Direccion.clear()
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Direcciones(self):
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_direccion(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la dirección
                    direccion = self.registro_datos.busca_1_direccion(str_id)
                    # Desempaquetar los datos
                    id_direccion, calle, ciudad, estado, pais, codigo_postal = direccion[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Calle_Direccion.setDisabled(False)
                    self.txt_Modificar_Ciudad_Direccion.setDisabled(False)
                    self.txt_Modificar_Estado_Direccion.setDisabled(False)
                    self.txt_Modificar_Pais_Direccion.setDisabled(False)
                    self.txt_Modificar_CodigoPostal_Direccion.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Proveedor.setText(str(id_direccion))
                    self.txt_Modificar_Calle_Direccion.setText(calle)
                    self.txt_Modificar_Ciudad_Direccion.setText(ciudad)
                    self.txt_Modificar_Estado_Direccion.setText(estado)
                    self.txt_Modificar_Pais_Direccion.setText(pais)
                    self.txt_Modificar_CodigoPostal_Direccion.setText(codigo_postal)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Direcciones(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        str_calle = self.txt_Modificar_Calle_Direccion.text().strip()
        str_ciudad = self.txt_Modificar_Ciudad_Direccion.text().strip()
        str_estado = self.txt_Modificar_Estado_Direccion.text().strip()
        str_pais = self.txt_Modificar_Pais_Direccion.text().strip()
        str_codigo_postal = self.txt_Modificar_CodigoPostal_Direccion.text().strip()

        if str_id != '' and str_calle != '' and str_ciudad != '' and str_estado != '' and str_pais != '' and str_codigo_postal != '':
            # Insertar los datos en la base de datos
            self.registro_datos.actualiza_direccion(str_id, str_calle, str_ciudad, str_estado, str_pais, str_codigo_postal)
            print("Dirección actualizada correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_Proveedor.clear()
            self.txt_Modificar_Calle_Direccion.clear()
            self.txt_Modificar_Ciudad_Direccion.clear()
            self.txt_Modificar_Estado_Direccion.clear()
            self.txt_Modificar_Pais_Direccion.clear()
            self.txt_Modificar_CodigoPostal_Direccion.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Direcciones(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_direccion(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la dirección
                    direccion = self.registro_datos.busca_1_direccion(str_id)
                    # Desempaquetar los datos
                    id_direccion, calle, ciudad, estado, pais, codigo_postal = direccion[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Calle_Direccion.setDisabled(True)
                    self.txt_Eliminar_Ciudad_Direccion.setDisabled(True)
                    self.txt_Eliminar_Estado_Direccion.setDisabled(True)
                    self.txt_Eliminar_Pais_Direccion.setDisabled(True)
                    self.txt_Eliminar_CodigoPostal_Direccion.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Proveedor.setText(str(id_direccion))
                    self.txt_Eliminar_Calle_Direccion.setText(calle)
                    self.txt_Eliminar_Ciudad_Direccion.setText(ciudad)
                    self.txt_Eliminar_Estado_Direccion.setText(estado)
                    self.txt_Eliminar_Pais_Direccion.setText(pais)
                    self.txt_Eliminar_CodigoPostal_Direccion.setText(codigo_postal)
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Calle_Direccion.setReadOnly(True)
                    self.txt_Eliminar_Ciudad_Direccion.setReadOnly(True)
                    self.txt_Eliminar_Estado_Direccion.setReadOnly(True)
                    self.txt_Eliminar_Pais_Direccion.setReadOnly(True)
                    self.txt_Eliminar_CodigoPostal_Direccion.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Direcciones(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        str_calle = self.txt_Eliminar_Calle_Direccion.text().strip()
        str_ciudad = self.txt_Eliminar_Ciudad_Direccion.text().strip()
        str_estado = self.txt_Eliminar_Estado_Direccion.text().strip()
        str_pais = self.txt_Eliminar_Pais_Direccion.text().strip()
        str_codigo_postal = self.txt_Eliminar_CodigoPostal_Direccion.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_calle != '' and str_ciudad != '' and str_estado != '' and str_pais != '' and str_codigo_postal != '':
            # Insertar los datos en la base de datos
            self.registro_datos.elimina_direccion(str_id)
            print("Dirección eliminada correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Proveedor.clear()
            self.txt_Eliminar_Calle_Direccion.clear()
            self.txt_Eliminar_Ciudad_Direccion.clear()
            self.txt_Eliminar_Estado_Direccion.clear()
            self.txt_Eliminar_Pais_Direccion.clear()
            self.txt_Eliminar_CodigoPostal_Direccion.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

     
    def buscar_Empleados(self):
        str_id = self.txt_Leer_Busqueda_ID_Empl.text().strip()
        if str_id != '':
            if str_id.isdigit():
                empleadoID = int(str_id)
                empleado = self.registro_datos.busca_1_empleado(empleadoID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Empl.clearContents()

                if empleado:
                    self.tblw_Leer_Tabla_Empl.setRowCount(1)
                    for col_idx, col_data in enumerate(empleado[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Empl.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Empl.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Empleados(self):
        # Extraer los datos de la interfaz
        str_id_persona = self.txt_Crear_ID_Persona_Empleado.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id_persona != '':
            # Verificar si el ID ya existe en la base de datos
            if self.registro_datos.buscar_registro('empleados', 'id_persona', str_id_persona):
                self.seleccion_MessageBox(3)
            else:
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_empleado(str_id_persona)
                print("Empleado insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_ID_Persona_Empleado.clear()
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Empleados(self):
        str_id = self.txt_Modificar_Busqueda_ID_Empleado.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_empleado(str_id):
                if str_id.isdigit():
                    # Obtener los datos del empleado
                    empleado = self.registro_datos.busca_1_empleado(str_id)
                    # Desempaquetar los datos
                    id_empleado, id_persona = empleado[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Persona_Empleado.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Empleado.setText(str(id_empleado))
                    self.txt_Modificar_ID_Persona_Empleado.setText(str(id_persona))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Empleados(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Empleado.text().strip()
        str_id_persona = self.txt_Modificar_ID_Persona_Empleado.text().strip()

        if str_id != '' and str_id_persona != '':
            # Insertar los datos en la base de datos
            self.registro_datos.actualiza_empleado(str_id, str_id_persona)
            print("Empleado actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_Empleado.clear()
            self.txt_Modificar_ID_Persona_Empleado.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Empleados(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Empleado.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_empleado(str_id):
                if str_id.isdigit():
                    # Obtener los datos del empleado
                    empleado = self.registro_datos.busca_1_empleado(str_id)
                    # Desempaquetar los datos
                    id_empleado, id_persona = empleado[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_ID_Persona_Empleado.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Empleado.setText(str(id_empleado))
                    self.txt_Eliminar_ID_Persona_Empleado.setText(str(id_persona))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_ID_Persona_Empleado.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Empleados(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Empleado.text().strip()
        str_id_persona = self.txt_Eliminar_ID_Persona_Empleado.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_id_persona != '':
            # Insertar los datos en la base de datos
            self.registro_datos.elimina_empleado(str_id)
            print("Empleado eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Empleado.clear()
            self.txt_Eliminar_ID_Persona_Empleado.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)


    def buscar_Gastos(self):
        str_id = self.txt_Leer_Busqueda_ID_Gastos.text().strip()
        if str_id != '':
            if str_id.isdigit():
                gastoID = int(str_id)
                gasto = self.registro_datos.busca_1_gasto(gastoID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Gastos.clearContents()

                if gasto:
                    self.tblw_Leer_Tabla_Gastos.setRowCount(1)
                    for col_idx, col_data in enumerate(gasto[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Gastos.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Gastos.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Gastos(self):
        # Extraer los datos de la interfaz
        str_monto = self.txt_Crear_Monto_Gasto.text().strip()
        str_id_sucursal = self.txt_Crear_ID_Sucursal_Gasto.text().strip()
        str_id_proveedor = self.txt_Crear_ID_Proveedor_Gasto.text().strip()

        # Verificar que los campos no estén vacíos
        if str_monto != '' and str_id_sucursal != '' and str_id_proveedor != '':
            # Verificar que el monto sea válido
            if self.verificar_Precios(str_monto):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_gasto(str_monto, str_id_sucursal, str_id_proveedor)
                print("Gasto insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_Monto_Gasto.clear()
                self.txt_Crear_ID_Sucursal_Gasto.clear()
                self.txt_Crear_ID_Proveedor_Gasto.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Gastos(self):
        str_id = self.txt_Modificar_Busqueda_ID_Gasto.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_gasto(str_id):
                if str_id.isdigit():
                    # Obtener los datos del gasto
                    gasto = self.registro_datos.busca_1_gasto(str_id)
                    # Desempaquetar los datos
                    id_gasto, monto, id_sucursal, id_proveedor = gasto[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Monto_Gasto.setDisabled(False)
                    self.txt_Modificar_ID_Sucursal_Gasto.setDisabled(False)
                    self.txt_Modificar_ID_Proveedor_Gasto.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Gasto.setText(str(id_gasto))
                    self.txt_Modificar_Monto_Gasto.setText(str(monto))
                    self.txt_Modificar_ID_Sucursal_Gasto.setText(str(id_sucursal))
                    self.txt_Modificar_ID_Proveedor_Gasto.setText(str(id_proveedor))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Gastos(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Gasto.text().strip()
        str_monto = self.txt_Modificar_Monto_Gasto.text().strip()
        str_id_sucursal = self.txt_Modificar_ID_Sucursal_Gasto.text().strip()
        str_id_proveedor = self.txt_Modificar_ID_Proveedor_Gasto.text().strip()

        if str_id != '' and str_monto != '' and str_id_sucursal != '' and str_id_proveedor != '':
            # Verificar que el monto sea válido
            if self.verificar_Precios(str_monto):
                # Insertar los datos en la base de datos
                self.registro_datos.actualiza_gasto(str_id, str_monto, str_id_sucursal, str_id_proveedor)
                print("Gasto actualizado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_Busqueda_ID_Gasto.clear()
                self.txt_Modificar_Monto_Gasto.clear()
                self.txt_Modificar_ID_Sucursal_Gasto.clear()
                self.txt_Modificar_ID_Proveedor_Gasto.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Gastos(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Gasto.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_gasto(str_id):
                if str_id.isdigit():
                    # Obtener los datos del gasto
                    gasto = self.registro_datos.busca_1_gasto(str_id)
                    # Desempaquetar los datos
                    id_gasto, monto, id_sucursal, id_proveedor = gasto[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Monto_Gasto.setDisabled(True)
                    self.txt_Eliminar_ID_Sucursal_Gasto.setDisabled(True)
                    self.txt_Eliminar_ID_Proveedor_Gasto.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Gasto.setText(str(id_gasto))
                    self.txt_Eliminar_Monto_Gasto.setText(str(monto))
                    self.txt_Eliminar_ID_Sucursal_Gasto.setText(str(id_sucursal))
                    self.txt_Eliminar_ID_Proveedor_Gasto.setText(str(id_proveedor))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Monto_Gasto.setReadOnly(True)
                    self.txt_Eliminar_ID_Sucursal_Gasto.setReadOnly(True)
                    self.txt_Eliminar_ID_Proveedor_Gasto.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Gastos(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Gasto.text().strip()
        str_monto = self.txt_Eliminar_Monto_Gasto.text().strip()
        str_id_sucursal = self.txt_Eliminar_ID_Sucursal_Gasto.text().strip()
        str_id_proveedor = self.txt_Eliminar_ID_Proveedor_Gasto.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_monto != '' and str_id_sucursal != '' and str_id_proveedor != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_gasto(str_id)
            print("Gasto eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Gasto.clear()
            self.txt_Eliminar_Monto_Gasto.clear()
            self.txt_Eliminar_ID_Sucursal_Gasto.clear()
            self.txt_Eliminar_ID_Proveedor_Gasto.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_InventarioSucursales(self):
        str_id = self.txt_Leer_Busqueda_ID_InvSuc.text().strip()
        if str_id != '':
            if str_id.isdigit():
                invID = int(str_id)
                inventario = self.registro_datos.busca_1_inventario_sucursal(invID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_InvSuc.clearContents()

                if inventario:
                    self.tblw_Leer_Tabla_InvSuc.setRowCount(1)
                    for col_idx, col_data in enumerate(inventario[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_InvSuc.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_InvSuc.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_InventarioSucursales(self):
        # Extraer los datos de la interfaz
        str_cantidad = self.txt_Crear_Cantidad_InvSuc.text().strip()
        str_id_sucursal = self.txt_Crear_ID_Sucursal_InvSuc.text().strip()
        str_id_producto = self.txt_Crear_ID_Producto_InvSuc.text().strip()

        # Verificar que los campos no estén vacíos
        if str_cantidad != '' and str_id_sucursal != '' and str_id_producto != '':
            # Verificar que la cantidad sea válida
            if self.verificar_Enteros(str_cantidad):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_inventario_sucursal(str_cantidad, str_id_sucursal, str_id_producto)
                print("Inventario insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_Cantidad_InvSuc.clear()
                self.txt_Crear_ID_Sucursal_InvSuc.clear()
                self.txt_Crear_ID_Producto_InvSuc.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_InventarioSucursales(self):
        str_id = self.txt_Modificar_ID_Inventario_InvSuc.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_inventario_sucursal(str_id):
                if str_id.isdigit():
                    # Obtener los datos del inventario
                    inventario = self.registro_datos.busca_1_inventario_sucursal(str_id)
                    # Desempaquetar los datos
                    id_inventario, cantidad, id_sucursal, id_producto = inventario[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Cantidad_InvSuc.setDisabled(False)
                    self.txt_Modificar_ID_Sucursal_InvSuc.setDisabled(False)
                    self.txt_Modificar_ID_Producto_InvSuc.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_ID_Inventario_InvSuc.setText(str(id_inventario))
                    self.txt_Modificar_Cantidad_InvSuc.setText(str(cantidad))
                    self.txt_Modificar_ID_Sucursal_InvSuc.setText(str(id_sucursal))
                    self.txt_Modificar_ID_Producto_InvSuc.setText(str(id_producto))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_InventarioSucursales(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_ID_Inventario_InvSuc.text().strip()
        str_cantidad = self.txt_Modificar_Cantidad_InvSuc.text().strip()
        str_id_sucursal = self.txt_Modificar_ID_Sucursal_InvSuc.text().strip()
        str_id_producto = self.txt_Modificar_ID_Producto_InvSuc.text().strip()

        if str_id != '' and str_cantidad != '' and str_id_sucursal != '' and str_id_producto != '':
            # Verificar que la cantidad sea válida
            if self.verificar_Enteros(str_cantidad):
                # Insertar los datos en la base de datos
                self.registro_datos.actualiza_inventario_sucursal(str_id, str_cantidad, str_id_sucursal, str_id_producto)
                print("Inventario actualizado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_ID_Inventario_InvSuc.clear()
                self.txt_Modificar_Cantidad_InvSuc.clear()
                self.txt_Modificar_ID_Sucursal_InvSuc.clear()
                self.txt_Modificar_ID_Producto_InvSuc.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_InventarioSucursales(self):
        str_id = self.txt_Eliminar_ID_Inventario_InvSuc.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_inventario_sucursal(str_id):
                if str_id.isdigit():
                    # Obtener los datos del inventario
                    inventario = self.registro_datos.busca_1_inventario_sucursal(str_id)
                    # Desempaquetar los datos
                    id_inventario, cantidad, id_sucursal, id_producto = inventario[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Cantidad_InvSuc.setDisabled(True)
                    self.txt_Eliminar_ID_Sucursal_InvSuc.setDisabled(True)
                    self.txt_Eliminar_ID_Producto_InvSuc.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_ID_Inventario_InvSuc.setText(str(id_inventario))
                    self.txt_Eliminar_Cantidad_InvSuc.setText(str(cantidad))
                    self.txt_Eliminar_ID_Sucursal_InvSuc.setText(str(id_sucursal))
                    self.txt_Eliminar_ID_Producto_InvSuc.setText(str(id_producto))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Cantidad_InvSuc.setReadOnly(True)
                    self.txt_Eliminar_ID_Sucursal_InvSuc.setReadOnly(True)
                    self.txt_Eliminar_ID_Producto_InvSuc.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_InventarioSucursales(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_ID_Inventario_InvSuc.text().strip()
        str_cantidad = self.txt_Eliminar_Cantidad_InvSuc.text().strip()
        str_id_sucursal = self.txt_Eliminar_ID_Sucursal_InvSuc.text().strip()
        str_id_producto = self.txt_Eliminar_ID_Producto_InvSuc.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_cantidad != '' and str_id_sucursal != '' and str_id_producto != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_inventario_sucursal(str_id)
            print("Inventario eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_ID_Inventario_InvSuc.clear()
            self.txt_Eliminar_Cantidad_InvSuc.clear()
            self.txt_Eliminar_ID_Sucursal_InvSuc.clear()
            self.txt_Eliminar_ID_Producto_InvSuc.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def verificar_Enteros(self, cadena):
        try:
            int(cadena)
            return True
        except ValueError:
            return False

    def buscar_Personas(self):
        str_id = self.txt_Leer_Busqueda_ID_Persona.text().strip()
        if str_id != '':
            if str_id.isdigit():
                personaID = int(str_id)
                persona = self.registro_datos.busca_1_persona(personaID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Persona.clearContents()

                if persona:
                    self.tblw_Leer_Tabla_Persona.setRowCount(1)
                    for col_idx, col_data in enumerate(persona[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Persona.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Persona.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Personas(self):
        # Extraer los datos de la interfaz
        nombre = self.txt_Crear_Nombre_Persona.text().strip()
        apellido_p = self.txt_Crear_Apellido_P_Persona.text().strip()
        apellido_m = self.txt_Crear_Apellido_M_Persona.text().strip()
        id_direccion = self.txt_Crear_ID_Direccion_Persona.text().strip()

        # Verificar que los campos no estén vacíos
        if nombre != '' and apellido_p != '' and apellido_m != '' and id_direccion != '':
            # Verificar que el ID de dirección sea válido
            if self.verificar_Enteros(id_direccion):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_persona(nombre, apellido_p, apellido_m, id_direccion)
                print("Persona insertada correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_Nombre_Persona.clear()
                self.txt_Crear_Apellido_P_Persona.clear()
                self.txt_Crear_Apellido_M_Persona.clear()
                self.txt_Crear_ID_Direccion_Persona.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Personas(self):
        str_id = self.txt_Modificar_Busqueda_ID_Persona.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_persona(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la persona
                    persona = self.registro_datos.busca_1_persona(str_id)
                    # Desempaquetar los datos
                    id_persona, nombre, apellido_p, apellido_m, id_direccion = persona[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Nombre_Persona.setDisabled(False)
                    self.txt_Modificar_Apellido_P_Persona.setDisabled(False)
                    self.txt_Modificar_Apellido_M_Persona.setDisabled(False)
                    self.txt_Modificar_ID_Direccion_Persona.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Persona.setText(str(id_persona))
                    self.txt_Modificar_Nombre_Persona.setText(str(nombre))
                    self.txt_Modificar_Apellido_P_Persona.setText(str(apellido_p))
                    self.txt_Modificar_Apellido_M_Persona.setText(str(apellido_m))
                    self.txt_Modificar_ID_Direccion_Persona.setText(str(id_direccion))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Personas(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Persona.text().strip()
        nombre = self.txt_Modificar_Nombre_Persona.text().strip()
        apellido_p = self.txt_Modificar_Apellido_P_Persona.text().strip()
        apellido_m = self.txt_Modificar_Apellido_M_Persona.text().strip()
        id_direccion = self.txt_Modificar_ID_Direccion_Persona.text().strip()

        if str_id != '' and nombre != '' and apellido_p != '' and apellido_m != '' and id_direccion != '':
            # Verificar que el ID de dirección sea válido
            if self.verificar_Enteros(id_direccion):
                # Actualizar los datos en la base de datos
                self.registro_datos.actualiza_persona(str_id, nombre, apellido_p, apellido_m, id_direccion)
                print("Persona actualizada correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_Busqueda_ID_Persona.clear()
                self.txt_Modificar_Nombre_Persona.clear()
                self.txt_Modificar_Apellido_P_Persona.clear()
                self.txt_Modificar_Apellido_M_Persona.clear()
                self.txt_Modificar_ID_Direccion_Persona.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Personas(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Persona.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_persona(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la persona
                    persona = self.registro_datos.busca_1_persona(str_id)
                    # Desempaquetar los datos
                    id_persona, nombre, apellido_p, apellido_m, id_direccion = persona[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Nombre_Persona.setDisabled(True)
                    self.txt_Eliminar_Apellido_P_Persona.setDisabled(True)
                    self.txt_Eliminar_Apellido_M_Persona.setDisabled(True)
                    self.txt_Eliminar_ID_Direccion_Persona.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Persona.setText(str(id_persona))
                    self.txt_Eliminar_Nombre_Persona.setText(str(nombre))
                    self.txt_Eliminar_Apellido_P_Persona.setText(str(apellido_p))
                    self.txt_Eliminar_Apellido_M_Persona.setText(str(apellido_m))
                    self.txt_Eliminar_ID_Direccion_Persona.setText(str(id_direccion))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Nombre_Persona.setReadOnly(True)
                    self.txt_Eliminar_Apellido_P_Persona.setReadOnly(True)
                    self.txt_Eliminar_Apellido_M_Persona.setReadOnly(True)
                    self.txt_Eliminar_ID_Direccion_Persona.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Personas(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Persona.text().strip()
        nombre = self.txt_Eliminar_Nombre_Persona.text().strip()
        apellido_p = self.txt_Eliminar_Apellido_P_Persona.text().strip()
        apellido_m = self.txt_Eliminar_Apellido_M_Persona.text().strip()
        id_direccion = self.txt_Eliminar_ID_Direccion_Persona.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and nombre != '' and apellido_p != '' and apellido_m != '' and id_direccion != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_persona(str_id)
            print("Persona eliminada correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Persona.clear()
            self.txt_Eliminar_Nombre_Persona.clear()
            self.txt_Eliminar_Apellido_P_Persona.clear()
            self.txt_Eliminar_Apellido_M_Persona.clear()
            self.txt_Eliminar_ID_Direccion_Persona.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)
    def verificar_Enteros(self, cadena):
        try:
            int(cadena)
            return True
        except ValueError:
            return False

    def buscar_Proveedores(self):
        str_id = self.txt_Leer_Busqueda_ID_Prov.text().strip()
        if str_id != '':
            if str_id.isdigit():
                proveedorID = int(str_id)
                proveedor = self.registro_datos.busca_1_proveedor(proveedorID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_Prov.clearContents()

                if proveedor:
                    self.tblw_Leer_Tabla_Prov.setRowCount(1)
                    for col_idx, col_data in enumerate(proveedor[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_Prov.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_Prov.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Proveedores(self):
        # Extraer los datos de la interfaz
        id_persona = self.txt_Crear_ID_Persona_Prov.text().strip()

        # Verificar que los campos no estén vacíos
        if id_persona != '':
            # Verificar que el ID de persona sea válido
            if self.verificar_Enteros(id_persona):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_proveedor(id_persona)
                print("Proveedor insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_ID_Persona_Prov.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Proveedores(self):
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_proveedor(str_id):
                if str_id.isdigit():
                    # Obtener los datos del proveedor
                    proveedor = self.registro_datos.busca_1_proveedor(str_id)
                    # Desempaquetar los datos
                    id_proveedor, id_persona = proveedor[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Persona_Proveedor.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Proveedor.setText(str(id_proveedor))
                    self.txt_Modificar_ID_Persona_Proveedor.setText(str(id_persona))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Proveedores(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        id_persona = self.txt_Modificar_ID_Persona_Proveedor.text().strip()

        if str_id != '' and id_persona != '':
            # Verificar que el ID de persona sea válido
            if self.verificar_Enteros(id_persona):
                # Actualizar los datos en la base de datos
                self.registro_datos.actualiza_proveedor(str_id, id_persona)
                print("Proveedor actualizado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_Busqueda_ID_Proveedor.clear()
                self.txt_Modificar_ID_Persona_Proveedor.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Proveedores(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_proveedor(str_id):
                if str_id.isdigit():
                    # Obtener los datos del proveedor
                    proveedor = self.registro_datos.busca_1_proveedor(str_id)
                    # Desempaquetar los datos
                    id_proveedor, id_persona = proveedor[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_ID_Persona_Proveedor.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Proveedor.setText(str(id_proveedor))
                    self.txt_Eliminar_ID_Persona_Proveedor.setText(str(id_persona))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_ID_Persona_Proveedor.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Proveedores(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        id_persona = self.txt_Eliminar_ID_Persona_Proveedor.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and id_persona != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_proveedor(str_id)
            print("Proveedor eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Proveedor.clear()
            self.txt_Eliminar_ID_Persona_Proveedor.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def verificar_Enteros(self, cadena):
        try:
            int(cadena)
            return True
        except ValueError:
            return False

    def buscar_Sucursales(self):
        str_id = self.txt_Leer_Busqueda_ID_LocSuc.text().strip()
        if str_id != '':
            if str_id.isdigit():
                sucursalID = int(str_id)
                sucursal = self.registro_datos.busca_1_sucursal(sucursalID)

                # Limpiar los datos anteriores de la tabla
                self.tblw_Leer_Tabla_LocSuc.clearContents()

                if sucursal:
                    self.tblw_Leer_Tabla_LocSuc.setRowCount(1)
                    for col_idx, col_data in enumerate(sucursal[0]):
                        item = QTableWidgetItem(str(col_data))
                        self.tblw_Leer_Tabla_LocSuc.setItem(0, col_idx, item)
                else:
                    self.tblw_Leer_Tabla_LocSuc.setRowCount(0)
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Sucursales(self):
        # Extraer los datos de la interfaz
        nombre = self.txt_Crear_Nombre_LocSuc.text().strip()
        id_direccion = self.txt_Crear_ID_Direccion_LocSuc.text().strip()

        # Verificar que los campos no estén vacíos
        if nombre != '' and id_direccion != '':
            # Verificar que el ID de dirección sea válido
            if self.verificar_Enteros(id_direccion):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_sucursal(nombre, id_direccion)
                print("Sucursal insertada correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Crear_Nombre_LocSuc.clear()
                self.txt_Crear_ID_Direccion_LocSuc.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar ventana de bienvenida
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Sucursales(self):
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_sucursal(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la sucursal
                    sucursal = self.registro_datos.busca_1_sucursal(str_id)
                    # Desempaquetar los datos
                    id_sucursal, nombre, id_direccion = sucursal[0]
                    # Habilitar Widgets
                    self.txt_Modificar_Nombre_LocSuc.setDisabled(False)
                    self.txt_Modificar_ID_Direccion_LocSuc.setDisabled(False)
                    # Poner los datos en los campos de entrada de texto
                    self.txt_Modificar_Busqueda_ID_Proveedor.setText(str(id_sucursal))
                    self.txt_Modificar_Nombre_LocSuc.setText(str(nombre))
                    self.txt_Modificar_ID_Direccion_LocSuc.setText(str(id_direccion))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def actualizar_Sucursales(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Proveedor.text().strip()
        nombre = self.txt_Modificar_Nombre_LocSuc.text().strip()
        id_direccion = self.txt_Modificar_ID_Direccion_LocSuc.text().strip()

        if str_id != '' and nombre != '' and id_direccion != '':
            # Verificar que el ID de dirección sea válido
            if self.verificar_Enteros(id_direccion):
                # Actualizar los datos en la base de datos
                self.registro_datos.actualiza_sucursal(str_id, nombre, id_direccion)
                print("Sucursal actualizada correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_Busqueda_ID_Proveedor.clear()
                self.txt_Modificar_Nombre_LocSuc.clear()
                self.txt_Modificar_ID_Direccion_LocSuc.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Sucursales(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_sucursal(str_id):
                if str_id.isdigit():
                    # Obtener los datos de la sucursal
                    sucursal = self.registro_datos.busca_1_sucursal(str_id)
                    # Desempaquetar los datos
                    id_sucursal, nombre, id_direccion = sucursal[0]
                    # Habilitar Widgets
                    self.txt_Eliminar_Nombre_LocSuc.setDisabled(True)
                    self.txt_Eliminar_ID_Direccion_LocSuc.setDisabled(True)
                    # Poner los datos en los campos de entrada de texto en modo de solo lectura
                    self.txt_Eliminar_Busqueda_ID_Proveedor.setText(str(id_sucursal))
                    self.txt_Eliminar_Nombre_LocSuc.setText(str(nombre))
                    self.txt_Eliminar_ID_Direccion_LocSuc.setText(str(id_direccion))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Nombre_LocSuc.setReadOnly(True)
                    self.txt_Eliminar_ID_Direccion_LocSuc.setReadOnly(True)
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def eliminar_Sucursales(self):
        # Extraer los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Proveedor.text().strip()
        nombre = self.txt_Eliminar_Nombre_LocSuc.text().strip()
        id_direccion = self.txt_Eliminar_ID_Direccion_LocSuc.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and nombre != '' and id_direccion != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_sucursal(str_id)
            print("Sucursal eliminada correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Proveedor.clear()
            self.txt_Eliminar_Nombre_LocSuc.clear()
            self.txt_Eliminar_ID_Direccion_LocSuc.clear()
        else:
            # Mostrar Ventana De Bienvenida
            self.seleccion_MessageBox(1)

    def verificar_Fecha(self, fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def buscar_TicketsCompras(self):
        str_id = self.txt_Leer_Busqueda_ID_Tickets.text().strip()
        if str_id != '':
            # Realizar la búsqueda del ticket de compra
            ticket = self.registro_datos.busca_1_ticket_compra(str_id)
            
            # Limpiar los datos anteriores de la tabla
            self.tblw_Leer_Tabla_Tickets.clearContents()
            
            if ticket:
                # Mostrar el ticket en la tabla
                self.tblw_Leer_Tabla_Tickets.setRowCount(1)
                for col_idx, col_data in enumerate(ticket[0]):
                    item = QTableWidgetItem(str(col_data))
                    self.tblw_Leer_Tabla_Tickets.setItem(0, col_idx, item)
            else:
                self.tblw_Leer_Tabla_Tickets.setRowCount(0)
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_TicketsCompras(self):
        # Obtener los datos de la interfaz
        str_fecha = self.de_Crear_Fecha_Ticket_Ticket.text().strip()
        detalles = self.txt_Crear_Detalles_Ticket.text().strip()
        id_proveedor = self.txt_Crear_ID_Proveedor_Ticket.text().strip()
        
        # Verificar que los campos no estén vacíos
        if str_fecha != '' and detalles != '' and id_proveedor != '':
            # Verificar el formato de la fecha
            if self.verificar_Fecha(str_fecha):
                # Insertar los datos en la base de datos
                self.registro_datos.inserta_ticket_compra(str_fecha, detalles, id_proveedor)
                print("Ticket de compra insertado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.de_Crear_Fecha_Ticket_Ticket.clear()
                self.txt_Crear_Detalles_Ticket.clear()
                self.txt_Crear_ID_Proveedor_Ticket.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_TicketsCompras(self):
        str_id = self.txt_Modificar_Busqueda_ID_Ticket.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_compra(str_id):
                # Obtener los datos del ticket de compra
                ticket = self.registro_datos.busca_1_ticket_compra(str_id)
                
                if ticket:
                    id_ticket, fecha, detalles, id_proveedor = ticket[0]
                    # Habilitar Widgets
                    self.de_Modificar_Fecha_Ticket_Ticket.setDisabled(False)
                    self.txt_Modificar_Detalles_Ticket.setDisabled(False)
                    self.txt_Modificar_ID_Proveedor_Ticket.setDisabled(False)
                    # Mostrar datos en los campos
                    self.txt_Modificar_Busqueda_ID_Ticket.setText(str(id_ticket))
                    self.de_Modificar_Fecha_Ticket_Ticket.setDate(QDate.fromString(fecha, 'yyyy-MM-dd'))
                    self.txt_Modificar_Detalles_Ticket.setText(detalles)
                    self.txt_Modificar_ID_Proveedor_Ticket.setText(str(id_proveedor))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def actualizar_TicketsCompras(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Ticket.text().strip()
        str_fecha = self.de_Modificar_Fecha_Ticket_Ticket.text().strip()
        detalles = self.txt_Modificar_Detalles_Ticket.text().strip()
        id_proveedor = self.txt_Modificar_ID_Proveedor_Ticket.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_fecha != '' and detalles != '' and id_proveedor != '':
            # Verificar el formato de la fecha
            if self.verificar_Fecha(str_fecha):
                # Actualizar los datos en la base de datos
                self.registro_datos.actualiza_ticket_compra(str_id, str_fecha, detalles, id_proveedor)
                print("Ticket de compra actualizado correctamente en la base de datos.")
                # Limpiar los campos de entrada de texto
                self.txt_Modificar_Busqueda_ID_Ticket.clear()
                self.de_Modificar_Fecha_Ticket_Ticket.clear()
                self.txt_Modificar_Detalles_Ticket.clear()
                self.txt_Modificar_ID_Proveedor_Ticket.clear()
            else:
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(1)

    def buscar_eliminar_TicketsCompras(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Ticket.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_compra(str_id):
                ticket = self.registro_datos.busca_1_ticket_compra(str_id)
                if ticket:
                    id_ticket, fecha, detalles, id_proveedor = ticket[0]
                    # Habilitar Widgets
                    self.de_Eliminar_Fecha_Ticket_Ticket.setDisabled(True)
                    self.txt_Eliminar_Detalles_Ticket.setDisabled(True)
                    self.txt_Eliminar_ID_Proveedor_Ticket.setDisabled(True)
                    # Mostrar datos en los campos
                    self.txt_Eliminar_Busqueda_ID_Ticket.setText(str(id_ticket))
                    self.de_Eliminar_Fecha_Ticket_Ticket.setDate(QDate.fromString(fecha, 'yyyy-MM-dd'))
                    self.txt_Eliminar_Detalles_Ticket.setText(detalles)
                    self.txt_Eliminar_ID_Proveedor_Ticket.setText(str(id_proveedor))
                    # Poner los campos de entrada de texto en solo lectura
                    self.txt_Eliminar_Detalles_Ticket.setReadOnly(True)
                    self.txt_Eliminar_ID_Proveedor_Ticket.setReadOnly(True)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def eliminar_TicketsCompras(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Ticket.text().strip()
        str_fecha = self.de_Eliminar_Fecha_Ticket_Ticket.text().strip()
        detalles = self.txt_Eliminar_Detalles_Ticket.text().strip()
        id_proveedor = self.txt_Eliminar_ID_Proveedor_Ticket.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and str_fecha != '' and detalles != '' and id_proveedor != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_ticket_compra(str_id)
            print("Ticket de compra eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt

    def verificar_Fecha(self, fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def buscar_Ventas(self):
        str_id = self.txt_Leer_Busqueda_ID_Ventas.text().strip()
        if str_id != '':
            # Realizar la búsqueda del ticket de venta
            ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
            
            # Limpiar los datos anteriores de la tabla
            self.tblw_Leer_Tabla_Ventas.clearContents()
            
            if ticket_venta:
                # Mostrar el ticket de venta en la tabla
                self.tblw_Leer_Tabla_Ventas.setRowCount(1)
                for col_idx, col_data in enumerate(ticket_venta[0]):
                    item = QTableWidgetItem(str(col_data))
                    self.tblw_Leer_Tabla_Ventas.setItem(0, col_idx, item)
            else:
                self.tblw_Leer_Tabla_Ventas.setRowCount(0)
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Ventas(self):
        # Obtener los datos de la interfaz
        id_sucursal = self.txt_Crear_ID_Sucursal_Venta.text().strip()
        id_cliente = self.txt_Crear_ID_Cliente_Venta.text().strip()
        
        # Verificar que los campos no estén vacíos
        if id_sucursal != '' and id_cliente != '':
            # Insertar los datos en la base de datos
            self.registro_datos.inserta_ticket_venta(id_sucursal, id_cliente)
            print("Ticket de venta insertado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Crear_ID_Sucursal_Venta.clear()
            self.txt_Crear_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Ventas(self):
        str_id = self.txt_Modificar_Busqueda_ID_Venta.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_venta(str_id):
                # Obtener los datos del ticket de venta
                ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
                
                if ticket_venta:
                    id_ticket_venta, id_sucursal, id_cliente = ticket_venta[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Sucursal_Venta.setDisabled(False)
                    self.txt_Modificar_ID_Cliente_Venta.setDisabled(False)
                    # Mostrar datos en los campos
                    self.txt_Modificar_Busqueda_ID_Venta.setText(str(id_ticket_venta))
                    self.txt_Modificar_ID_Sucursal_Venta.setText(str(id_sucursal))
                    self.txt_Modificar_ID_Cliente_Venta.setText(str(id_cliente))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def actualizar_Ventas(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Venta.text().strip()
        id_sucursal = self.txt_Modificar_ID_Sucursal_Venta.text().strip()
        id_cliente = self.txt_Modificar_ID_Cliente_Venta.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and id_sucursal != '' and id_cliente != '':
            # Actualizar los datos en la base de datos
            self.registro_datos.actualiza_ticket_venta(str_id, id_sucursal, id_cliente)
            print("Ticket de venta actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_Venta.clear()
            self.txt_Modificar_ID_Sucursal_Venta.clear()
            self.txt_Modificar_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Ventas(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Venta.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_venta(str_id):
                ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
                if ticket_venta:
                    id_ticket_venta, id_sucursal, id_cliente = ticket_venta[0]
                    # Mostrar datos en los campos
                    self.txt_Eliminar_Busqueda_ID_Venta.setText(str(id_ticket_venta))
                    self.txt_Eliminar_ID_Sucursal_Venta.setText(str(id_sucursal))
                    self.txt_Eliminar_ID_Cliente_Venta.setText(str(id_cliente))
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def eliminar_Ventas(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Venta.text().strip()

        # Verificar que el campo no esté vacío
        if str_id != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_ticket_venta(str_id)
            print("Ticket de venta eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Venta.clear()
            self.txt_Eliminar_ID_Sucursal_Venta.clear()
            self.txt_Eliminar_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def verificar_Fecha(self, fecha):
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def buscar_Ventas(self):
        str_id = self.txt_Leer_Busqueda_ID_Ventas.text().strip()
        if str_id != '':
            # Realizar la búsqueda del ticket de venta
            ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
            
            # Limpiar los datos anteriores de la tabla
            self.tblw_Leer_Tabla_Ventas.clearContents()
            
            if ticket_venta:
                # Mostrar el ticket de venta en la tabla
                self.tblw_Leer_Tabla_Ventas.setRowCount(1)
                for col_idx, col_data in enumerate(ticket_venta[0]):
                    item = QTableWidgetItem(str(col_data))
                    self.tblw_Leer_Tabla_Ventas.setItem(0, col_idx, item)
            else:
                self.tblw_Leer_Tabla_Ventas.setRowCount(0)
                self.seleccion_MessageBox(2)
        else:
            self.seleccion_MessageBox(2)

    def crear_Ventas(self):
        # Obtener los datos de la interfaz
        id_sucursal = self.txt_Crear_ID_Sucursal_Venta.text().strip()
        id_cliente = self.txt_Crear_ID_Cliente_Venta.text().strip()
        
        # Verificar que los campos no estén vacíos
        if id_sucursal != '' and id_cliente != '':
            # Insertar los datos en la base de datos
            self.registro_datos.inserta_ticket_venta(id_sucursal, id_cliente)
            print("Ticket de venta insertado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Crear_ID_Sucursal_Venta.clear()
            self.txt_Crear_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def habilitar_actualizar_Ventas(self):
        str_id = self.txt_Modificar_Busqueda_ID_Venta.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_venta(str_id):
                # Obtener los datos del ticket de venta
                ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
                
                if ticket_venta:
                    id_ticket_venta, id_sucursal, id_cliente = ticket_venta[0]
                    # Habilitar Widgets
                    self.txt_Modificar_ID_Sucursal_Venta.setDisabled(False)
                    self.txt_Modificar_ID_Cliente_Venta.setDisabled(False)
                    # Mostrar datos en los campos
                    self.txt_Modificar_Busqueda_ID_Venta.setText(str(id_ticket_venta))
                    self.txt_Modificar_ID_Sucursal_Venta.setText(str(id_sucursal))
                    self.txt_Modificar_ID_Cliente_Venta.setText(str(id_cliente))
                else:
                    self.seleccion_MessageBox(2)
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def actualizar_Ventas(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Modificar_Busqueda_ID_Venta.text().strip()
        id_sucursal = self.txt_Modificar_ID_Sucursal_Venta.text().strip()
        id_cliente = self.txt_Modificar_ID_Cliente_Venta.text().strip()

        # Verificar que los campos no estén vacíos
        if str_id != '' and id_sucursal != '' and id_cliente != '':
            # Actualizar los datos en la base de datos
            self.registro_datos.actualiza_ticket_venta(str_id, id_sucursal, id_cliente)
            print("Ticket de venta actualizado correctamente en la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Modificar_Busqueda_ID_Venta.clear()
            self.txt_Modificar_ID_Sucursal_Venta.clear()
            self.txt_Modificar_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def buscar_eliminar_Ventas(self):
        str_id = self.txt_Eliminar_Busqueda_ID_Venta.text().strip()
        if str_id != '':
            if self.registro_datos.busca_1_ticket_venta(str_id):
                ticket_venta = self.registro_datos.busca_1_ticket_venta(str_id)
                if ticket_venta:
                    id_ticket_venta, id_sucursal, id_cliente = ticket_venta[0]
                    # Mostrar datos en los campos
                    self.txt_Eliminar_Busqueda_ID_Venta.setText(str(id_ticket_venta))
                    self.txt_Eliminar_ID_Sucursal_Venta.setText(str(id_sucursal))
                    self.txt_Eliminar_ID_Cliente_Venta.setText(str(id_cliente))
            else:
                self.seleccion_MessageBox(4)
        else:
            self.seleccion_MessageBox(1)

    def eliminar_Ventas(self):
        # Obtener los datos de la interfaz
        str_id = self.txt_Eliminar_Busqueda_ID_Venta.text().strip()

        # Verificar que el campo no esté vacío
        if str_id != '':
            # Eliminar los datos de la base de datos
            self.registro_datos.elimina_ticket_venta(str_id)
            print("Ticket de venta eliminado correctamente de la base de datos.")
            # Limpiar los campos de entrada de texto
            self.txt_Eliminar_Busqueda_ID_Venta.clear()
            self.txt_Eliminar_ID_Sucursal_Venta.clear()
            self.txt_Eliminar_ID_Cliente_Venta.clear()
        else:
            self.seleccion_MessageBox(1)

    def seleccion_Opcion_Menu_1(self, id):
        #Obtener Titulo De Texto
        self.str_TituloView = f'{self.lst_Menu_Nombres_1[id]}'
        
        #Pruebas De Print
        print(f'{self.str_TituloView}')
        
        # Ciclo En Paneles
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_Menu_1) + -1:
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_Menu_1[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
        else:
            #Cerrar Aplicacion
            self.close()
    
    def seleccion_Opcion_Menu_1(self, id):
        #Obtener Titulo De Texto
        self.str_TituloView = f'{self.lst_Menu_Nombres_1[id]}'
        
        #Pruebas De Print
        print(f'{self.str_TituloView}')
        
        # Ciclo En Paneles
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_Menu_1) + -1:
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_Menu_1[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
        else:
            #Cerrar Aplicacion
            self.close()
    
    def seleccion_Opcion_SubMenu_1_1(self, id):
        #Obtener Titulo De Texto
        self.str_SubtituloView = self.lst_SubMenu_Nombres_1_1[id]
        
        #Pruebas De Print
        print(f'{self.str_TituloView} >> {self.str_SubtituloView}')
        
        # Ocultar Panel Principal & Secundario
        self.lbl_Titulo_Menu.hide()
        self.frm_Ventana_Principal.hide()
        
        # Ciclo En Panel De Menu Principal
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        # Ciclo En Panel De SubMenu
        for frm_Panel_2 in self.lst_frm_Ventanas_SubMenu_1_1:
            # Oculta Todos Los Paneles
            frm_Panel_2.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_SubMenu_1_1):
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_SubMenu_1_1[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
    
    def seleccion_Opcion_SubMenu_1_2(self, id):
        #Obtener Titulo De Texto
        self.str_SubtituloView = self.lst_SubMenu_Nombres_1_2[id]
        
        #Pruebas De Print
        print(f'{self.str_TituloView} >> {self.str_SubtituloView}')
        
        # Ocultar Panel Principal & Secundario
        self.lbl_Titulo_Menu.hide()
        self.frm_Ventana_Principal.hide()
        
        # Ciclo En Panel De Menu Principal
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        # Ciclo En Panel De SubMenu
        for frm_Panel_2 in self.lst_frm_Ventanas_SubMenu_1_2:
            # Oculta Todos Los Paneles
            frm_Panel_2.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_SubMenu_1_2):
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_SubMenu_1_2[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
    
    def seleccion_Opcion_SubMenu_1_3(self, id):
        #Obtener Titulo De Texto
        self.str_SubtituloView = self.lst_SubMenu_Nombres_1_3[id]
        
        #Pruebas De Print
        print(f'{self.str_TituloView} >> {self.str_SubtituloView}')
        
        # Ocultar Panel Principal & Secundario
        self.lbl_Titulo_Menu.hide()
        self.frm_Ventana_Principal.hide()
        
        # Ciclo En Panel De Menu Principal
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        # Ciclo En Panel De SubMenu
        for frm_Panel_2 in self.lst_frm_Ventanas_SubMenu_1_3:
            # Oculta Todos Los Paneles
            frm_Panel_2.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_SubMenu_1_3):
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_SubMenu_1_3[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
    
    def seleccion_Opcion_SubMenu_1_4(self, id):
        #Obtener Titulo De Texto
        self.str_SubtituloView = self.lst_SubMenu_Nombres_1_4[id]
        
        #Pruebas De Print
        print(f'{self.str_TituloView} >> {self.str_SubtituloView}')
        
        # Ocultar Panel Principal & Secundario
        self.lbl_Titulo_Menu.hide()
        self.frm_Ventana_Principal.hide()
        
        # Ciclo En Panel De Menu Principal
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        # Ciclo En Panel De SubMenu
        for frm_Panel_2 in self.lst_frm_Ventanas_SubMenu_1_4:
            # Oculta Todos Los Paneles
            frm_Panel_2.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_SubMenu_1_4):
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_SubMenu_1_4[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
    
    def seleccion_Opcion_SubMenu_1_5(self, id):
        #Obtener Titulo De Texto
        self.str_SubtituloView = self.lst_SubMenu_Nombres_1_5[id]
        
        #Pruebas De Print
        print(f'{self.str_TituloView} >> {self.str_SubtituloView}')
        
        # Ocultar Panel Principal & Secundario
        self.lbl_Titulo_Menu.hide()
        self.frm_Ventana_Principal.hide()
        
        # Ciclo En Panel De Menu Principal
        for frm_Panel_1 in self.lst_frm_Ventanas_Menu_1:
            # Oculta Todos Los Paneles
            frm_Panel_1.hide()
        # Ciclo En Panel De SubMenu
        for frm_Panel_2 in self.lst_frm_Ventanas_SubMenu_1_5:
            # Oculta Todos Los Paneles
            frm_Panel_2.hide()
        
        # Si Cumple La Condicion
        if id < len(self.lst_frm_Ventanas_SubMenu_1_5):
            # Selecciona El Panel Con El ID
            frm_PanelActual = self.lst_frm_Ventanas_SubMenu_1_5[id]
            # Mostrar Panel Selecionado
            frm_PanelActual.show()
    
    def regresar_Menu_Principal(self):
        # Lista De Paneles
        lst_Ocultar_Paneles = [
            self.lst_frm_Ventanas_Menu_1,
            self.lst_frm_Ventanas_SubMenu_1_1,
            self.lst_frm_Ventanas_SubMenu_1_2,
            self.lst_frm_Ventanas_SubMenu_1_3,
            self.lst_frm_Ventanas_SubMenu_1_4,
            self.lst_frm_Ventanas_SubMenu_1_5
        ]

        # Ciclo Para 
        for paneles in lst_Ocultar_Paneles:
            for panel in paneles:
                panel.hide()
        # Mostrar Panel Principal
        self.lbl_Titulo_Menu.show()
        self.frm_Ventana_Principal.show()
    
    #Funcion De Contenido
    def contenido(self):
        #[Declaracion Previa]=========================================================================;
        #Para Titulo De Menu
        self.str_TituloView, self.str_SubtituloView = '', ''
        
        # Instanciar Widget
        self.frm_Ventana_Principal = QFrame(self)
        # Tamaño & Posicion De Widget
        self.frm_Ventana_Principal.setFixedSize(180, 440), self.frm_Ventana_Principal.move(20, 20)
        # Estilo De Widget
        self.frm_Ventana_Principal.setStyleSheet('''
            /* Fondo */
            background-color: rgb(175, 175, 175); /* Color De Fondo */
            border: 1px solid rgb(0, 0, 0); /* Color De Borde */
        ''')
        
        # Crear Lista De Botones
        self.lst_btn_Menu_1 = []
        self.lst_btn_SubMenu_1_1 = []
        self.lst_btn_SubMenu_1_2 = []
        self.lst_btn_SubMenu_1_3 = []
        self.lst_btn_SubMenu_1_4 = []
        self.lst_btn_SubMenu_1_5 = []
        # Crear Lista De Ventanas
        self.lst_frm_Ventanas_Menu_1 = []
        self.lst_frm_Ventanas_SubMenu_1_1 = []
        self.lst_frm_Ventanas_SubMenu_1_2 = []
        self.lst_frm_Ventanas_SubMenu_1_3 = []
        self.lst_frm_Ventanas_SubMenu_1_4 = []
        self.lst_frm_Ventanas_SubMenu_1_5 = []
        # Crear Lista De Pestañas
        self.lst_frm_Pestaña_1_1 = []
        self.lst_frm_Pestaña_1_2 = []
        self.lst_frm_Pestaña_1_3 = []
        self.lst_frm_Pestaña_1_4 = []
        self.lst_frm_Pestaña_1_5 = []
        #[Panel Principal]============================================================================;
        # Instanciar Widget
        self.lbl_Titulo_Menu = QLabel('Menu Principal', self)
        # Tamaño & Posicion De Widget
        self.lbl_Titulo_Menu.setFixedSize(614, 40), self.lbl_Titulo_Menu.move(220, 20)
        # Estilo De Widget
        self.lbl_Titulo_Menu.setStyleSheet('''
            /* Fondo */
            margin: 2px 2px; /* Margen De Letra */
            background-color: rgb(75, 175, 80); /* Color De Fondo */
            border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            /* Letra */
            color: rgb(255, 255, 255); /* Color De Letra */
            font-size: 11px; /* Tamaño De Letra */
            text-align: center; /* Alinear Texto */
        ''')
        
        # Instanciar Widget
        self.lbl_Descripcion_Menu = QLabel('Seleccione Una Opcion A\nModificar En La Base', self.frm_Ventana_Principal)
        # Tamaño & Posicion De Widget
        self.lbl_Descripcion_Menu.setFixedSize(178, 38), self.lbl_Descripcion_Menu.move(1, 1)
        # Estilo De Widget
        self.lbl_Descripcion_Menu.setStyleSheet('''
            /* Fondo */
            background-color: rgb(175, 175, 175); /* Color De Fondo */
            border: none; /* Sin Borde */
            /* Letra */
            margin: 2px 2px; /* Margen De Letra */
            color: rgb(0, 0, 0); /* Color De Letra */
            font-size: 11px; /* Tamaño De Letra */
            text-align: center; /* Alinear Texto */
        ''')
        
        # Lista De Botones / Paneles
        self.lst_Menu_Nombres_1 = [
            'Inventario',
            'Capital Humano',
            'Localizaciones',
            'Transacciones',
            'Reportes',
            'Salir'
        ]
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_Menu_Nombres_1):
            # Instanciar Widget
            self.btn_Menu = QPushButton(f'{nombre}', self.frm_Ventana_Principal)
            # Tamaño & Posicion De Widget
            self.btn_Menu.setFixedSize(150, 30), self.btn_Menu.move(15, 75 + (index * 60))
            # Estilo De Widget
            self.btn_Menu.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Menu.clicked.connect(lambda _, id = index: self.seleccion_Opcion_Menu_1(id))
            # Añadir A La Lista
            self.lst_btn_Menu_1.append(self.btn_Menu)
        
        for index, nombre in enumerate(self.lst_Menu_Nombres_1):
            # Instanciar Widget
            self.frm_Ventana_Secundaria = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_Secundaria.setFixedSize(614, 380), self.frm_Ventana_Secundaria.move(220, 80)
            # Estilo De Widget
            self.frm_Ventana_Secundaria.setStyleSheet('''
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            ''')
            # Esconder Widget
            self.frm_Ventana_Secundaria.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_Menu_1.append(self.frm_Ventana_Secundaria)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_Menu_Nombres_1):
            # Instanciar Widget
            self.lbl_Descripcion_SubMenu = QLabel(f'Seleccione Una Opcion De {nombre}', self.lst_frm_Ventanas_Menu_1[index])
            # Tamaño & Posicion De Widget
            self.lbl_Descripcion_SubMenu.setFixedSize(612, 38), self.lbl_Descripcion_SubMenu.move(1, 1)
            # Estilo De Widget
            self.lbl_Descripcion_SubMenu.setStyleSheet('''
                /* Fondo */
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: none; /* Sin Borde */
                /* Letra */
                margin: 2px 2px; /* Margen De Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
                text-align: center; /* Alinear Texto */
            ''')
        #[Panel Secundario_1_1]=======================================================================;
        # Lista De Botones / Paneles
        self.lst_SubMenu_Nombres_1_1 = [
            'Inventario Almacenes',
            'Inventario Sucursales',
            'Productos'
        ]
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_1):
            # Instanciar Widget
            self.btn_SubMenu_1_1 = QPushButton(f'{nombre}', self.lst_frm_Ventanas_Menu_1[0])
            # Tamaño & Posicion De Widget
            self.btn_SubMenu_1_1.setFixedSize(150, 30), self.btn_SubMenu_1_1.move(15, 70 + (index * 60))
            # Estilo De Widget
            self.btn_SubMenu_1_1.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_SubMenu_1_1.clicked.connect(lambda _, id = index: self.seleccion_Opcion_SubMenu_1_1(id))
            # Añadir A La Lista
            self.lst_btn_SubMenu_1_1.append(self.btn_SubMenu_1_1)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_1):
            # Instanciar Widget
            self.frm_Ventana_smbd_1_1 = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_smbd_1_1.setFixedSize(854, 480), self.frm_Ventana_smbd_1_1.move(0, 0)
            # Esconder Widget
            self.frm_Ventana_smbd_1_1.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_SubMenu_1_1.append(self.frm_Ventana_smbd_1_1)
        #[Panel Secundario_1_2]=======================================================================;
        # Lista De Botones / Paneles
        self.lst_SubMenu_Nombres_1_2 = [
            'Clientes',
            'Empleados',
            'Proovedores',
            'Acceso Empleados',
            'Persona'
        ]
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_2):
            # Instanciar Widget
            self.btn_SubMenu_1_2 = QPushButton(f'{nombre}', self.lst_frm_Ventanas_Menu_1[1])
            # Tamaño & Posicion De Widget
            self.btn_SubMenu_1_2.setFixedSize(150, 30), self.btn_SubMenu_1_2.move(15, 70 + (index * 60))
            # Estilo De Widget
            self.btn_SubMenu_1_2.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_SubMenu_1_2.clicked.connect(lambda _, id = index: self.seleccion_Opcion_SubMenu_1_2(id))
            # Añadir A La Lista
            self.lst_btn_SubMenu_1_2.append(self.btn_SubMenu_1_2)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_2):
            # Instanciar Widget
            self.frm_Ventana_smbd_1_2 = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_smbd_1_2.setFixedSize(854, 480), self.frm_Ventana_smbd_1_2.move(0, 0)
            # Esconder Widget
            self.frm_Ventana_smbd_1_2.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_SubMenu_1_2.append(self.frm_Ventana_smbd_1_2)
        #[Panel Secundario_1_3]=======================================================================;
        # Lista De Botones / Paneles
        self.lst_SubMenu_Nombres_1_3 = [
            'Almacenes',
            'Sucursales',
            'Direcciones'
        ]
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_3):
            # Instanciar Widget
            self.btn_SubMenu_1_3 = QPushButton(f'{nombre}', self.lst_frm_Ventanas_Menu_1[2])
            # Tamaño & Posicion De Widget
            self.btn_SubMenu_1_3.setFixedSize(150, 30), self.btn_SubMenu_1_3.move(15, 70 + (index * 60))
            # Estilo De Widget
            self.btn_SubMenu_1_3.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_SubMenu_1_3.clicked.connect(lambda _, id = index: self.seleccion_Opcion_SubMenu_1_3(id))
            # Añadir A La Lista
            self.lst_btn_SubMenu_1_3.append(self.btn_SubMenu_1_3)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_3):
            # Instanciar Widget
            self.frm_Ventana_smbd_1_3 = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_smbd_1_3.setFixedSize(854, 480), self.frm_Ventana_smbd_1_3.move(0, 0)
            # Esconder Widget
            self.frm_Ventana_smbd_1_3.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_SubMenu_1_3.append(self.frm_Ventana_smbd_1_3)
        #[Panel Secundario_1_4]=======================================================================;
        # Lista De Botones / Paneles
        self.lst_SubMenu_Nombres_1_4 = [
            'Gastos',
            'Ventas',
            'Ticket'
        ]
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_4):
            # Instanciar Widget
            self.btn_SubMenu_1_4 = QPushButton(f'{nombre}', self.lst_frm_Ventanas_Menu_1[3])
            # Tamaño & Posicion De Widget
            self.btn_SubMenu_1_4.setFixedSize(150, 30), self.btn_SubMenu_1_4.move(15, 70 + (index * 60))
            # Estilo De Widget
            self.btn_SubMenu_1_4.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_SubMenu_1_4.clicked.connect(lambda _, id = index: self.seleccion_Opcion_SubMenu_1_4(id))
            # Añadir A La Lista
            self.lst_btn_SubMenu_1_4.append(self.btn_SubMenu_1_4)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_4):
            # Instanciar Widget
            self.frm_Ventana_smbd_1_4 = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_smbd_1_4.setFixedSize(854, 480), self.frm_Ventana_smbd_1_4.move(0, 0)
            # Esconder Widget
            self.frm_Ventana_smbd_1_4.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_SubMenu_1_4.append(self.frm_Ventana_smbd_1_4)
        #[Panel Secundario_1_5]=======================================================================;
        # Lista De Botones / Paneles
        self.lst_SubMenu_Nombres_1_5 = [
            'Ventas por Sucursal',
            'Cambios De Precio',
            'Datos De Almacen',
            'Datos Del Cliente'
        ]
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_5):
            # Instanciar Widget
            self.btn_SubMenu_1_5 = QPushButton(f'{nombre}', self.lst_frm_Ventanas_Menu_1[4])
            # Tamaño & Posicion De Widget
            self.btn_SubMenu_1_5.setFixedSize(150, 30), self.btn_SubMenu_1_5.move(15, 70 + (index * 60))
            # Estilo De Widget
            self.btn_SubMenu_1_5.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 13px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_SubMenu_1_5.clicked.connect(lambda _, id = index: self.seleccion_Opcion_SubMenu_1_5(id))
            # Añadir A La Lista
            self.lst_btn_SubMenu_1_5.append(self.btn_SubMenu_1_5)
        
        # Ciclo Para Widget
        for index, nombre in enumerate(self.lst_SubMenu_Nombres_1_5):
            # Instanciar Widget
            self.frm_Ventana_smbd_1_5 = QFrame(self)
            # Tamaño & Posicion De Widget
            self.frm_Ventana_smbd_1_5.setFixedSize(854, 480), self.frm_Ventana_smbd_1_5.move(0, 0)
            # Esconder Widget
            self.frm_Ventana_smbd_1_5.hide()
            # Añadir A La Lista
            self.lst_frm_Ventanas_SubMenu_1_5.append(self.frm_Ventana_smbd_1_5)
        #[Lista Genral De Pestaña]====================================================================;
        # Lista De Pestaña De Nombres
        self.lst_Pestania_Nombres_1 = [
            'Leer',
            'Crear',
            'Modificar',
            'Eliminar'
        ]
        
        # Lista De Pestaña De Nombres
        self.lst_Pestania_Nombres_2 = [
            'Leer',
            'Crear'
        ]
        #[Crear TabWidget 1_1]========================================================================;
        #Ciclo Para Botón De Volver
        for i in range(len(self.lst_frm_Ventanas_SubMenu_1_1)):
            # Instanciar Widget
            self.lbl_Volver = QLabel(f'{self.lst_Menu_Nombres_1[0]} >> {self.lst_SubMenu_Nombres_1_1[i]}', self.lst_frm_Ventanas_SubMenu_1_1[i])
            # Posicion De Widget
            self.lbl_Volver.move(130, 10)
            
            # Instanciar Widget
            self.btn_Volver = QPushButton(f'Volver', self.lst_frm_Ventanas_SubMenu_1_1[i])
            # Tamaño & Posicion De Widget
            self.btn_Volver.setFixedSize(100, 20), self.btn_Volver.move(20, 10)
            # Estilo De Widget
            self.btn_Volver.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 11px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Volver.clicked.connect(self.regresar_Menu_Principal)
        
        # Instanciar Widget
        self.tbl_Crud_1_1 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_1[0])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_1.setFixedSize(814, 400), self.tbl_Crud_1_1.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_1.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_1.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_1.append(self.tbl_Crud_1_1)
        
        # Instanciar Widget
        self.tbl_Crud_1_1 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_1[1])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_1.setFixedSize(814, 400), self.tbl_Crud_1_1.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_1.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            
            QHeaderView::section {
                border: 1px solid #000000; /* Borde de los encabezados */
                font-size: 11pt; /* Tamaño De Texto */
                color: rgb(255, 255, 255); /* Color De Texto */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_1.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_1.append(self.tbl_Crud_1_1)
        
        # Instanciar Widget
        self.tbl_Crud_1_1 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_1[2])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_1.setFixedSize(814, 400), self.tbl_Crud_1_1.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_1.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_1.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_1.append(self.tbl_Crud_1_1)
        #[Crear TabWidget 1_2]========================================================================;
        #Ciclo Para Botón De Volver
        for i in range(len(self.lst_frm_Ventanas_SubMenu_1_2)):
            # Instanciar Widget
            self.lbl_Volver = QLabel(f'{self.lst_Menu_Nombres_1[1]} >> {self.lst_SubMenu_Nombres_1_2[i]}', self.lst_frm_Ventanas_SubMenu_1_2[i])
            # Posicion De Widget
            self.lbl_Volver.move(130, 10)
            
            # Instanciar Widget
            self.btn_Volver = QPushButton(f'Volver', self.lst_frm_Ventanas_SubMenu_1_2[i])
            # Tamaño & Posicion De Widget
            self.btn_Volver.setFixedSize(100, 20), self.btn_Volver.move(20, 10)
            # Estilo De Widget
            self.btn_Volver.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 11px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Volver.clicked.connect(self.regresar_Menu_Principal)
        
        # Instanciar Widget
        self.tbl_Crud_1_2 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_2[0])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_2.setFixedSize(814, 400), self.tbl_Crud_1_2.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_2.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_2.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_2.append(self.tbl_Crud_1_2)
        
        # Instanciar Widget
        self.tbl_Crud_1_2 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_2[1])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_2.setFixedSize(814, 400), self.tbl_Crud_1_2.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_2.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_2.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_2.append(self.tbl_Crud_1_2)
        
        # Instanciar Widget
        self.tbl_Crud_1_2 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_2[2])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_2.setFixedSize(814, 400), self.tbl_Crud_1_2.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_2.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_2.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_2.append(self.tbl_Crud_1_2)
        
        # Instanciar Widget
        self.tbl_Crud_1_2 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_2[3])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_2.setFixedSize(814, 400), self.tbl_Crud_1_2.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_2.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_2)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_2.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_2[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_2.append(self.tbl_Crud_1_2)
        
        # Instanciar Widget
        self.tbl_Crud_1_2 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_2[4])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_2.setFixedSize(814, 400), self.tbl_Crud_1_2.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_2.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_2.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_2.append(self.tbl_Crud_1_2)
        #[Crear TabWidget 1_3]========================================================================;
        #Ciclo Para Botón De Volver
        for i in range(len(self.lst_frm_Ventanas_SubMenu_1_3)):
            # Instanciar Widget
            self.lbl_Volver = QLabel(f'{self.lst_Menu_Nombres_1[2]} >> {self.lst_SubMenu_Nombres_1_3[i]}', self.lst_frm_Ventanas_SubMenu_1_3[i])
            # Posicion De Widget
            self.lbl_Volver.move(130, 10)
            
            # Instanciar Widget
            self.btn_Volver = QPushButton(f'Volver', self.lst_frm_Ventanas_SubMenu_1_3[i])
            # Tamaño & Posicion De Widget
            self.btn_Volver.setFixedSize(100, 20), self.btn_Volver.move(20, 10)
            # Estilo De Widget
            self.btn_Volver.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 11px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Volver.clicked.connect(self.regresar_Menu_Principal)
        
        # Instanciar Widget
        self.tbl_Crud_1_3 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_3[0])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_3.setFixedSize(814, 400), self.tbl_Crud_1_3.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_3.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_3.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_3.append(self.tbl_Crud_1_3)
        
        # Instanciar Widget
        self.tbl_Crud_1_3 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_3[1])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_3.setFixedSize(814, 400), self.tbl_Crud_1_3.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_3.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_3.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_3.append(self.tbl_Crud_1_3)
        
        # Instanciar Widget
        self.tbl_Crud_1_3 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_3[2])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_3.setFixedSize(814, 400), self.tbl_Crud_1_3.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_3.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_3.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_3.append(self.tbl_Crud_1_3)
        #[Crear TabWidget 1_4]========================================================================;
        #Ciclo Para Botón De Volver
        for i in range(len(self.lst_frm_Ventanas_SubMenu_1_4)):
            # Instanciar Widget
            self.lbl_Volver = QLabel(f'{self.lst_Menu_Nombres_1[3]} >> {self.lst_SubMenu_Nombres_1_4[i]}', self.lst_frm_Ventanas_SubMenu_1_4[i])
            # Posicion De Widget
            self.lbl_Volver.move(130, 10)
            
            # Instanciar Widget
            self.btn_Volver = QPushButton(f'Volver', self.lst_frm_Ventanas_SubMenu_1_4[i])
            # Tamaño & Posicion De Widget
            self.btn_Volver.setFixedSize(100, 20), self.btn_Volver.move(20, 10)
            # Estilo De Widget
            self.btn_Volver.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 11px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Volver.clicked.connect(self.regresar_Menu_Principal)
        
        # Instanciar Widget
        self.tbl_Crud_1_4 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_4[0])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_4.setFixedSize(814, 400), self.tbl_Crud_1_4.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_4.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_4.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_4.append(self.tbl_Crud_1_4)
        
        # Instanciar Widget
        self.tbl_Crud_1_4 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_4[1])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_4.setFixedSize(814, 400), self.tbl_Crud_1_4.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_4.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_4.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_4.append(self.tbl_Crud_1_4)
        
        # Instanciar Widget
        self.tbl_Crud_1_4 = QTabWidget(self.lst_frm_Ventanas_SubMenu_1_4[2])
        # Tamaño & Posicion De Widget
        self.tbl_Crud_1_4.setFixedSize(814, 400), self.tbl_Crud_1_4.move(20, 60)
        # Estilo De Widget
        self.tbl_Crud_1_4.setStyleSheet('''
            /* Fondo */
            QTabWidget::pane {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestañas */
            QTabBar::tab {
                width: ''' + str(805 / 4) + '''px; /* Ancho De La Pestaña */
                height: 20px; /* Alto De La Pestaña */
                font-size: 11px; /* Tamaño De Letra */
            }
            
            /* Pestaña Seleccionada */
            QTabBar::tab:selected {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña Seleccionadan't */
            QTabBar::tab:!selected {
                background-color: rgb(175, 175, 175); /* Color De Borde */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:hover {
                background-color: rgb(150, 225, 245); /* Color De Fondo */
            }
            
            /* Pestaña En Eleccion */
            QTabBar::tab:pressed {
                background-color: rgb(125, 200, 230); /* Color De Fondo */
                color: rgb(255, 255, 255); /* Color De Fondo */
            }
            
            /* Quitar Flecha */
            QTabBar::scroller {
                width: 0;
            }
        ''')
        # Ciclo Para Crear Pestañas Del TabWidget
        for index in range(len(self.lst_Pestania_Nombres_1)):
            # Crear Widget
            self.frm_Crud = QWidget()
            # Añadir Pestaña Con Nombres De La Lista
            self.tbl_Crud_1_4.addTab(self.frm_Crud, f'{self.lst_Pestania_Nombres_1[index]}')
        # Añadir TabWidget A Una Lista
        self.lst_frm_Pestaña_1_4.append(self.tbl_Crud_1_4)
        #[Crear TabWidget 1_5]========================================================================;
        #Ciclo Para Botón De Volver
        for i in range(len(self.lst_frm_Ventanas_SubMenu_1_5)):
            # Instanciar Widget
            self.lbl_Volver = QLabel(f'{self.lst_Menu_Nombres_1[4]} >> {self.lst_SubMenu_Nombres_1_5[i]}', self.lst_frm_Ventanas_SubMenu_1_5[i])
            # Posicion De Widget
            self.lbl_Volver.move(130, 10)
            
            # Instanciar Widget
            self.btn_Volver = QPushButton(f'Volver', self.lst_frm_Ventanas_SubMenu_1_5[i])
            # Tamaño & Posicion De Widget
            self.btn_Volver.setFixedSize(100, 20), self.btn_Volver.move(20, 10)
            # Estilo De Widget
            self.btn_Volver.setStyleSheet('''
                QPushButton {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(255, 255, 255); /* Color De Letra */
                    font-size: 11px; /* Tamaño De Letra */
                }
                QPushButton:hover {
                    /* Fondo */
                    background-color: rgb(255, 255, 255); /* Color De Fondo */
                    border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                    /* Letra */
                    color: rgb(75, 175, 80); /* Color De Letra */
                }
                QPushButton:pressed {
                    /* Fondo */
                    background-color: rgb(75, 175, 80); /* Color De Fondo */
                    border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                    /* Letra */
                    color: rgb(0, 0, 0); /* Color De Letra */
                }
            ''')
            # Accion De Clickear Widget
            self.btn_Volver.clicked.connect(self.regresar_Menu_Principal)
        #[Panel_1-SubPanel_1-Pestania_1]==============================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_InvAlm = QLabel('Visualizar Tabla Del Inventario De Almacenes', self.lst_frm_Pestaña_1_1[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_InvAlm.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_InvAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_InvAlm.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_InvAlm.setPlaceholderText('Ingrese ID (ejemplo: 35)')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_InvAlm.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_InvAlm.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_InvAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[0].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_InvAlm.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_InvAlm.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_InvAlm.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_InvAlm_Nombres = [
            'Inventario ID',
            'Cantidad',
            'Almacen ID',
            'Producto ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_InvAlm = QTableWidget(self.lst_frm_Pestaña_1_1[0].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_InvAlm.setFixedSize(764, 300), self.tblw_Leer_Tabla_InvAlm.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_InvAlm.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_InvAlm.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_InvAlm.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_inventario_almacenes()
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_InvAlm.setColumnCount(len(self.lst_Leer_Tabla_InvAlm_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_InvAlm.setHorizontalHeaderLabels(self.lst_Leer_Tabla_InvAlm_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_InvAlm.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_InvAlm.verticalHeader().setVisible(False)
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_InvAlm.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_InvAlm.setItem(row_idx, col_idx, item)
        #[Panel_1-SubPanel_1-Pestania_2]==============================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_InvAlm = QLabel('Crear Inventario De Almacen',self.lst_frm_Pestaña_1_1[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_InvAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Cantidad_InvAlm = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Cantidad_InvAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Cantidad_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Cantidad_InvAlm.setPlaceholderText('Ingrese Cantidad')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Cantidad_InvAlm.setFixedSize(350, 20), self.txt_Crear_Cantidad_InvAlm.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Almacen_InvAlm = QLabel('ID Del Almacen',self.lst_frm_Pestaña_1_1[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Almacen_InvAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Almacen_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Almacen_InvAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Almacen_InvAlm.setFixedSize(350, 20), self.txt_Crear_ID_Almacen_InvAlm.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Producto_InvAlm = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Producto_InvAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_ID_Producto_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Producto_InvAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Producto_InvAlm.setFixedSize(350, 20), self.txt_Crear_ID_Producto_InvAlm.move(300, 160)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_InvAlm = QPushButton('Crear', self.lst_frm_Pestaña_1_1[0].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_InvAlm.setFixedSize(150, 20), self.btn_Crear_Aniadir_InvAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_InvAlm.clicked.connect(self.obtener_Datos_InvAlm_1_1_1)
        #[Panel_1-SubPanel_1-Pestania_3]==============================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_InvAlm = QLabel('Modificar Inventario De Almacen',self.lst_frm_Pestaña_1_1[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_InvAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Inventario_InvAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Inventario_InvAlm.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Inventario_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_ID_Inventario_InvAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Inventario_InvAlm.setFixedSize(190, 20), self.txt_Modificar_ID_Inventario_InvAlm.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_ID_Inventario_InvAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_ID_Inventario_InvAlm.setFixedSize(150, 20), self.btn_Modificar_ID_Inventario_InvAlm.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_ID_Inventario_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_ID_Inventario_InvAlm.clicked.connect(self.buscar_Datos_Producto_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Cantidad_InvAlm = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Cantidad_InvAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Cantidad_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Cantidad_InvAlm.setFixedSize(350, 20), self.txt_Modificar_Cantidad_InvAlm.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Cantidad_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Almacen_InvAlm = QLabel('ID Del Almacen',self.lst_frm_Pestaña_1_1[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Almacen_InvAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Almacen_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Almacen_InvAlm.setFixedSize(350, 20), self.txt_Modificar_ID_Almacen_InvAlm.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Almacen_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Producto_InvAlm = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Producto_InvAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Producto_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Producto_InvAlm.setFixedSize(350, 20), self.txt_Modificar_ID_Producto_InvAlm.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Producto_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_InvAlm = QPushButton('Modificar', self.lst_frm_Pestaña_1_1[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_InvAlm.setFixedSize(150, 20), self.btn_Modificar_Aniadir_InvAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_InvAlm.clicked.connect(self.obtener_Datos_InvAlm_1_1_1)
        #[Panel_1-SubPanel_1-Pestania_4]==============================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_InvAlm = QLabel('Eliminar Inventario De Almacen',self.lst_frm_Pestaña_1_1[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_InvAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Inventario_InvAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Inventario_InvAlm.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Inventario_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_ID_Inventario_InvAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Inventario_InvAlm.setFixedSize(190, 20), self.txt_Eliminar_ID_Inventario_InvAlm.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_ID_Inventario_InvAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_ID_Inventario_InvAlm.setFixedSize(150, 20), self.btn_Eliminar_ID_Inventario_InvAlm.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_ID_Inventario_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_ID_Inventario_InvAlm.clicked.connect(self.buscar_Datos_Producto_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Cantidad_InvAlm = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Cantidad_InvAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Cantidad_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Cantidad_InvAlm.setFixedSize(350, 20), self.txt_Eliminar_Cantidad_InvAlm.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Cantidad_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Almacen_InvAlm = QLabel('ID Del Almacen',self.lst_frm_Pestaña_1_1[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Almacen_InvAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Almacen_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Almacen_InvAlm.setFixedSize(350, 20), self.txt_Eliminar_ID_Almacen_InvAlm.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Almacen_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Producto_InvAlm = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Producto_InvAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Producto_InvAlm = QLineEdit(self.lst_frm_Pestaña_1_1[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Producto_InvAlm.setFixedSize(350, 20), self.txt_Eliminar_ID_Producto_InvAlm.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Producto_InvAlm.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_InvAlm = QPushButton('Eliminar', self.lst_frm_Pestaña_1_1[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_InvAlm.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_InvAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_InvAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_InvAlm.clicked.connect(self.obtener_Datos_InvAlm_1_1_1)
        #[Panel_1-SubPanel_2-Pestania_1]==============================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_InvSuc = QLabel('Visualizar Tabla Del Inventario De Sucursales', self.lst_frm_Pestaña_1_1[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_InvSuc.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_InvSuc = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_InvSuc.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_InvSuc.setPlaceholderText('Ingrese ID (ejemplo: 35)')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_InvSuc.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_InvSuc.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_InvSuc = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[1].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_InvSuc.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_InvSuc.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_InvSuc.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_InvSuc_Nombres = [
            'Inventario ID',
            'Cantidad',
            'Sucursal ID',
            'Producto ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_InvSuc = QTableWidget(self.lst_frm_Pestaña_1_1[1].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_InvSuc.setFixedSize(764, 300), self.tblw_Leer_Tabla_InvSuc.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_InvSuc.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_InvSuc.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_InvSuc.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_InvSuc.setColumnCount(len(self.lst_Leer_Tabla_InvSuc_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_InvSuc.setHorizontalHeaderLabels(self.lst_Leer_Tabla_InvSuc_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_InvSuc.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_InvSuc.verticalHeader().setVisible(False)
        
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_inventario_sucursales()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_InvSuc.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_InvSuc.setItem(row_idx, col_idx, item)
        #[Panel_1-SubPanel_2-Pestania_2]==============================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_InvSuc = QLabel('Crear Inventario De Sucursal',self.lst_frm_Pestaña_1_1[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_InvSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Cantidad_InvSuc = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Cantidad_InvSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Cantidad_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Cantidad_InvSuc.setPlaceholderText('Ingrese Cantidad')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Cantidad_InvSuc.setFixedSize(350, 20), self.txt_Crear_Cantidad_InvSuc.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Sucursal_InvSuc = QLabel('ID De La Sucursal',self.lst_frm_Pestaña_1_1[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Sucursal_InvSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Sucursal_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Sucursal_InvSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Sucursal_InvSuc.setFixedSize(350, 20), self.txt_Crear_ID_Sucursal_InvSuc.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Producto_InvSuc = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Producto_InvSuc.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_ID_Producto_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Producto_InvSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Producto_InvSuc.setFixedSize(350, 20), self.txt_Crear_ID_Producto_InvSuc.move(300, 160)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_InvSuc = QPushButton('Crear', self.lst_frm_Pestaña_1_1[1].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_InvSuc.setFixedSize(150, 20), self.btn_Crear_Aniadir_InvSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_InvSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[Panel_1-SubPanel_2-Pestania_3]==============================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_InvSuc = QLabel('Modificar Inventario De Sucursal',self.lst_frm_Pestaña_1_1[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_InvSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Inventario_InvSuc = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Inventario_InvSuc.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Inventario_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_ID_Inventario_InvSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Inventario_InvSuc.setFixedSize(190, 20), self.txt_Modificar_ID_Inventario_InvSuc.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_ID_Inventario_InvSuc = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_ID_Inventario_InvSuc.setFixedSize(150, 20), self.btn_Modificar_ID_Inventario_InvSuc.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_ID_Inventario_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_ID_Inventario_InvSuc.clicked.connect(self.buscar_Datos_Producto_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Cantidad_InvSuc = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Cantidad_InvSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Cantidad_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Cantidad_InvSuc.setFixedSize(350, 20), self.txt_Modificar_Cantidad_InvSuc.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Cantidad_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Sucursal_InvSuc = QLabel('ID De La Sucursal',self.lst_frm_Pestaña_1_1[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Sucursal_InvSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Sucursal_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Sucursal_InvSuc.setFixedSize(350, 20), self.txt_Modificar_ID_Sucursal_InvSuc.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Sucursal_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Producto_InvSuc = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Producto_InvSuc.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Producto_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Producto_InvSuc.setFixedSize(350, 20), self.txt_Modificar_ID_Producto_InvSuc.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Producto_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_InvSuc = QPushButton('Modificar', self.lst_frm_Pestaña_1_1[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_InvSuc.setFixedSize(150, 20), self.btn_Modificar_Aniadir_InvSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_InvSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[Panel_1-SubPanel_2-Pestania_4]==============================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_InvSuc = QLabel('Eliminar Inventario De Sucursal',self.lst_frm_Pestaña_1_1[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_InvSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Inventario_InvSuc = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Inventario_InvSuc.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Inventario_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_ID_Inventario_InvSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Inventario_InvSuc.setFixedSize(190, 20), self.txt_Eliminar_ID_Inventario_InvSuc.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_ID_Inventario_InvSuc = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_ID_Inventario_InvSuc.setFixedSize(150, 20), self.btn_Eliminar_ID_Inventario_InvSuc.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_ID_Inventario_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_ID_Inventario_InvSuc.clicked.connect(self.buscar_Datos_Producto_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Cantidad_InvSuc = QLabel('Cantidad',self.lst_frm_Pestaña_1_1[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Cantidad_InvSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Cantidad_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Cantidad_InvSuc.setFixedSize(350, 20), self.txt_Eliminar_Cantidad_InvSuc.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Cantidad_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Sucursal_InvSuc = QLabel('ID De La Sucursal',self.lst_frm_Pestaña_1_1[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Sucursal_InvSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Sucursal_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Sucursal_InvSuc.setFixedSize(350, 20), self.txt_Eliminar_ID_Sucursal_InvSuc.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Sucursal_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Producto_InvSuc = QLabel('ID Del Producto',self.lst_frm_Pestaña_1_1[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Producto_InvSuc.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Producto_InvSuc = QLineEdit(self.lst_frm_Pestaña_1_1[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Producto_InvSuc.setFixedSize(350, 20), self.txt_Eliminar_ID_Producto_InvSuc.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Producto_InvSuc.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_InvSuc = QPushButton('Eliminar', self.lst_frm_Pestaña_1_1[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_InvSuc.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_InvSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_InvSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_InvSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[Panel_1-SubPanel_3-Pestania_1]==============================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Producto = QLabel('Visualizar Tabla De Productos', self.lst_frm_Pestaña_1_1[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Producto.move(20, 10)

        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Producto = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Producto.move(20, 30)

        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Producto.setPlaceholderText('Ingrese ID (ejemplo: 35)')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Producto.setFixedSize(150, 20)
        self.txt_Leer_Busqueda_ID_Producto.move(110, 30)

        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Producto = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[2].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Producto.setFixedSize(150, 20)
        self.btn_Leer_Busqueda_ID_Producto.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Leer_Busqueda_ID_Producto.clicked.connect(self.buscar_Producto)

        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Producto_Nombres = [
            'ID',
            'Nombre',
            'Cantidad',
            'Precio',
            'Codigo',
            'Caducidad'
        ]

        # Instanciar Widget
        self.tblw_Leer_Tabla_Producto = QTableWidget(self.lst_frm_Pestaña_1_1[2].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Producto.setFixedSize(764, 300)
        self.tblw_Leer_Tabla_Producto.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Producto.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Producto.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Producto.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Producto.setColumnCount(len(self.lst_Leer_Tabla_Producto_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Producto.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Producto_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Producto.horizontalHeader().setVisible(True)
        self.tblw_Leer_Tabla_Producto.verticalHeader().setVisible(False)

        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_productos()

        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Producto.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Producto.setItem(row_idx, col_idx, item)
        #[Panel_1-SubPanel_3-Pestania_2]==============================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Producto = QLabel('Crear Productos',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Producto.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Nombre_Producto = QLabel('Nombre Del Producto',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Nombre_Producto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Nombre_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Nombre_Producto.setPlaceholderText('Ingrese Nombre')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Nombre_Producto.setFixedSize(350, 20), self.txt_Crear_Nombre_Producto.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_Codigo_Producto = QLabel('Codigo Del Producto',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Codigo_Producto.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_Codigo_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Codigo_Producto.setPlaceholderText('Ingrese Codigo')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Codigo_Producto.setFixedSize(350, 20), self.txt_Crear_Codigo_Producto.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_Cantidad_Producto = QLabel('Cantidad De Unidades',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Cantidad_Producto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_Cantidad_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Cantidad_Producto.setPlaceholderText('Ingrese Cantidad')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Cantidad_Producto.setFixedSize(350, 20), self.txt_Crear_Cantidad_Producto.move(300, 160)
        
        # Instanciar Widget
        self.lbl_Crear_Precio_Producto = QLabel('Precio Del Producto',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Precio_Producto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Crear_Precio_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Precio_Producto.setPlaceholderText('Ingrese Precio')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Precio_Producto.setFixedSize(350, 20), self.txt_Crear_Precio_Producto.move(300, 190)
        
        # Instanciar Widget
        self.lbl_Crear_Fecha_Caducidad_Producto = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_1[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Fecha_Caducidad_Producto.move(150, 220)
        
        # Instanciar Widget
        self.de_Crear_Fecha_Caducidad_Producto = QDateEdit(self.lst_frm_Pestaña_1_1[2].widget(1))
        # Tamaño & Posicion De Widget
        self.de_Crear_Fecha_Caducidad_Producto.setFixedSize(350, 20), self.de_Crear_Fecha_Caducidad_Producto.move(300, 220)
        # Mostrar Calendario
        self.de_Crear_Fecha_Caducidad_Producto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Crear_Fecha_Caducidad_Producto.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Crear_Fecha_Caducidad_Producto.setDisplayFormat('yyyy/MM/dd')
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Producto = QPushButton('Crear', self.lst_frm_Pestaña_1_1[2].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Producto.setFixedSize(150, 20), self.btn_Crear_Aniadir_Producto.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Crear_Aniadir_Producto.clicked.connect(self.crear_Producto)
        #[Panel_1-SubPanel_3-Pestania_3]==============================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Producto = QLabel('Modificar Productos',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Producto.move(370, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Producto = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Producto.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Producto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Producto.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Producto.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Producto = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Producto.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Producto.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Modificar_Busqueda_ID_Producto.clicked.connect(self.habilitar_actualizar_producto)
        
        # Instanciar Widget
        self.lbl_Modificar_Nombre_Producto = QLabel('Nombre Del Producto',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Nombre_Producto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Nombre_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Nombre_Producto.setFixedSize(350, 20), self.txt_Modificar_Nombre_Producto.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Nombre_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Codigo_Producto = QLabel('Codigo Del Producto',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Codigo_Producto.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_Codigo_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Codigo_Producto.setFixedSize(350, 20), self.txt_Modificar_Codigo_Producto.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_Codigo_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Cantidad_Producto = QLabel('Cantidad De Unidades',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Cantidad_Producto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_Cantidad_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Cantidad_Producto.setFixedSize(350, 20), self.txt_Modificar_Cantidad_Producto.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_Cantidad_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Precio_Producto = QLabel('Precio Del Producto',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Precio_Producto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Modificar_Precio_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Precio_Producto.setFixedSize(350, 20), self.txt_Modificar_Precio_Producto.move(300, 190)
        #Inhabilitar Widget
        self.txt_Modificar_Precio_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Fecha_Caducidad_Producto = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_1[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Fecha_Caducidad_Producto.move(150, 220)
        
        # Instanciar Widget
        self.de_Modificar_Fecha_Caducidad_Producto = QDateEdit(self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.de_Modificar_Fecha_Caducidad_Producto.setFixedSize(350, 20), self.de_Modificar_Fecha_Caducidad_Producto.move(300, 220)
        # Mostrar Calendario
        self.de_Modificar_Fecha_Caducidad_Producto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Modificar_Fecha_Caducidad_Producto.setDate(QDate.currentDate())
        # Mostrar En Formato Especifico
        self.de_Modificar_Fecha_Caducidad_Producto.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Modificar_Fecha_Caducidad_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Producto = QPushButton('Modificar', self.lst_frm_Pestaña_1_1[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Producto.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Producto.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Modificar_Aniadir_Producto.clicked.connect(self.actualizar_Producto)
        #[Panel_1-SubPanel_3-Pestania_4]==============================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Producto = QLabel('Eliminar Productos',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Producto.move(375, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Producto = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Producto.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Producto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Producto.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Producto.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Producto = QPushButton('Buscar', self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Producto.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Producto.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Eliminar_Busqueda_ID_Producto.clicked.connect(self.buscar_eliminar_producto)
        
        # Instanciar Widget
        self.lbl_Eliminar_Nombre_Producto = QLabel('Nombre Del Producto',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Nombre_Producto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Nombre_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Nombre_Producto.setFixedSize(350, 20), self.txt_Eliminar_Nombre_Producto.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Nombre_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Codigo_Producto = QLabel('Codigo Del Producto',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Codigo_Producto.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_Codigo_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Codigo_Producto.setFixedSize(350, 20), self.txt_Eliminar_Codigo_Producto.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_Codigo_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Cantidad_Producto = QLabel('Cantidad De Unidades',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Cantidad_Producto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_Cantidad_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Cantidad_Producto.setFixedSize(350, 20), self.txt_Eliminar_Cantidad_Producto.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_Cantidad_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Precio_Producto = QLabel('Precio Del Producto',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Precio_Producto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Eliminar_Precio_Producto = QLineEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Precio_Producto.setFixedSize(350, 20), self.txt_Eliminar_Precio_Producto.move(300, 190)
        #Inhabilitar Widget
        self.txt_Eliminar_Precio_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Fecha_Caducidad_Producto = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_1[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Fecha_Caducidad_Producto.move(150, 220)
        
        # Instanciar Widget
        self.de_Eliminar_Fecha_Caducidad_Producto = QDateEdit(self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.de_Eliminar_Fecha_Caducidad_Producto.setFixedSize(350, 20), self.de_Eliminar_Fecha_Caducidad_Producto.move(300, 220)
        # Mostrar Calendario
        self.de_Eliminar_Fecha_Caducidad_Producto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Eliminar_Fecha_Caducidad_Producto.setDate(QDate.currentDate())
        # Mostrar En Formato Especifico
        self.de_Eliminar_Fecha_Caducidad_Producto.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Eliminar_Fecha_Caducidad_Producto.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Producto = QPushButton('Eliminar', self.lst_frm_Pestaña_1_1[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Producto.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Producto.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Producto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        self.btn_Eliminar_Aniadir_Producto.clicked.connect(self.eliminar_producto)
        #[Panel_2-SubPanel_1-Pestania_1]==============================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Cliente = QLabel('Visualizar Tabla De Clientes', self.lst_frm_Pestaña_1_2[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Cliente.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Cliente = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Cliente.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Cliente.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Cliente.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Cliente.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Cliente = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[0].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Cliente.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Cliente.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Cliente.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Cliente_Nombres = [
            'Cliente ID',
            'Persona ID',
            'Nombre',
            'A. Paterno',
            'A. Materno',
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Cliente = QTableWidget(self.lst_frm_Pestaña_1_2[0].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Cliente.setFixedSize(764, 300), self.tblw_Leer_Tabla_Cliente.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Cliente.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Cliente.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Cliente.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Cliente.setColumnCount(len(self.lst_Leer_Tabla_Cliente_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Cliente.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Cliente_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Cliente.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Cliente.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_clientes()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Cliente.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Cliente.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Cliente = QLabel('Crear Cliente',self.lst_frm_Pestaña_1_2[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Cliente.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Persona_Cliente = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Persona_Cliente.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_ID_Persona_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Persona_Cliente.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Persona_Cliente.setFixedSize(350, 20), self.txt_Crear_ID_Persona_Cliente.move(300, 100)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Cliente = QPushButton('Crear', self.lst_frm_Pestaña_1_2[0].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Cliente.setFixedSize(150, 20), self.btn_Crear_Aniadir_Cliente.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Cliente.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Cliente = QLabel('Modificar Cliente',self.lst_frm_Pestaña_1_2[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Cliente.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Cliente = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Cliente.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Cliente.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Cliente.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Cliente.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Cliente = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Cliente.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Cliente.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Cliente.clicked.connect(self.buscar_Datos_Cliente_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Persona_Cliente = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Persona_Cliente.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Persona_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Persona_Cliente.setFixedSize(350, 20), self.txt_Modificar_ID_Persona_Cliente.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Persona_Cliente.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Cliente = QPushButton('Modificar', self.lst_frm_Pestaña_1_2[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Cliente.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Cliente.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Cliente.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Cliente = QLabel('Eliminar Cliente',self.lst_frm_Pestaña_1_2[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Cliente.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Cliente = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Cliente.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Cliente.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Cliente.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Cliente.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Cliente = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Cliente.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Cliente.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Cliente.clicked.connect(self.buscar_Datos_Cliente_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Persona_Cliente = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Persona_Cliente.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Persona_Cliente = QLineEdit(self.lst_frm_Pestaña_1_2[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Persona_Cliente.setFixedSize(350, 20), self.txt_Eliminar_ID_Persona_Cliente.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Persona_Cliente.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Cliente = QPushButton('Eliminar', self.lst_frm_Pestaña_1_2[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Cliente.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Cliente.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Cliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Cliente.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Empl = QLabel('Visualizar Tabla Del Empleados', self.lst_frm_Pestaña_1_2[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Empl.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Empl = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Empl.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Empl = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Empl.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Empl.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Empl.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Empl = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[1].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Empl.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Empl.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Empl.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Empl.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Empl_Nombres = [
            'Empleado ID',
            'Persona ID',
            'Nombre',
            'A. Paterno',
            'A. Materno',
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Empl = QTableWidget(self.lst_frm_Pestaña_1_2[1].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Empl.setFixedSize(764, 300), self.tblw_Leer_Tabla_Empl.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Empl.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Empl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Empl.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Empl.setColumnCount(len(self.lst_Leer_Tabla_Empl_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Empl.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Empl_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Empl.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Empl.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_empleados()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Empl.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Empl.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Empleado = QLabel('Crear Empleado',self.lst_frm_Pestaña_1_2[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Empleado.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Persona_Empleado = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Persona_Empleado.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_ID_Persona_Empleado = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Persona_Empleado.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Persona_Empleado.setFixedSize(350, 20), self.txt_Crear_ID_Persona_Empleado.move(300, 100)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Empleado = QPushButton('Crear', self.lst_frm_Pestaña_1_2[1].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Empleado.setFixedSize(150, 20), self.btn_Crear_Aniadir_Empleado.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Empleado.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Empleado.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Empleado = QLabel('Modificar Empleado',self.lst_frm_Pestaña_1_2[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Empleado.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Empleado = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Empleado.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Empleado = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Empleado.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Empleado.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Empleado.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Empleado = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Empleado.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Empleado.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Empleado.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Empleado.clicked.connect(self.buscar_Datos_Empleado_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Persona_Empleado = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Persona_Empleado.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Persona_Empleado = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Persona_Empleado.setFixedSize(350, 20), self.txt_Modificar_ID_Persona_Empleado.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Persona_Empleado.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Empleado = QPushButton('Modificar', self.lst_frm_Pestaña_1_2[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Empleado.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Empleado.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Empleado.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Empleado.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Empleado = QLabel('Eliminar Empleado',self.lst_frm_Pestaña_1_2[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Empleado.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Empleado = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Empleado.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Empleado = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Empleado.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Empleado.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Empleado.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Empleado = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Empleado.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Empleado.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Empleado.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Empleado.clicked.connect(self.buscar_Datos_Empleado_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Persona_Empleado = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Persona_Empleado.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Persona_Empleado = QLineEdit(self.lst_frm_Pestaña_1_2[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Persona_Empleado.setFixedSize(350, 20), self.txt_Eliminar_ID_Persona_Empleado.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Persona_Empleado.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Empleado = QPushButton('Eliminar', self.lst_frm_Pestaña_1_2[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Empleado.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Empleado.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Empleado.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Empleado.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Prov = QLabel('Visualizar Tabla Del Proveedores', self.lst_frm_Pestaña_1_2[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Prov.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Prov = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Prov.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Prov = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Prov.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Prov.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Prov.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Prov = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[2].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Prov.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Prov.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Prov.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Prov.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Prov_Nombres = [
            'Proveedor ID',
            'Persona ID',
            'Nombre',
            'A. Paterno',
            'A. Materno'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Prov = QTableWidget(self.lst_frm_Pestaña_1_2[2].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Prov.setFixedSize(764, 300), self.tblw_Leer_Tabla_Prov.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Prov.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Prov.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Prov.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Prov.setColumnCount(len(self.lst_Leer_Tabla_Prov_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Prov.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Prov_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Prov.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Prov.verticalHeader().setVisible(False)
       # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_proveedores()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Prov.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Prov.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Prov = QLabel('Crear Proveedor',self.lst_frm_Pestaña_1_2[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Prov.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Persona_Prov = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Persona_Prov.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_ID_Persona_Prov = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Persona_Prov.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Persona_Prov.setFixedSize(350, 20), self.txt_Crear_ID_Persona_Prov.move(300, 100)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Prov = QPushButton('Crear', self.lst_frm_Pestaña_1_2[2].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Prov.setFixedSize(150, 20), self.btn_Crear_Aniadir_Prov.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Prov.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Prov.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Proveedor = QLabel('Modificar Proveedor',self.lst_frm_Pestaña_1_2[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Proveedor.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Persona_Proveedor = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Persona_Proveedor.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Persona_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Persona_Proveedor.setFixedSize(350, 20), self.txt_Modificar_ID_Persona_Proveedor.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Persona_Proveedor.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Proveedor = QPushButton('Modificar', self.lst_frm_Pestaña_1_2[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Proveedor.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Proveedor.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Proveedor.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Proveedor = QLabel('Eliminar Proveedor',self.lst_frm_Pestaña_1_2[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Proveedor.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Persona_Proveedor = QLabel('ID De Persona',self.lst_frm_Pestaña_1_2[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Persona_Proveedor.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Persona_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_2[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Persona_Proveedor.setFixedSize(350, 20), self.txt_Eliminar_ID_Persona_Proveedor.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Persona_Proveedor.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Proveedor = QPushButton('Eliminar', self.lst_frm_Pestaña_1_2[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Proveedor.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Proveedor.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Proveedor.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_AccEmpl = QLabel('Visualizar Tabla De Acceso De Empleados', self.lst_frm_Pestaña_1_2[3].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_AccEmpl.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_AccEmpl = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[3].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_AccEmpl.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_AccEmpl = QLineEdit(self.lst_frm_Pestaña_1_2[3].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_AccEmpl.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_AccEmpl.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_AccEmpl.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_AccEmpl = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[3].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_AccEmpl.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_AccEmpl.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_AccEmpl.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_AccEmpl.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_AccEmpl_Nombres = [
            'Acceso ID',
            'Fecha De Acceso',
            'Empleado ID',
            'Persona ID',
            'Nombre',
            'A. Paterno',
            'A. Materno'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_AccEmpl = QTableWidget(self.lst_frm_Pestaña_1_2[3].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_AccEmpl.setFixedSize(764, 300), self.tblw_Leer_Tabla_AccEmpl.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_AccEmpl.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_AccEmpl.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_AccEmpl.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_AccEmpl.setColumnCount(len(self.lst_Leer_Tabla_AccEmpl_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_AccEmpl.setHorizontalHeaderLabels(self.lst_Leer_Tabla_AccEmpl_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_AccEmpl.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_AccEmpl.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_acceso_empleados()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_AccEmpl.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_AccEmpl.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_AccEmpl = QLabel('Crear Acceso',self.lst_frm_Pestaña_1_2[3].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_AccEmpl.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Fecha_Nacimiento_AccEmpl = QLabel('Fecha De Acceso',self.lst_frm_Pestaña_1_2[3].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Fecha_Nacimiento_AccEmpl.move(150, 100)
        
        # Instanciar Widget
        self.de_Crear_Fecha_Nacimiento_AccEmpl = QDateEdit(self.lst_frm_Pestaña_1_2[3].widget(1))
        # Tamaño & Posicion De Widget
        self.de_Crear_Fecha_Nacimiento_AccEmpl.setFixedSize(350, 20), self.de_Crear_Fecha_Nacimiento_AccEmpl.move(300, 100)
        # Mostrar Calendario
        self.de_Crear_Fecha_Nacimiento_AccEmpl.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Crear_Fecha_Nacimiento_AccEmpl.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Crear_Fecha_Nacimiento_AccEmpl.setDisplayFormat('yyyy/MM/dd')
        
        # Instanciar Widget
        self.lbl_Crear_ID_Empleado_AccEmpl = QLabel('ID De Empleado',self.lst_frm_Pestaña_1_2[3].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Empleado_AccEmpl.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Empleado_AccEmpl = QLineEdit(self.lst_frm_Pestaña_1_2[3].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Empleado_AccEmpl.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Empleado_AccEmpl.setFixedSize(350, 20), self.txt_Crear_ID_Empleado_AccEmpl.move(300, 130)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_AccEmpl = QPushButton('Crear', self.lst_frm_Pestaña_1_2[3].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_AccEmpl.setFixedSize(150, 20), self.btn_Crear_Aniadir_AccEmpl.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_AccEmpl.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_AccEmpl.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Persona = QLabel('Visualizar Tabla Del Persona', self.lst_frm_Pestaña_1_2[4].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Persona.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Persona = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[4].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Persona.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(0))
        # Texto Dentro Del LineEdit De EjPersonao
        self.txt_Leer_Busqueda_ID_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Persona.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Persona.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Persona = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[4].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Persona.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Persona.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Persona.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Persona_Nombres = [
            'Persona ID',
            'Nombre',
            'A. Paterno',
            'A. Materno',
            'Fecha Nacimiento',
            'Edad',
            'Direccion ID',
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Persona = QTableWidget(self.lst_frm_Pestaña_1_2[4].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Persona.setFixedSize(764, 300), self.tblw_Leer_Tabla_Persona.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Persona.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Persona.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Persona.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Persona.setColumnCount(len(self.lst_Leer_Tabla_Persona_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Persona.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Persona_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Persona.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Persona.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_personas()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Persona.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Persona.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Persona = QLabel('Crear Persona',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Persona.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Nombre_Persona = QLabel('Nombre',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Nombre_Persona.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Nombre_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Nombre_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Nombre_Persona.setFixedSize(350, 20), self.txt_Crear_Nombre_Persona.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_Apellido_P_Persona = QLabel('Apellido Paterno',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Apellido_P_Persona.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_Apellido_P_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Apellido_P_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Apellido_P_Persona.setFixedSize(350, 20), self.txt_Crear_Apellido_P_Persona.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_Apellido_M_Persona = QLabel('Apellido Materno',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Apellido_M_Persona.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_Apellido_M_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Apellido_M_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Apellido_M_Persona.setFixedSize(350, 20), self.txt_Crear_Apellido_M_Persona.move(300, 160)
        
        # Instanciar Widget
        self.lbl_Crear_Fecha_Nacimiento_Persona = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Fecha_Nacimiento_Persona.move(150, 190)
        
        # Instanciar Widget
        self.de_Crear_Fecha_Nacimiento_Persona = QDateEdit(self.lst_frm_Pestaña_1_2[4].widget(1))
        # Tamaño & Posicion De Widget
        self.de_Crear_Fecha_Nacimiento_Persona.setFixedSize(350, 20), self.de_Crear_Fecha_Nacimiento_Persona.move(300, 190)
        # Mostrar Calendario
        self.de_Crear_Fecha_Nacimiento_Persona.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Crear_Fecha_Nacimiento_Persona.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Crear_Fecha_Nacimiento_Persona.setDisplayFormat('yyyy/MM/dd')
        
        # Instanciar Widget
        self.lbl_Crear_ID_Direccion_Persona = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_2[4].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Direccion_Persona.move(150, 220)
        
        # Instanciar Widget
        self.txt_Crear_ID_Direccion_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Direccion_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Direccion_Persona.setFixedSize(350, 20), self.txt_Crear_ID_Direccion_Persona.move(300, 220)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Persona = QPushButton('Crear', self.lst_frm_Pestaña_1_2[4].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Persona.setFixedSize(150, 20), self.btn_Crear_Aniadir_Persona.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Persona.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Persona = QLabel('Modificar Persona',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Persona.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Persona = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Persona.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Persona.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Persona.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Persona = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Persona.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Persona.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Persona.clicked.connect(self.buscar_Datos_Persona_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Nombre_Persona = QLabel('Nombre',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Nombre_Persona.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Nombre_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Nombre_Persona.setFixedSize(350, 20), self.txt_Modificar_Nombre_Persona.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Nombre_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Apellido_P_Persona = QLabel('Apellido Paterno',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Apellido_P_Persona.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_Apellido_P_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Apellido_P_Persona.setFixedSize(350, 20), self.txt_Modificar_Apellido_P_Persona.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_Apellido_P_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Apellido_M_Persona = QLabel('Apellido Materno',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Apellido_M_Persona.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_Apellido_M_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Apellido_M_Persona.setFixedSize(350, 20), self.txt_Modificar_Apellido_M_Persona.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_Apellido_M_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Fecha_Nacimiento_Persona = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Fecha_Nacimiento_Persona.move(150, 190)
        
        # Instanciar Widget
        self.de_Modificar_Fecha_Nacimiento_Persona = QDateEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.de_Modificar_Fecha_Nacimiento_Persona.setFixedSize(350, 20), self.de_Modificar_Fecha_Nacimiento_Persona.move(300, 190)
        # Mostrar Calendario
        self.de_Modificar_Fecha_Nacimiento_Persona.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Modificar_Fecha_Nacimiento_Persona.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Modificar_Fecha_Nacimiento_Persona.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Modificar_Fecha_Nacimiento_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Direccion_Persona = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_2[4].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Direccion_Persona.move(150, 220)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Direccion_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Direccion_Persona.setFixedSize(350, 20), self.txt_Modificar_ID_Direccion_Persona.move(300, 220)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Direccion_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Persona = QPushButton('Modificar', self.lst_frm_Pestaña_1_2[4].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Persona.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Persona.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Persona.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Persona = QLabel('Eliminar Persona',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Persona.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Persona = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Persona.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Persona.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Persona.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Persona.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Persona = QPushButton('Buscar', self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Persona.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Persona.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Persona.clicked.connect(self.buscar_Datos_Persona_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Nombre_Persona = QLabel('Nombre',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Nombre_Persona.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Nombre_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Nombre_Persona.setFixedSize(350, 20), self.txt_Eliminar_Nombre_Persona.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Nombre_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Apellido_P_Persona = QLabel('Apellido Paterno',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Apellido_P_Persona.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_Apellido_P_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Apellido_P_Persona.setFixedSize(350, 20), self.txt_Eliminar_Apellido_P_Persona.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_Apellido_P_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Apellido_M_Persona = QLabel('Apellido Materno',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Apellido_M_Persona.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_Apellido_M_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Apellido_M_Persona.setFixedSize(350, 20), self.txt_Eliminar_Apellido_M_Persona.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_Apellido_M_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Fecha_Nacimiento_Persona = QLabel('Fecha De Caducidad',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Fecha_Nacimiento_Persona.move(150, 190)
        
        # Instanciar Widget
        self.de_Eliminar_Fecha_Nacimiento_Persona = QDateEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.de_Eliminar_Fecha_Nacimiento_Persona.setFixedSize(350, 20), self.de_Eliminar_Fecha_Nacimiento_Persona.move(300, 190)
        # Mostrar Calendario
        self.de_Eliminar_Fecha_Nacimiento_Persona.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Eliminar_Fecha_Nacimiento_Persona.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Eliminar_Fecha_Nacimiento_Persona.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Eliminar_Fecha_Nacimiento_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Direccion_Persona = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_2[4].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Direccion_Persona.move(150, 220)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Direccion_Persona = QLineEdit(self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Direccion_Persona.setFixedSize(350, 20), self.txt_Eliminar_ID_Direccion_Persona.move(300, 220)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Direccion_Persona.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Persona = QPushButton('Eliminar', self.lst_frm_Pestaña_1_2[4].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Persona.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Persona.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Persona.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Persona.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_LocAlm = QLabel('Visualizar Tabla De Localizaciones De Almacenes', self.lst_frm_Pestaña_1_3[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_LocAlm.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_LocAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_LocAlm.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_LocAlm.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_LocAlm.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_LocAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[0].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_LocAlm.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_LocAlm.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_LocAlm.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_LocAlm_Nombres = [
            'Almacen ID',
            'Nombre',
            'Sucursal ID',
            'Direccion ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_LocAlm = QTableWidget(self.lst_frm_Pestaña_1_3[0].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_LocAlm.setFixedSize(764, 300), self.tblw_Leer_Tabla_LocAlm.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_LocAlm.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_LocAlm.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_LocAlm.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_LocAlm.setColumnCount(len(self.lst_Leer_Tabla_LocAlm_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_LocAlm.setHorizontalHeaderLabels(self.lst_Leer_Tabla_LocAlm_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_LocAlm.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_LocAlm.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_almacenes()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_LocAlm.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_LocAlm.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_LocAlm = QLabel('Crear Almacen',self.lst_frm_Pestaña_1_3[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_LocAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Nombre_LocAlm = QLabel('Nombre',self.lst_frm_Pestaña_1_3[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Nombre_LocAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Nombre_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Nombre_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Nombre_LocAlm.setFixedSize(350, 20), self.txt_Crear_Nombre_LocAlm.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Sucursal_LocAlm = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_3[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Sucursal_LocAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Sucursal_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Sucursal_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Sucursal_LocAlm.setFixedSize(350, 20), self.txt_Crear_ID_Sucursal_LocAlm.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Direccion_LocAlm = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Direccion_LocAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_ID_Direccion_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Direccion_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Direccion_LocAlm.setFixedSize(350, 20), self.txt_Crear_ID_Direccion_LocAlm.move(300, 160)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_LocAlm = QPushButton('Crear', self.lst_frm_Pestaña_1_3[0].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_LocAlm.setFixedSize(150, 20), self.btn_Crear_Aniadir_LocAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_LocAlm.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_LocAlm = QLabel('Modificar Almacen',self.lst_frm_Pestaña_1_3[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_LocAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_LocAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_LocAlm.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_LocAlm.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_LocAlm.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_LocAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_LocAlm.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_LocAlm.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_LocAlm.clicked.connect(self.buscar_Datos_LocAlm_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Nombre_LocAlm = QLabel('Nombre',self.lst_frm_Pestaña_1_3[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Nombre_LocAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Nombre_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Nombre_LocAlm.setFixedSize(350, 20), self.txt_Modificar_Nombre_LocAlm.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Nombre_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Sucursal_LocAlm = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_3[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Sucursal_LocAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Sucursal_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Sucursal_LocAlm.setFixedSize(350, 20), self.txt_Modificar_ID_Sucursal_LocAlm.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Sucursal_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Direccion_LocAlm = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Direccion_LocAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Direccion_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Direccion_LocAlm.setFixedSize(350, 20), self.txt_Modificar_ID_Direccion_LocAlm.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Direccion_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_LocAlm = QPushButton('Modificar', self.lst_frm_Pestaña_1_3[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_LocAlm.setFixedSize(150, 20), self.btn_Modificar_Aniadir_LocAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_LocAlm.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_LocAlm = QLabel('Eliminar Almacen',self.lst_frm_Pestaña_1_3[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_LocAlm.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_LocAlm = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_LocAlm.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_LocAlm.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_LocAlm.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_LocAlm.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_LocAlm = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_LocAlm.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_LocAlm.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_LocAlm.clicked.connect(self.buscar_Datos_LocAlm_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Nombre_LocAlm = QLabel('Nombre',self.lst_frm_Pestaña_1_3[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Nombre_LocAlm.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Nombre_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Nombre_LocAlm.setFixedSize(350, 20), self.txt_Eliminar_Nombre_LocAlm.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Nombre_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Sucursal_LocAlm = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_3[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Sucursal_LocAlm.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Sucursal_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Sucursal_LocAlm.setFixedSize(350, 20), self.txt_Eliminar_ID_Sucursal_LocAlm.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Sucursal_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Direccion_LocAlm = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Direccion_LocAlm.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Direccion_LocAlm = QLineEdit(self.lst_frm_Pestaña_1_3[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Direccion_LocAlm.setFixedSize(350, 20), self.txt_Eliminar_ID_Direccion_LocAlm.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Direccion_LocAlm.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_LocAlm = QPushButton('Eliminar', self.lst_frm_Pestaña_1_3[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_LocAlm.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_LocAlm.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_LocAlm.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_LocAlm.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_LocSuc = QLabel('Visualizar Tabla De Localizaciones De Sucursales', self.lst_frm_Pestaña_1_3[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_LocSuc.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_LocSuc = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_LocSuc.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_LocSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_LocSuc.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_LocSuc.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_LocSuc = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[1].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_LocSuc.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_LocSuc.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_LocSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_LocSuc.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_LocSuc_Nombres = [
            'Sucursal ID',
            'Nombre',
            'Direccion ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_LocSuc = QTableWidget(self.lst_frm_Pestaña_1_3[1].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_LocSuc.setFixedSize(764, 300), self.tblw_Leer_Tabla_LocSuc.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_LocSuc.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_LocSuc.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_LocSuc.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_LocSuc.setColumnCount(len(self.lst_Leer_Tabla_LocSuc_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_LocSuc.setHorizontalHeaderLabels(self.lst_Leer_Tabla_LocSuc_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_LocSuc.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_LocSuc.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_sucursales()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_LocSuc.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_LocSuc.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_LocSuc = QLabel('Crear Sucursal',self.lst_frm_Pestaña_1_3[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_LocSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Nombre_LocSuc = QLabel('Nombre',self.lst_frm_Pestaña_1_3[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Nombre_LocSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Nombre_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Nombre_LocSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Nombre_LocSuc.setFixedSize(350, 20), self.txt_Crear_Nombre_LocSuc.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Direccion_LocSuc = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Direccion_LocSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Direccion_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Direccion_LocSuc.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Direccion_LocSuc.setFixedSize(350, 20), self.txt_Crear_ID_Direccion_LocSuc.move(300, 130)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_LocSuc = QPushButton('Crear', self.lst_frm_Pestaña_1_3[1].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_LocSuc.setFixedSize(150, 20), self.btn_Crear_Aniadir_LocSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_LocSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_LocSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_LocSuc = QLabel('Modificar Sucursal',self.lst_frm_Pestaña_1_3[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_LocSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)

        # Instanciar Widget
        self.lbl_Modificar_Nombre_LocSuc = QLabel('Nombre',self.lst_frm_Pestaña_1_3[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Nombre_LocSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Nombre_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Nombre_LocSuc.setFixedSize(350, 20), self.txt_Modificar_Nombre_LocSuc.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Nombre_LocSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Direccion_LocSuc = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Direccion_LocSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Direccion_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Direccion_LocSuc.setFixedSize(350, 20), self.txt_Modificar_ID_Direccion_LocSuc.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Direccion_LocSuc.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_LocSuc = QPushButton('Modificar', self.lst_frm_Pestaña_1_3[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_LocSuc.setFixedSize(150, 20), self.btn_Modificar_Aniadir_LocSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_LocSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_LocSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_LocSuc = QLabel('Eliminar Sucursal',self.lst_frm_Pestaña_1_3[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_LocSuc.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)

        # Instanciar Widget
        self.lbl_Eliminar_Nombre_LocSuc = QLabel('Nombre',self.lst_frm_Pestaña_1_3[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Nombre_LocSuc.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Nombre_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Nombre_LocSuc.setFixedSize(350, 20), self.txt_Eliminar_Nombre_LocSuc.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Nombre_LocSuc.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Direccion_LocSuc = QLabel('ID De Direccion',self.lst_frm_Pestaña_1_3[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Direccion_LocSuc.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Direccion_LocSuc = QLineEdit(self.lst_frm_Pestaña_1_3[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Direccion_LocSuc.setFixedSize(350, 20), self.txt_Eliminar_ID_Direccion_LocSuc.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Direccion_LocSuc.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_LocSuc = QPushButton('Eliminar', self.lst_frm_Pestaña_1_3[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_LocSuc.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_LocSuc.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_LocSuc.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_LocSuc.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Direccion = QLabel('Visualizar Tabla De Direcciones', self.lst_frm_Pestaña_1_3[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Direccion.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Direccion = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[2].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Direccion.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Direccion.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Direccion.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Direccion = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[2].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Direccion.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Direccion.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Direccion.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Direccion.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Direccion_Nombres = [
            'Direcccion ID',
            'Calle',
            'Ciudad',
            'Estado',
            'Pais',
            'Codigo Postal'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Direccion = QTableWidget(self.lst_frm_Pestaña_1_3[2].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Direccion.setFixedSize(764, 300), self.tblw_Leer_Tabla_Direccion.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Direccion.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Direccion.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Direccion.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Direccion.setColumnCount(len(self.lst_Leer_Tabla_Direccion_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Direccion.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Direccion_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Direccion.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Direccion.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_direcciones()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Direccion.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Direccion.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Direccion = QLabel('Crear Direccion',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Direccion.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Calle_Direccion = QLabel('Calle',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Calle_Direccion.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Calle_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Calle_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Calle_Direccion.setFixedSize(350, 20), self.txt_Crear_Calle_Direccion.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_Ciudad_Direccion = QLabel('Ciudad',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Ciudad_Direccion.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_Ciudad_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Ciudad_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Ciudad_Direccion.setFixedSize(350, 20), self.txt_Crear_Ciudad_Direccion.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_Estado_Direccion = QLabel('Estado',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Estado_Direccion.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_Estado_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Estado_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Estado_Direccion.setFixedSize(350, 20), self.txt_Crear_Estado_Direccion.move(300, 160)
        
        # Instanciar Widget
        self.lbl_Crear_Pais_Direccion = QLabel('Pais',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Pais_Direccion.move(150, 190)
        
        # Instanciar Widget
        self.txt_Crear_Pais_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Pais_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Pais_Direccion.setFixedSize(350, 20), self.txt_Crear_Pais_Direccion.move(300, 190)
        
        # Instanciar Widget
        self.lbl_Crear_CodigoPostal_Direccion = QLabel('Codigo Postal',self.lst_frm_Pestaña_1_3[2].widget(1))
        # Posicion De Widget
        self.lbl_Crear_CodigoPostal_Direccion.move(150, 220)
        
        # Instanciar Widget
        self.txt_Crear_CodigoPostal_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_CodigoPostal_Direccion.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_CodigoPostal_Direccion.setFixedSize(350, 20), self.txt_Crear_CodigoPostal_Direccion.move(300, 220)
        # Instanciar Widget
        self.btn_Crear_Aniadir_Direccion = QPushButton('Crear', self.lst_frm_Pestaña_1_3[2].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Direccion.setFixedSize(150, 20), self.btn_Crear_Aniadir_Direccion.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Direccion.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Direccion.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Direccion = QLabel('Modificar Direccion',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Direccion.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Calle_Direccion = QLabel('Calle',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Calle_Direccion.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Calle_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Calle_Direccion.setFixedSize(350, 20), self.txt_Modificar_Calle_Direccion.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Calle_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Ciudad_Direccion = QLabel('Ciudad',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Ciudad_Direccion.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_Ciudad_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Ciudad_Direccion.setFixedSize(350, 20), self.txt_Modificar_Ciudad_Direccion.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_Ciudad_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Estado_Direccion = QLabel('Estado',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Estado_Direccion.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_Estado_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Estado_Direccion.setFixedSize(350, 20), self.txt_Modificar_Estado_Direccion.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_Estado_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_Pais_Direccion = QLabel('Pais',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Pais_Direccion.move(150, 190)
        
        # Instanciar Widget
        self.txt_Modificar_Pais_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Pais_Direccion.setFixedSize(350, 20), self.txt_Modificar_Pais_Direccion.move(300, 190)
        #Inhabilitar Widget
        self.txt_Modificar_Pais_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_CodigoPostal_Direccion = QLabel('Codigo Postal',self.lst_frm_Pestaña_1_3[2].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_CodigoPostal_Direccion.move(150, 220)
        
        # Instanciar Widget
        self.txt_Modificar_CodigoPostal_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_CodigoPostal_Direccion.setFixedSize(350, 20), self.txt_Modificar_CodigoPostal_Direccion.move(300, 220)
        #Inhabilitar Widget
        self.txt_Modificar_CodigoPostal_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Direccion = QPushButton('Modificar', self.lst_frm_Pestaña_1_3[2].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Direccion.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Direccion.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Direccion.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Direccion.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Direccion = QLabel('Eliminar Direccion',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Direccion.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Proveedor.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Proveedor.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Proveedor.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Proveedor.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor = QPushButton('Buscar', self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Proveedor.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Proveedor.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Proveedor.clicked.connect(self.buscar_Datos_Proveedor_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Calle_Direccion = QLabel('Calle',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Calle_Direccion.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Calle_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Calle_Direccion.setFixedSize(350, 20), self.txt_Eliminar_Calle_Direccion.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Calle_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Ciudad_Direccion = QLabel('Ciudad',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Ciudad_Direccion.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_Ciudad_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Ciudad_Direccion.setFixedSize(350, 20), self.txt_Eliminar_Ciudad_Direccion.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_Ciudad_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Estado_Direccion = QLabel('Estado',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Estado_Direccion.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_Estado_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Estado_Direccion.setFixedSize(350, 20), self.txt_Eliminar_Estado_Direccion.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_Estado_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_Pais_Direccion = QLabel('Pais',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Pais_Direccion.move(150, 190)
        
        # Instanciar Widget
        self.txt_Eliminar_Pais_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Pais_Direccion.setFixedSize(350, 20), self.txt_Eliminar_Pais_Direccion.move(300, 190)
        #Inhabilitar Widget
        self.txt_Eliminar_Pais_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_CodigoPostal_Direccion = QLabel('Codigo Postal',self.lst_frm_Pestaña_1_3[2].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_CodigoPostal_Direccion.move(150, 220)
        
        # Instanciar Widget
        self.txt_Eliminar_CodigoPostal_Direccion = QLineEdit(self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_CodigoPostal_Direccion.setFixedSize(350, 20), self.txt_Eliminar_CodigoPostal_Direccion.move(300, 220)
        #Inhabilitar Widget
        self.txt_Eliminar_CodigoPostal_Direccion.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Direccion = QPushButton('Eliminar', self.lst_frm_Pestaña_1_3[2].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Direccion.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Direccion.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Direccion.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Direccion.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Gasto = QLabel('Crear Gasto',self.lst_frm_Pestaña_1_4[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Gasto.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Monto_Gasto = QLabel('Monto',self.lst_frm_Pestaña_1_4[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Monto_Gasto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Crear_Monto_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_Monto_Gasto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_Monto_Gasto.setFixedSize(350, 20), self.txt_Crear_Monto_Gasto.move(300, 100)
        
        # Instanciar Widget
        self.lbl_Crear_FechaGasto_Gasto = QLabel('Fecha De Gasto',self.lst_frm_Pestaña_1_4[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_FechaGasto_Gasto.move(150, 130)
        
        # Instanciar Widget
        self.de_Crear_FechaGasto_Gasto = QDateEdit(self.lst_frm_Pestaña_1_4[0].widget(1))
        # Tamaño & Posicion De Widget
        self.de_Crear_FechaGasto_Gasto.setFixedSize(350, 20), self.de_Crear_FechaGasto_Gasto.move(300, 130)
        # Mostrar Calendario
        self.de_Crear_FechaGasto_Gasto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Crear_FechaGasto_Gasto.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Crear_FechaGasto_Gasto.setDisplayFormat('yyyy/MM/dd')
        
        # Instanciar Widget
        self.lbl_Crear_ID_Sucursal_Gasto = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Sucursal_Gasto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_ID_Sucursal_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Sucursal_Gasto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Sucursal_Gasto.setFixedSize(350, 20), self.txt_Crear_ID_Sucursal_Gasto.move(300, 160)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Proveedor_Gasto = QLabel('ID De Proveedor',self.lst_frm_Pestaña_1_4[0].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Proveedor_Gasto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Crear_ID_Proveedor_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Proveedor_Gasto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Proveedor_Gasto.setFixedSize(350, 20), self.txt_Crear_ID_Proveedor_Gasto.move(300, 190)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Gasto = QPushButton('Crear', self.lst_frm_Pestaña_1_4[0].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Gasto.setFixedSize(150, 20), self.btn_Crear_Aniadir_Gasto.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Gasto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Gasto.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Gasto = QLabel('Modificar Gasto',self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Gasto.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Gasto = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Gasto.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Gasto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Gasto.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Gasto.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Gasto = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Gasto.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Gasto.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Gasto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Gasto.clicked.connect(self.buscar_Datos_Gasto_1_1_3)
        # Instanciar Widget
        self.lbl_Modificar_Monto_Gasto = QLabel('Monto',self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Monto_Gasto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Modificar_Monto_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Monto_Gasto.setFixedSize(350, 20), self.txt_Modificar_Monto_Gasto.move(300, 100)
        #Inhabilitar Widget
        self.txt_Modificar_Monto_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_FechaGasto_Gasto = QLabel('Fecha De Gasto',self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_FechaGasto_Gasto.move(150, 130)
        
        # Instanciar Widget
        self.de_Modificar_FechaGasto_Gasto = QDateEdit(self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.de_Modificar_FechaGasto_Gasto.setFixedSize(350, 20), self.de_Modificar_FechaGasto_Gasto.move(300, 130)
        # Mostrar Calendario
        self.de_Modificar_FechaGasto_Gasto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Modificar_FechaGasto_Gasto.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Modificar_FechaGasto_Gasto.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Modificar_FechaGasto_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Sucursal_Gasto = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Sucursal_Gasto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Sucursal_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Sucursal_Gasto.setFixedSize(350, 20), self.txt_Modificar_ID_Sucursal_Gasto.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Sucursal_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Proveedor_Gasto = QLabel('ID De Proveedor',self.lst_frm_Pestaña_1_4[0].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Proveedor_Gasto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Proveedor_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Proveedor_Gasto.setFixedSize(350, 20), self.txt_Modificar_ID_Proveedor_Gasto.move(300, 190)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Proveedor_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Gasto = QPushButton('Modificar', self.lst_frm_Pestaña_1_4[0].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Gasto.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Gasto.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Gasto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Gasto.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Gasto = QLabel('Eliminar Gasto',self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Gasto.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Gasto = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Gasto.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Gasto.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Gasto.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Gasto.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Gasto = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Gasto.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Gasto.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Gasto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Gasto.clicked.connect(self.buscar_Datos_Gasto_1_1_3)
        # Instanciar Widget
        self.lbl_Eliminar_Monto_Gasto = QLabel('Monto',self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Monto_Gasto.move(150, 100)
        
        # Instanciar Widget
        self.txt_Eliminar_Monto_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Monto_Gasto.setFixedSize(350, 20), self.txt_Eliminar_Monto_Gasto.move(300, 100)
        #Inhabilitar Widget
        self.txt_Eliminar_Monto_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_FechaGasto_Gasto = QLabel('Fecha De Gasto',self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_FechaGasto_Gasto.move(150, 130)
        
        # Instanciar Widget
        self.de_Eliminar_FechaGasto_Gasto = QDateEdit(self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.de_Eliminar_FechaGasto_Gasto.setFixedSize(350, 20), self.de_Eliminar_FechaGasto_Gasto.move(300, 130)
        # Mostrar Calendario
        self.de_Eliminar_FechaGasto_Gasto.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Eliminar_FechaGasto_Gasto.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Eliminar_FechaGasto_Gasto.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Eliminar_FechaGasto_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Sucursal_Gasto = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Sucursal_Gasto.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Sucursal_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Sucursal_Gasto.setFixedSize(350, 20), self.txt_Eliminar_ID_Sucursal_Gasto.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Sucursal_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Proveedor_Gasto = QLabel('ID De Proveedor',self.lst_frm_Pestaña_1_4[0].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Proveedor_Gasto.move(150, 190)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Proveedor_Gasto = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Proveedor_Gasto.setFixedSize(350, 20), self.txt_Eliminar_ID_Proveedor_Gasto.move(300, 190)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Proveedor_Gasto.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Gasto = QPushButton('Eliminar', self.lst_frm_Pestaña_1_4[0].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Gasto.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Gasto.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Gasto.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Aniadir_Gasto.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Gastos = QLabel('Visualizar Tabla De Gastos', self.lst_frm_Pestaña_1_4[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Gastos.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Gastos = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[0].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Gastos.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Gastos = QLineEdit(self.lst_frm_Pestaña_1_4[0].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Gastos.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Gastos.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Gastos.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Gastos = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[0].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Gastos.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Gastos.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Gastos.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Gastos.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Gastos_Nombres = [
            'Gasto ID',
            'Monto',
            'Fecha Gasto',
            'Sucursal ID',
            'Proveedor ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Gastos = QTableWidget(self.lst_frm_Pestaña_1_4[0].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Gastos.setFixedSize(764, 300), self.tblw_Leer_Tabla_Gastos.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Gastos.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Gastos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Gastos.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Gastos.setColumnCount(len(self.lst_Leer_Tabla_Gastos_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Gastos.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Gastos_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Gastos.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Gastos.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_gastos()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Gastos.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Gastos.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_Ventas = QLabel('Visualizar Tabla De Ventas', self.lst_frm_Pestaña_1_4[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_Ventas.move(20, 10)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_Ventas = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[1].widget(0))
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_Ventas.move(20, 30)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_Ventas = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(0))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_Ventas.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_Ventas.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_Ventas.move(110, 30)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_Ventas = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[1].widget(0))
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_Ventas.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_Ventas.move(270, 30)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_Ventas.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_Ventas.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_Ventas_Nombres = [
            'Venta ID',
            'Fecha Venta',
            'Sucursal ID',
            'Cliente ID'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_Ventas = QTableWidget(self.lst_frm_Pestaña_1_4[1].widget(0))
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_Ventas.setFixedSize(764, 300), self.tblw_Leer_Tabla_Ventas.move(20, 60)
        # Estilo De Widget
        self.tblw_Leer_Tabla_Ventas.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_Ventas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_Ventas.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_Ventas.setColumnCount(len(self.lst_Leer_Tabla_Ventas_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_Ventas.setHorizontalHeaderLabels(self.lst_Leer_Tabla_Ventas_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_Ventas.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_Ventas.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.buscar_ticket_ventas()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_Ventas.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_Ventas.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Crear_Titulo_Venta = QLabel('Crear Venta',self.lst_frm_Pestaña_1_4[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Titulo_Venta.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Crear_Fecha_Venta_Venta = QLabel('Fecha De Venta',self.lst_frm_Pestaña_1_4[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_Fecha_Venta_Venta.move(150, 100)
        
        # Instanciar Widget
        self.de_Crear_Fecha_Venta_Venta = QDateEdit(self.lst_frm_Pestaña_1_4[1].widget(1))
        # Tamaño & Posicion De Widget
        self.de_Crear_Fecha_Venta_Venta.setFixedSize(350, 20), self.de_Crear_Fecha_Venta_Venta.move(300, 100)
        # Mostrar Calendario
        self.de_Crear_Fecha_Venta_Venta.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Crear_Fecha_Venta_Venta.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Crear_Fecha_Venta_Venta.setDisplayFormat('yyyy/MM/dd')
        
        # Instanciar Widget
        self.lbl_Crear_ID_Sucursal_Venta = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Sucursal_Venta.move(150, 130)
        
        # Instanciar Widget
        self.txt_Crear_ID_Sucursal_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Sucursal_Venta.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Sucursal_Venta.setFixedSize(350, 20), self.txt_Crear_ID_Sucursal_Venta.move(300, 130)
        
        # Instanciar Widget
        self.lbl_Crear_ID_Cliente_Venta = QLabel('ID De Cliente',self.lst_frm_Pestaña_1_4[1].widget(1))
        # Posicion De Widget
        self.lbl_Crear_ID_Cliente_Venta.move(150, 160)
        
        # Instanciar Widget
        self.txt_Crear_ID_Cliente_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(1))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Crear_ID_Cliente_Venta.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Crear_ID_Cliente_Venta.setFixedSize(350, 20), self.txt_Crear_ID_Cliente_Venta.move(300, 160)
        
        # Instanciar Widget
        self.btn_Crear_Aniadir_Venta = QPushButton('Crear', self.lst_frm_Pestaña_1_4[1].widget(1))
        # Tamaño & Posicion De Widget
        self.btn_Crear_Aniadir_Venta.setFixedSize(150, 20), self.btn_Crear_Aniadir_Venta.move(342, 340)
        # Estilo De Widget
        self.btn_Crear_Aniadir_Venta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Crear_Aniadir_Venta.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Modificar_Titulo_Venta = QLabel('Modificar Venta',self.lst_frm_Pestaña_1_4[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Titulo_Venta.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Modificar_Busqueda_ID_Venta = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Busqueda_ID_Venta.move(150, 70)
        
        # Instanciar Widget
        self.txt_Modificar_Busqueda_ID_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(2))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Modificar_Busqueda_ID_Venta.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Modificar_Busqueda_ID_Venta.setFixedSize(190, 20), self.txt_Modificar_Busqueda_ID_Venta.move(300, 70)
        
        # Instanciar Widget
        self.btn_Modificar_Busqueda_ID_Venta = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Busqueda_ID_Venta.setFixedSize(150, 20), self.btn_Modificar_Busqueda_ID_Venta.move(500, 70)
        # Estilo De Widget
        self.btn_Modificar_Busqueda_ID_Venta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Busqueda_ID_Venta.clicked.connect(self.buscar_Datos_Venta_1_1_3)
        
        # Instanciar Widget
        self.lbl_Modificar_Fecha_Venta_Venta = QLabel('Fecha De Venta',self.lst_frm_Pestaña_1_4[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_Fecha_Venta_Venta.move(150, 100)
        
        # Instanciar Widget
        self.de_Modificar_Fecha_Venta_Venta = QDateEdit(self.lst_frm_Pestaña_1_4[1].widget(2))
        # Tamaño & Posicion De Widget
        self.de_Modificar_Fecha_Venta_Venta.setFixedSize(350, 20), self.de_Modificar_Fecha_Venta_Venta.move(300, 100)
        # Mostrar Calendario
        self.de_Modificar_Fecha_Venta_Venta.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Modificar_Fecha_Venta_Venta.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Modificar_Fecha_Venta_Venta.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Modificar_Fecha_Venta_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Sucursal_Venta = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Sucursal_Venta.move(150, 130)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Sucursal_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Sucursal_Venta.setFixedSize(350, 20), self.txt_Modificar_ID_Sucursal_Venta.move(300, 130)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Sucursal_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Modificar_ID_Cliente_Venta = QLabel('ID De Cliente',self.lst_frm_Pestaña_1_4[1].widget(2))
        # Posicion De Widget
        self.lbl_Modificar_ID_Cliente_Venta.move(150, 160)
        
        # Instanciar Widget
        self.txt_Modificar_ID_Cliente_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(2))
        # Tamaño & Posicion De Widget
        self.txt_Modificar_ID_Cliente_Venta.setFixedSize(350, 20), self.txt_Modificar_ID_Cliente_Venta.move(300, 160)
        #Inhabilitar Widget
        self.txt_Modificar_ID_Cliente_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Modificar_Aniadir_Venta = QPushButton('Modificar', self.lst_frm_Pestaña_1_4[1].widget(2))
        # Tamaño & Posicion De Widget
        self.btn_Modificar_Aniadir_Venta.setFixedSize(150, 20), self.btn_Modificar_Aniadir_Venta.move(342, 340)
        # Estilo De Widget
        self.btn_Modificar_Aniadir_Venta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Modificar_Aniadir_Venta.clicked.connect(self.obtener_Datos_InvSuc_1_1_1)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Eliminar_Titulo_Venta = QLabel('Eliminar Venta',self.lst_frm_Pestaña_1_4[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Titulo_Venta.move(380, 30)
        
        # Instanciar Widget
        self.lbl_Eliminar_Busqueda_ID_Venta = QLabel('Busqueda Por ID', self.lst_frm_Pestaña_1_4[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Busqueda_ID_Venta.move(150, 70)
        
        # Instanciar Widget
        self.txt_Eliminar_Busqueda_ID_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(3))
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Eliminar_Busqueda_ID_Venta.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_Busqueda_ID_Venta.setFixedSize(190, 20), self.txt_Eliminar_Busqueda_ID_Venta.move(300, 70)
        
        # Instanciar Widget
        self.btn_Eliminar_Busqueda_ID_Venta = QPushButton('Buscar', self.lst_frm_Pestaña_1_4[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Busqueda_ID_Venta.setFixedSize(150, 20), self.btn_Eliminar_Busqueda_ID_Venta.move(500, 70)
        # Estilo De Widget
        self.btn_Eliminar_Busqueda_ID_Venta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Eliminar_Busqueda_ID_Venta.clicked.connect(self.buscar_Datos_Venta_1_1_3)
        
        # Instanciar Widget
        self.lbl_Eliminar_Fecha_Venta_Venta = QLabel('Fecha De Venta',self.lst_frm_Pestaña_1_4[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_Fecha_Venta_Venta.move(150, 100)
        
        # Instanciar Widget
        self.de_Eliminar_Fecha_Venta_Venta = QDateEdit(self.lst_frm_Pestaña_1_4[1].widget(3))
        # Tamaño & Posicion De Widget
        self.de_Eliminar_Fecha_Venta_Venta.setFixedSize(350, 20), self.de_Eliminar_Fecha_Venta_Venta.move(300, 100)
        # Mostrar Calendario
        self.de_Eliminar_Fecha_Venta_Venta.setCalendarPopup(True)
        # Mostrar Fecha Actual
        self.de_Eliminar_Fecha_Venta_Venta.setDate(QDate.currentDate())
        # Formato De Fecha
        self.de_Eliminar_Fecha_Venta_Venta.setDisplayFormat('yyyy/MM/dd')
        #Inhabilitar Widget
        self.de_Eliminar_Fecha_Venta_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Sucursal_Venta = QLabel('ID De Sucursal',self.lst_frm_Pestaña_1_4[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Sucursal_Venta.move(150, 130)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Sucursal_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Sucursal_Venta.setFixedSize(350, 20), self.txt_Eliminar_ID_Sucursal_Venta.move(300, 130)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Sucursal_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.lbl_Eliminar_ID_Cliente_Venta = QLabel('ID De Cliente',self.lst_frm_Pestaña_1_4[1].widget(3))
        # Posicion De Widget
        self.lbl_Eliminar_ID_Cliente_Venta.move(150, 160)
        
        # Instanciar Widget
        self.txt_Eliminar_ID_Cliente_Venta = QLineEdit(self.lst_frm_Pestaña_1_4[1].widget(3))
        # Tamaño & Posicion De Widget
        self.txt_Eliminar_ID_Cliente_Venta.setFixedSize(350, 20), self.txt_Eliminar_ID_Cliente_Venta.move(300, 160)
        #Inhabilitar Widget
        self.txt_Eliminar_ID_Cliente_Venta.setDisabled(True)
        
        # Instanciar Widget
        self.btn_Eliminar_Aniadir_Venta = QPushButton('Eliminar', self.lst_frm_Pestaña_1_4[1].widget(3))
        # Tamaño & Posicion De Widget
        self.btn_Eliminar_Aniadir_Venta.setFixedSize(150, 20), self.btn_Eliminar_Aniadir_Venta.move(342, 340)
        # Estilo De Widget
        self.btn_Eliminar_Aniadir_Venta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
       # =============================================================================
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_RegistroVenta = QLabel('Visualizar Tabla Registro De Ventas Por Sucursal', self.lst_frm_Ventanas_SubMenu_1_5[0])
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_RegistroVenta.move(20, 50)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_RegistroVenta = QLabel('Busqueda Por ID', self.lst_frm_Ventanas_SubMenu_1_5[0])
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_RegistroVenta.move(20, 70)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_RegistroVenta = QLineEdit(self.lst_frm_Ventanas_SubMenu_1_5[0])
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_RegistroVenta.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_RegistroVenta.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_RegistroVenta.move(110, 70)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_RegistroVenta = QPushButton('Buscar', self.lst_frm_Ventanas_SubMenu_1_5[0])
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_RegistroVenta.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_RegistroVenta.move(270, 70)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_RegistroVenta.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_RegistroVenta.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_RegistroVenta_Nombres = [
            'Sucursal',
            'Total De Producto',
            'Monto Total'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_RegistroVenta = QTableWidget(self.lst_frm_Ventanas_SubMenu_1_5[0])
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_RegistroVenta.setFixedSize(814, 360), self.tblw_Leer_Tabla_RegistroVenta.move(20, 100)
        # Estilo De Widget
        self.tblw_Leer_Tabla_RegistroVenta.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_RegistroVenta.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_RegistroVenta.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_RegistroVenta.setColumnCount(len(self.lst_Leer_Tabla_RegistroVenta_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_RegistroVenta.setHorizontalHeaderLabels(self.lst_Leer_Tabla_RegistroVenta_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_RegistroVenta.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_RegistroVenta.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.vista_ventas_por_sucursal()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_RegistroVenta.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_RegistroVenta.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_CambiosPrecio = QLabel('Visualizar Tabla Del Registro De Cambio De Precios', self.lst_frm_Ventanas_SubMenu_1_5[1])
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_CambiosPrecio.move(20, 50)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_CambiosPrecio = QLabel('Busqueda Por ID', self.lst_frm_Ventanas_SubMenu_1_5[1])
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_CambiosPrecio.move(20, 70)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_CambiosPrecio = QLineEdit(self.lst_frm_Ventanas_SubMenu_1_5[1])
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_CambiosPrecio.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_CambiosPrecio.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_CambiosPrecio.move(110, 70)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_CambiosPrecio = QPushButton('Buscar', self.lst_frm_Ventanas_SubMenu_1_5[1])
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_CambiosPrecio.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_CambiosPrecio.move(270, 70)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_CambiosPrecio.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_CambiosPrecio.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_CambiosPrecio_Nombres = [
            'Producto',
            'Precio Previo',
            'Precio Actual',
            'Fecha De Cambio'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_CambiosPrecio = QTableWidget(self.lst_frm_Ventanas_SubMenu_1_5[1])
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_CambiosPrecio.setFixedSize(814, 360), self.tblw_Leer_Tabla_CambiosPrecio.move(20, 100)
        # Estilo De Widget
        self.tblw_Leer_Tabla_CambiosPrecio.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_CambiosPrecio.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_CambiosPrecio.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_CambiosPrecio.setColumnCount(len(self.lst_Leer_Tabla_CambiosPrecio_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_CambiosPrecio.setHorizontalHeaderLabels(self.lst_Leer_Tabla_CambiosPrecio_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_CambiosPrecio.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_CambiosPrecio.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.vista_cambio_de_precios()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_CambiosPrecio.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_CambiosPrecio.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_DatosAlmacen = QLabel('Visualizar Tabla Del Registro De Inventario Por  Almacen', self.lst_frm_Ventanas_SubMenu_1_5[2])
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_DatosAlmacen.move(20, 50)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_DatosAlmacen = QLabel('Busqueda Por ID', self.lst_frm_Ventanas_SubMenu_1_5[2])
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_DatosAlmacen.move(20, 70)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_DatosAlmacen = QLineEdit(self.lst_frm_Ventanas_SubMenu_1_5[2])
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_DatosAlmacen.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_DatosAlmacen.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_DatosAlmacen.move(110, 70)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_DatosAlmacen = QPushButton('Buscar', self.lst_frm_Ventanas_SubMenu_1_5[2])
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_DatosAlmacen.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_DatosAlmacen.move(270, 70)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_DatosAlmacen.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''')
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_DatosAlmacen.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_DatosAlmacen_Nombres = [
            'Almacen',
            'Producto',
            'Cantidad'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_DatosAlmacen = QTableWidget(self.lst_frm_Ventanas_SubMenu_1_5[2])
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_DatosAlmacen.setFixedSize(814, 360), self.tblw_Leer_Tabla_DatosAlmacen.move(20, 100)
        # Estilo De Widget
        self.tblw_Leer_Tabla_DatosAlmacen.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_DatosAlmacen.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_DatosAlmacen.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_DatosAlmacen.setColumnCount(len(self.lst_Leer_Tabla_DatosAlmacen_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_DatosAlmacen.setHorizontalHeaderLabels(self.lst_Leer_Tabla_DatosAlmacen_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_DatosAlmacen.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_DatosAlmacen.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.vista_inventario_por_almacen()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_DatosAlmacen.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_DatosAlmacen.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        # Instanciar Widget
        self.lbl_Leer_Titulo_Tabla_DatosCliente = QLabel('Visualizar Tabla Del Registro De Datos De Clientes', self.lst_frm_Ventanas_SubMenu_1_5[3])
        # Posicion De Widget
        self.lbl_Leer_Titulo_Tabla_DatosCliente.move(20, 50)
        
        # Instanciar Widget
        self.lbl_Leer_Busqueda_ID_DatosCliente = QLabel('Busqueda Por ID', self.lst_frm_Ventanas_SubMenu_1_5[3])
        # Posicion De Widget
        self.lbl_Leer_Busqueda_ID_DatosCliente.move(20, 70)
        
        # Instanciar Widget
        self.txt_Leer_Busqueda_ID_DatosCliente = QLineEdit(self.lst_frm_Ventanas_SubMenu_1_5[3])
        # Texto Dentro Del LineEdit De Ejemplo
        self.txt_Leer_Busqueda_ID_DatosCliente.setPlaceholderText('Ingrese ID')
        # Tamaño & Posicion De Widget
        self.txt_Leer_Busqueda_ID_DatosCliente.setFixedSize(150, 20), self.txt_Leer_Busqueda_ID_DatosCliente.move(110, 70)
        
        # Instanciar Widget
        self.btn_Leer_Busqueda_ID_DatosCliente = QPushButton('Buscar', self.lst_frm_Ventanas_SubMenu_1_5[3])
        # Tamaño & Posicion De Widget
        self.btn_Leer_Busqueda_ID_DatosCliente.setFixedSize(150, 20), self.btn_Leer_Busqueda_ID_DatosCliente.move(270, 70)
        # Estilo De Widget
        self.btn_Leer_Busqueda_ID_DatosCliente.setStyleSheet('''
            QPushButton {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QPushButton:hover {
                /* Fondo */
                background-color: rgb(255, 255, 255); /* Color De Fondo */
                border: 1px solid rgb(75, 175, 80); /* Color De Borde */
                /* Letra */
                color: rgb(75, 175, 80); /* Color De Letra */
            }
            QPushButton:pressed {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
            }
        ''') 
        # Accion De Boton
        #self.btn_Leer_Busqueda_ID_DatosCliente.clicked.connect(self.buscar_Datos_Cliente_1_1_1)
        
        # Lista Nombre De Columnas
        self.lst_Leer_Tabla_DatosCliente_Nombres = [
            'Cliente ID',
            'Nombre',
            'Apellido Paterno',
            'Apellido Materno',
            'Fecha De Nacimiento',
            'Edad',
            'Calle',
            'Ciudad',
            'Estado',
            'Pais',
            'Codigo Postal'
        ]
        
        # Instanciar Widget
        self.tblw_Leer_Tabla_DatosCliente = QTableWidget(self.lst_frm_Ventanas_SubMenu_1_5[3])
        # Tamaño & Posicion De Widget
        self.tblw_Leer_Tabla_DatosCliente.setFixedSize(814, 360), self.tblw_Leer_Tabla_DatosCliente.move(20, 100)
        # Estilo De Widget
        self.tblw_Leer_Tabla_DatosCliente.setStyleSheet('''
            QTableWidget {
                /* Fondo */
                background-color: rgb(175, 175, 175); /* Color De Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
            }
            QHeaderView::section {
                /* Fondo */
                background-color: rgb(75, 175, 80); /* Color de fondo de los encabezados */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item {
                /* Fondo */
                border: 1px solid rgb(0, 0, 0); /* Color De Borde */
                /* Letra */
                color: rgb(0, 0, 0); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
            QTableWidget::item:selected {
                /* Fondo */
                background-color: #a0a0a0; /* Color De Fondo */
                /* Letra */
                color: rgb(255, 255, 255); /* Color De Letra */
                font-size: 11px; /* Tamaño De Letra */
            }
        ''')
        # No Poder Editar Tablas
        self.tblw_Leer_Tabla_DatosCliente.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # No Cambiar Tamaño De Filas
        self.tblw_Leer_Tabla_DatosCliente.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # Cantidad De Filas Conforme La Lista
        self.tblw_Leer_Tabla_DatosCliente.setColumnCount(len(self.lst_Leer_Tabla_DatosCliente_Nombres))
        # Poner Nombres De La Lista En Tabla
        self.tblw_Leer_Tabla_DatosCliente.setHorizontalHeaderLabels(self.lst_Leer_Tabla_DatosCliente_Nombres)
        # Mostrar Titulos De Fila Pero No Indice De Columna
        self.tblw_Leer_Tabla_DatosCliente.horizontalHeader().setVisible(True), self.tblw_Leer_Tabla_DatosCliente.verticalHeader().setVisible(False)
        # Obtener los registros de la base de datos
        registros = self.registro_datos.vista_datos_de_cliente()
        # Establecer la cantidad de filas en la tabla
        self.tblw_Leer_Tabla_DatosCliente.setRowCount(len(registros))

        # Llenar la tabla con los datos obtenidos
        for row_idx, row_data in enumerate(registros):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tblw_Leer_Tabla_DatosCliente.setItem(row_idx, col_idx, item)
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
        #[]===========================================================================================;
    
    def seleccion_MessageBox(self, idMB):
        if idMB == 0:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Bienvenido Al SMBD')
            msg_box.setText('Este Programa Es Para Administrar La Base De Datos De Nuestra Empresa\n'
                            'Por Favor Siga El Protocolo De La Empresa Y Evite Borrar La Base De Datos Sin Permiso\n'
                            'Si Ignora Lo Ultimo Sera Sancionado O Despedido En Dado Caso La Gravedad De Affeccion\n'
                            'Si Acepta Todo Esto Por Favor De En Continuar')
            msg_box_continue = msg_box.addButton('Continuar', QMessageBox.AcceptRole)
            msg_box.exec_()
        elif idMB == 1:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Error De Validacion De Datos')
            msg_box.setText('Por Favor Llene Todas Las Casillas Para Proseguir Con La Base De Datos')
            msg_box_accept = msg_box.addButton('Aceptar', QMessageBox.AcceptRole)
            msg_box.exec_()
        elif idMB == 2:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Error De Validacion De Datos')
            msg_box.setText('Por Favor Ingrese Los Datos Correctos Para Proseguir Con La Base De Datos')
            msg_box_accept = msg_box.addButton('Aceptar', QMessageBox.AcceptRole)
            msg_box.exec_()
        elif idMB == 3:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Error De Validacion De Datos')
            msg_box.setText('Por Favor Ingrese Nuevos Datos Datos, ID Ya Existente')
            msg_box_accept = msg_box.addButton('Aceptar', QMessageBox.AcceptRole)
            msg_box.exec_()
        elif idMB == 4:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Error De Validacion De Datos')
            msg_box.setText('Por Favor Ingrese Nuevos Datos Datos, ID No Existente')
            msg_box_accept = msg_box.addButton('Aceptar', QMessageBox.AcceptRole)
            msg_box.exec_()
            
    # Constructor
    def __init__ (self):
        # Para Hacer Herencia De QMainWindow
        super().__init__()
        # Nombre De Ventana
        self.setWindowTitle('Proyecto: Base De Datos')
        # Tamaño De Ventana
        self.setFixedSize(854, 480)
        # Invocar Funcion De Contenido
        self.contenido()

# Instanciar QApplication
aplicacion = QApplication(sys.argv)
# Instanciar Clase Interfaz
app = Portada()
# Mostrar Ventana
app.show()
# Evita Errores De Cierre
sys.exit(aplicacion.exec_())