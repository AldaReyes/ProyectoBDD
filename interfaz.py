import tkinter as tk
from tkinter import ttk

class Interfaz():
    def panelSeleccionado(self, indice):
        def panelesInternos(indice):
            for panelActual1_1 in self.paneles1_1:
                panelActual1_1.place_forget()
            self.paneles1_1[indice].place(x = 20, y = 80, width = 630, height = 340)
            self.textoPanel1_1 = f'Area: '
                
        if indice < 4:
            for panelActual in self.paneles1:
                panelActual.place_forget()
            self.paneles1[indice].place(x = 150, y = 20, width = 670, height = 440)
            self.textoPanel1 = f'Area: '
            
            if indice == 0:
                self.paneles1_1 = []
                self.nombrePanel1_1 = ['Inventario de Almacenes', 'Inventario de Sucursales', 'Productos', 'Productos Vendidos']
                self.coloresPanel1_1 = ['red', 'lightgreen', 'lightpink']
                for nombre1_1, color1_1 in zip(self.nombrePanel1_1, self.coloresPanel1_1):
                    self.panel1_1 = tk.Frame(self.paneles1[indice], background = color1_1)
                    self.panel1_1.place(x = 20, y = 80, width = 630, height = 340)
                    self.panel1_1.place_forget()
                    self.paneles1_1.append(self.panel1_1)
                self.textoPanel1 += 'Inventarios'
                
                self.opcNombreCB = ttk.Combobox(self.paneles1[indice], values=self.nombrePanel1_1, state='readonly')
                self.opcNombreCB.place(x = 20, y = 50)
                self.opcNombreCB.bind("<<ComboboxSelected>>", lambda event, j=self.opcNombreCB: panelesInternos(j.current()))
                self.opcNombreCB.current(0)
                panelesInternos(0)
            elif indice == 1:
                self.paneles1_1 = []
                self.nombrePanel1_1 = ['Panel 1_1', 'Panel 2_2', 'Panel 3_3']
                self.coloresPanel1_1 = ['red', 'lightgreen', 'lightpink']
                for nombre1_1, color1_1 in zip(self.nombrePanel1_1, self.coloresPanel1_1):
                    self.panel1_1 = tk.Frame(self.paneles1[indice], background = color1_1)
                    self.panel1_1.place(x = 20, y = 80, width = 630, height = 340)
                    self.panel1_1.place_forget()
                    self.paneles1_1.append(self.panel1_1)
                self.textoPanel1 += 'Humano'
                
                self.opcNombreCB = ttk.Combobox(self.paneles1[indice], values=self.nombrePanel1_1, state='readonly')
                self.opcNombreCB.place(x = 20, y = 50)
                self.opcNombreCB.bind("<<ComboboxSelected>>", lambda event, j=self.opcNombreCB: panelesInternos(j.current()))
                self.opcNombreCB.current(0)
                panelesInternos(0)
            elif indice == 2:
                self.textoPanel1 += 'Localizaciones'
            elif indice == 3:
                self.textoPanel1 += 'Transacciones'

            self.nombrePanel = tk.Label(self.paneles1[indice], text = f'{self.textoPanel1}',background = self.coloresPanel[indice])
            self.nombrePanel.place(x = 20, y = 20)
        else:
            self.ventana.destroy()
        
    def contenido(self):
        self.paneles1 = []
        self.nombrePanel = ['Inventarios', 'Humano', 'Localizaciones','Transacciones']
        self.coloresPanel = ['lightblue', 'lightgreen','lightpink' , 'blue']
        for nombre, color in zip(self.nombrePanel, self.coloresPanel):
            self.panel = tk.Frame(self.ventana, background = color)
            self.panel.place(x = 150, y = 20, width = 670, height = 440)
            self.panel.place_forget()
            self.paneles1.append(self.panel)
        global nombreBotones 
        self.nombreBotones = ['Inventarios', 'Capital Humano', 'Localizaciones','Transacciones','Salir']
        
        for indice, nombre in enumerate(self.nombreBotones):
            self.botones1 = tk.Button(self.ventana, text = nombre, width = 15,command = lambda i = indice: self.panelSeleccionado(i))
            self.botones1.place(x = 20, y = 20 + (30 * indice))
    
    def __init__(self):
       self.ventana = tk.Tk()
       self.ventana.title('Inventario')
       self.width, self.height = 854,480
       self.ventana.geometry(f'{self.width}x{self.height}')
       #funciones de la interfaz
       self.contenido()
       #funciones de la interfaz
       self.ventana.mainloop()

app = Interfaz()
