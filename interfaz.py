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
        self.panelesGuardados_2 = []#Lista Vacia De Paneles
        
        self.nombreBotones_1 = ['Inventarios', 'Capital Humano', 'Localizaciones','Transacciones','Salir']#Lista De Nombres De Botones
        self.coloresBotones_1 = [QColor(200 + -(20 * (x + -1)), 200 + -(20 * (x + -1)), 200 + -(20 * (x + -1))) for x in range(len(self.nombreBotones_1))]#Lista De Colores De Botones
        
        for indexBoton_1, nombreBoton_1 in enumerate(self.nombreBotones_1):#Obtener Nombre Y ID De La Lista De Botones Con Enumerate
            self.boton_1 = QPushButton(f'{nombreBoton_1}',self)#Crear Boton
            self.boton_1.move(20,20 + (30 * indexBoton_1))#Coordenadas Del Boton
            self.boton_1.setFixedSize(100,20)#Tamaño De Boton
            self.colorActual = self.coloresBotones_1[indexBoton_1] if indexBoton_1 < len(self.coloresBotones_1) else QColor(0, 0, 0)#Distribucion De Colores
            self.boton_1.setStyleSheet(f'background-color: {self.colorActual.name()}; border: 1px solid black;')#Color Y Margen
            self.boton_1.clicked.connect(lambda _, id = indexBoton_1: self.selectPaneles1(id))#Eventos De Boton Con ID
        
        for nombreBoton_1, colorPanel_1 in zip(self.nombreBotones_1,self.coloresBotones_1):#
            self.frame_1 = QFrame(self)
            self.frame_1.setFrameShape(QFrame.StyledPanel)
            self.frame_1.move(140,20)
            self.frame_1.setFixedSize(690,440)
            self.frame_1.setStyleSheet(f'background-color: {colorPanel_1.name()}; border: 1px solid black;')  # Acceder al nombre del color
            self.frame_1.hide()
            self.panelesGuardados_1.append(self.frame_1)
            
        self.nombreBotones_2 = ['Crear','Leer','Actualizar','Eliminar']#Lista De Nombres De Botones
        self.coloresBotones_2 = [QColor(200 + -(20 * (x + -1)), 200 + -(20 * (x + -1)), 200 + -(20 * (x + -1))) for x in range(len(self.nombreBotones_2))]#Lista De Colores De Botones
        
        for nombreBoton_2, colorPanel_2 in zip(self.nombreBotones_2,self.coloresBotones_2):#
            self.frame_2 = QFrame(self.panelesGuardados_1[1])
            self.frame_2.setFrameShape(QFrame.StyledPanel)
            self.frame_2.move(20,100)
            self.frame_2.setFixedSize(550,320)
            self.frame_2.setStyleSheet(f'background-color: {colorPanel_2.name()}; border: 1px solid black;')
            self.frame_2.hide()
            self.panelesGuardados_2.append(self.frame_2)
            
        self.comboBoxPanel_1 = QComboBox(self.panelesGuardados_1[1])
        self.comboBoxPanel_1.addItems(self.nombreBotones_2)
        self.comboBoxPanel_1.move(20, 40)
        self.comboBoxPanel_1.setFixedSize(80, 20)
        self.comboBoxPanel_1.currentIndexChanged.connect(self.selectPaneles2)
        
        self.selectPaneles2(0)
        
        for i in range(len(self.panelesGuardados_1)):
            self.titulo_1 = QLabel(f'Area: {self.nombreBotones_1[i]}',self.panelesGuardados_1[i])#Crear Label
            self.titulo_1.move(20, 20)#Posicion Del widget
            self.titulo_1.setStyleSheet(f'border: 0px;')#Sin Bordes
        
        self.texto_2 = QLabel('Amdios Tonotos',self.panelesGuardados_2[1])
        self.texto_2.move(20, 20)
        self.texto_2.setStyleSheet(f'border: 0px;')
        
    def cajaMensajes(self, x):
        if x == 1:
            cajaMensaje_1 = QMessageBox()
            cajaMensaje_1.setWindowTitle('Bienvenido')
            cajaMensaje_1.setText('Ponga Aceptar Para Continuar')
            botonMensaje_1 = QPushButton('Aceptar', cajaMensaje_1)
            cajaMensaje_1.addButton(botonMensaje_1, QMessageBox.AcceptRole)
            cajaMensaje_1.exec_()
    
    def selectPaneles1(self, id):
        for panel in self.panelesGuardados_1:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_1) + -1):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_1[id] #Selecciona El Panel Con El ID
            
            panelActual.show()#Mostrar Panel Selecionado
        else:
            self.close()

    def selectPaneles2(self, id):
        for panel in self.panelesGuardados_2:#Ciclo En Todos Los Paneles
            panel.hide()#Oculta Los Paneles
        if id < (len(self.panelesGuardados_2)):#Si El Tamaño De La Lista Es Menor A La ID
            panelActual = self.panelesGuardados_2[id]#Selecciona El Panel Con El ID
            panelActual.show()#Mostrar Panel Selecionado
        else:
            pass

app = QApplication(sys.argv)#Aplicacion PyQT
aplicacion = appWindow()#Crear Instancia
aplicacion.show()#Mostrar ventana

aplicacion.cajaMensajes(1)#MessageBox De Ejemplo

sys.exit(app.exec_())#Ejecutar la aplicación