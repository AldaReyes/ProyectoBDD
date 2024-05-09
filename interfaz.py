import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class appWindow(QWidget):#Clase Que Hereda QWidget
    def __init__(self):#Constructor Base
        super().__init__()#Herencia De La Clase QWidget
        self.setWindowTitle('Area De Ventas')#Titulo De Ventana
        self.setFixedSize(854,480)#Posicion De La Ventana
        self.move((QApplication.primaryScreen().geometry().center()) - (self.frameGeometry().center()))#Centrar Ventana
        self.contenido()#Invocar Funcion
    
    def contenido(self):
        self.colorActual = None
        self.panelesGuardados_1 = []#Lista Vacia De Paneles
        self.panelesGuardados_1_1 = []#Lista Vacia De Paneles
        self.panelesGuardados_1_2 = []#Lista Vacia De Paneles
        self.panelesGuardados_1_3 = []#Lista Vacia De Paneles
        self.panelesGuardados_1_4 = []#Lista Vacia De Paneles
        
        self.nombreBotones_1 = ['Inventarios', 'Capital Humano', 'Localizaciones','Transacciones','Salir']#Lista De Nombres De Botones
        self.coloresBotones_1 = [QColor(200 + -(20 * (x + -1)), 200 + -(20 * (x + -1)), 200 + -(20 * (x + -1))) for x in range(len(self.nombreBotones_1))]#Lista De Colores De Botones
        
        for indexBoton_1, nombreBoton_1 in enumerate(self.nombreBotones_1):#Obtener Nombre Y ID De La Lista De Botones Con Enumerate
            self.boton_1 = QPushButton(f'{nombreBoton_1}',self)#Crear Boton
            self.boton_1.move(20,20 + (30 * indexBoton_1))#Coordenadas Del Boton
            self.boton_1.setFixedSize(100,20)#Tamaño De Boton
            self.colorActual = self.coloresBotones_1[indexBoton_1] if indexBoton_1 < len(self.coloresBotones_1) else QColor(0, 0, 0)#Distribucion De Colores
            self.boton_1.setStyleSheet(f'background-color: {self.colorActual.name()}; border: 1px solid black;')#Color Y Margen
            self.boton_1.clicked.connect(lambda _, id = indexBoton_1: self.selectPaneles1(id))#Eventos De Boton Con ID
        
        for nombreBoton_1, colorPanel_1 in zip(self.nombreBotones_1,self.coloresBotones_1):#Ciclo Para Emparejar Listas
            self.paneles_1 = QFrame(self)#Añadir En Panel Principal
            self.paneles_1.setFrameShape(QFrame.StyledPanel)#Definir Bordes
            self.paneles_1.move(140,20)#Posicion De Panel
            self.paneles_1.setFixedSize(690,440)#Definir Tamaño
            self.paneles_1.setStyleSheet(f'background-color: {colorPanel_1.name()}; border: 1px solid black;')#Definir Color Y Estilo
            self.paneles_1.hide()#Esconder Paneles
            self.panelesGuardados_1.append(self.paneles_1)#Añadir A Lista 1_1
            
        self.nombreBotones_1_1 = ['Crear','Leer','Actualizar','Eliminar']#Lista De Nombres De Botones
        self.coloresBotones_1_1 = [QColor(200 + -(20 * (x + -1)), 200 + -(20 * (x + -1)), 200 + -(20 * (x + -1))) for x in range(len(self.nombreBotones_1_1))]#Lista De Colores De Botones
        
        for nombreBoton_1_1, colorPanel_1_1 in zip(self.nombreBotones_1_1,self.coloresBotones_1_1):#Ciclo Para Emparejar Listas
            self.paneles_1_1 = QFrame(self.panelesGuardados_1[0])#Añadir En Panel 1 
            self.paneles_1_1.setFrameShape(QFrame.StyledPanel)#Definir Bordes
            self.paneles_1_1.move(20,80)#Posicion De Panel
            self.paneles_1_1.setFixedSize(650,340)#Definir Tamaño
            self.paneles_1_1.setStyleSheet(f'background-color: {colorPanel_1_1.name()}; border: 1px solid black;')#Definir Color Y Estilo
            self.paneles_1_1.hide()#Esconder Paneles
            self.panelesGuardados_1_1.append(self.paneles_1_1)#Añadir A Lista 1_1
            
        self.comboBoxPanel_1_1 = QComboBox(self.panelesGuardados_1[0])#Añadir En Panel 1_1
        self.comboBoxPanel_1_1.addItems(self.nombreBotones_1_1)#Añadir Items De Lista
        self.comboBoxPanel_1_1.move(20, 40)#Posicion De ComboBox
        self.comboBoxPanel_1_1.setFixedSize(80, 20)#Definir Tamaño
        self.comboBoxPanel_1_1.currentIndexChanged.connect(self.selectPaneles1_1)#Cuando Cambie De Opcion Cambia De Pestaña
        
        #self.ingresarNombre = QLineEdit(self.panelesGuardados_1_1[0])
        #self.panelesGuardados_1_1[0].setLayout(QVBoxLayout())
        
        for nombreBoton_1_2, colorPanel_1_2 in zip(self.nombreBotones_1_1,self.coloresBotones_1_1):#Ciclo Para Emparejar Listas
            self.paneles_1_2 = QFrame(self.panelesGuardados_1[1])#Añadir En Panel 1 
            self.paneles_1_2.setFrameShape(QFrame.StyledPanel)#Definir Bordes
            self.paneles_1_2.move(20,80)#Posicion De Panel
            self.paneles_1_2.setFixedSize(650,340)#Definir Tamaño
            self.paneles_1_2.setStyleSheet(f'background-color: {colorPanel_1_2.name()}; border: 1px solid black;')#Definir Color Y Estilo
            self.paneles_1_2.hide()#Esconder Paneles
            self.panelesGuardados_1_2.append(self.paneles_1_2)#Añadir A Lista 1_2
            
        self.comboBoxPanel_1_2 = QComboBox(self.panelesGuardados_1[1])#Añadir En Panel 1_2
        self.comboBoxPanel_1_2.addItems(self.nombreBotones_1_1)#Añadir Items De Lista
        self.comboBoxPanel_1_2.move(20, 40)#Posicion De ComboBox
        self.comboBoxPanel_1_2.setFixedSize(80, 20)#Definir Tamaño
        self.comboBoxPanel_1_2.currentIndexChanged.connect(self.selectPaneles1_2)#Cuando Cambie De Opcion Cambia De Pestaña
        
        for nombreBoton_1_3, colorPanel_1_3 in zip(self.nombreBotones_1_1,self.coloresBotones_1_1):#Ciclo Para Emparejar Listas
            self.paneles_1_3 = QFrame(self.panelesGuardados_1[2])#Añadir En Panel 1 
            self.paneles_1_3.setFrameShape(QFrame.StyledPanel)#Definir Bordes
            self.paneles_1_3.move(20,80)#Posicion De Panel
            self.paneles_1_3.setFixedSize(650,340)#Definir Tamaño
            self.paneles_1_3.setStyleSheet(f'background-color: {colorPanel_1_3.name()}; border: 1px solid black;')#Definir Color Y Estilo
            self.paneles_1_3.hide()#Esconder Paneles
            self.panelesGuardados_1_3.append(self.paneles_1_3)#Añadir A Lista 1_3
            
        self.comboBoxPanel_1_3 = QComboBox(self.panelesGuardados_1[2])#Añadir En Panel 1_3
        self.comboBoxPanel_1_3.addItems(self.nombreBotones_1_1)#Añadir Items De Lista
        self.comboBoxPanel_1_3.move(20, 40)#Posicion De ComboBox
        self.comboBoxPanel_1_3.setFixedSize(80, 20)#Definir Tamaño
        self.comboBoxPanel_1_3.currentIndexChanged.connect(self.selectPaneles1_3)#Cuando Cambie De Opcion Cambia De Pestaña
        
        for nombreBoton_1_4, colorPanel_1_4 in zip(self.nombreBotones_1_1,self.coloresBotones_1_1):#Ciclo Para Emparejar Listas
            self.paneles_1_4 = QFrame(self.panelesGuardados_1[3])#Añadir En Panel 1 
            self.paneles_1_4.setFrameShape(QFrame.StyledPanel)#Definir Bordes
            self.paneles_1_4.move(20,80)#Posicion De Panel
            self.paneles_1_4.setFixedSize(650,340)#Definir Tamaño
            self.paneles_1_4.setStyleSheet(f'background-color: {colorPanel_1_4.name()}; border: 1px solid black;')#Definir Color Y Estilo
            self.paneles_1_4.hide()#Esconder Paneles
            self.panelesGuardados_1_4.append(self.paneles_1_4)#Añadir A Lista 1_4
            
        self.comboBoxPanel_1_4 = QComboBox(self.panelesGuardados_1[3])#Añadir En Panel 1_4
        self.comboBoxPanel_1_4.addItems(self.nombreBotones_1_1)#Añadir Items De Lista
        self.comboBoxPanel_1_4.move(20, 40)#Posicion De ComboBox
        self.comboBoxPanel_1_4.setFixedSize(80, 20)#Definir Tamaño
        self.comboBoxPanel_1_4.currentIndexChanged.connect(self.selectPaneles1_4)#Cuando Cambie De Opcion Cambia De Pestaña
        
        self.selectPaneles1_1(0)
        self.selectPaneles1_2(0)
        self.selectPaneles1_3(0)
        self.selectPaneles1_4(0)
        
        for i in range(len(self.panelesGuardados_1)):#Ciclo Para Titulo De Areas En Cada Panel_1
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1[i]}',self.panelesGuardados_1[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
            
        for i in range(len(self.panelesGuardados_1_1)):#Ciclo Para Titulo De ComboBox En Cada Panel_1_1
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1_1[i]}',self.panelesGuardados_1_1[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
        for i in range(len(self.panelesGuardados_1_2)):#Ciclo Para Titulo De ComboBox En Cada Panel_1_1
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1_1[i]}',self.panelesGuardados_1_2[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
        for i in range(len(self.panelesGuardados_1_3)):#Ciclo Para Titulo De ComboBox En Cada Panel_1_1
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1_1[i]}',self.panelesGuardados_1_3[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
        for i in range(len(self.panelesGuardados_1_4)):#Ciclo Para Titulo De ComboBox En Cada Panel_1_1
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1_1[i]}',self.panelesGuardados_1_4[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
        
    def cajaMensajes(self, x):
        if x == 1:
            cajaMensaje_1 = QMessageBox()#Mensaje De Cajita
            cajaMensaje_1.setWindowTitle('Bienvenido')#Titulo De Cajita
            cajaMensaje_1.setText('Ponga Aceptar Para Continuar')#Mensaje De Cajita
            botonMensaje_1 = QPushButton('Aceptar', cajaMensaje_1)#Boton De Cajita
            cajaMensaje_1.addButton(botonMensaje_1, QMessageBox.AcceptRole)#Añadir Boton A Cajita
            cajaMensaje_1.exec_()#Iniciar Cajita
    
    def selectPaneles1(self, id):
        for panel in self.panelesGuardados_1:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1) + -1):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1[id] #Selecciona El Panel Con El ID
            
            panelActual.show()#Mostrar Panel Selecionado
        else:
            self.close()

    def selectPaneles1_1(self, id):
        for panel in self.panelesGuardados_1_1:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1_1)):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1_1[id]#Selecciona El Panel Con El ID
            panelActual.show()#Mostrar Panel Selecionado

    def selectPaneles1_2(self, id):
        for panel in self.panelesGuardados_1_2:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1_2)):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1_2[id]#Selecciona El Panel Con El ID
            panelActual.show()#Mostrar Panel Selecionado

    def selectPaneles1_3(self, id):
        for panel in self.panelesGuardados_1_3:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1_3)):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1_3[id]#Selecciona El Panel Con El ID
            panelActual.show()#Mostrar Panel Selecionado

    def selectPaneles1_4(self, id):
        for panel in self.panelesGuardados_1_4:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1_4)):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1_4[id]#Selecciona El Panel Con El ID
            panelActual.show()#Mostrar Panel Selecionado

app = QApplication(sys.argv)#Aplicacion PyQT
aplicacion = appWindow()#Crear Instancia
aplicacion.show()#Mostrar ventana

aplicacion.cajaMensajes(1)#MessageBox De Ejemplo

sys.exit(app.exec_())#Ejecutar la aplicación