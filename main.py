import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from tkinter.constants import END, DISABLED, NORMAL, HIDDEN

from analizador import obtener_estadisticas, obtener_texto
from graficos import obtener_diagrama
from modelos import Estadisticas



class AnalizadorDeTextos(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.fichero_seleccionado = None

        self.master = master
        self.pack(padx=20, pady=20)
        self.crear_menu()
        self.crear_componentes()
        self.posicionar_componentes()

    def crear_menu(self):
        """crea la barra de menu"""
        barra_menu = tk.Menu(self.master)

        # Menu archivo
        menu_archivo = tk.Menu(barra_menu, tearoff=0)
        menu_archivo.add_command(label='Abrir', command=self.abrir_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label='Salir', command=self.master.quit)
        barra_menu.add_cascade(label='Archivo', menu=menu_archivo)

        # Menu ayuda
        menu_ayuda = tk.Menu(barra_menu, tearoff=0)
        menu_ayuda.add_command(label='Acerca de', command=self.acerca_de)
        barra_menu.add_cascade(label='Ayuda', menu=menu_ayuda)

        self.master.config(menu=barra_menu)

    def acerca_de(self):
        """simple cuadro de dialogo para mostrar informacion acerca de la aplicacion"""
        messagebox.showinfo('Acerca de', 'Aplicacion de ejemplo usando tkinter')
    
    def crear_componentes(self):
        """crea los componentes y los mantiene a la espera de que se seleccione algun fichero"""
        self.label_principal = tk.Label(self, text='seleccione un fichero en el menu Archivo -> Abrir')
        # Etiqueta que se utilizara para mostrar la imagen del analisis en el fichero
        self.imagen_analisis = tk.Label(self)
        # Componentes de estadisticas
        self.num_palabras_lbl = tk.Label(self, text='Numero de palabras: ')
        self.num_palabras_val = tk.Label(self)
        self.num_lineas_lbl = tk.Label(self, text='numero de lineas: ')
        self.num_lineas_val = tk.Label(self)
        self.num_caracteres_lbl = tk.Label(self, text='numero de caracteres: ')
        self.num_caracteres_val = tk.Label(self)
        # Componente para ver el texto
        self.texto_del_fichero = scrolledtext.ScrolledText(self)
    
    def posicionar_componentes(self):
        """Posiciona los componentes en funcion de si se ha seleccionado un fichero para analizar
        o no"""
        if not self.fichero_seleccionado:
            self.label_principal.grid(column=0, row=0, rowspan=6, columnspan=5, pady=350)
        else:
            self.imagen_analisis.grid(column=0, row=0, rowspan=6, columnspan=4, sticky='nw')
            self.num_palabras_lbl.grid(column=4, row=0)
            self.num_palabras_val.grid(column=4, row=1)
            self.num_lineas_lbl.grid(column=4, row=2)
            self.num_lineas_val.grid(column=4, row=3)
            self.num_caracteres_lbl.grid(column=4, row=4)
            self.num_caracteres_val.grid(column=4, row=5)
            self.texto_del_fichero.grid(column=0, row=8, columnspan=6, pady=15)
    
    def abrir_archivo(self):
        """pide al urusario que seleccione un archivo de texto para analizarlo y mostrarlo en
        la aplicacion"""
        ruta_archivo = filedialog.askopenfilename(title='seleccione un fichero de texto',
                                                  filetypes=(('Texto', '*.txt'),))

        if ruta_archivo:
            self.fichero_seleccionado = ruta_archivo
            self.label_principal.destroy()
            info, ruta_imagen, texto_de_archivo = self.obtener_informacion_de_fichero(self.fichero_seleccionado)
            self.mostrar_informacion_estadistica(info)
            self.mostrar_imagen(ruta_imagen)
            self.mostrar_informacion_fichero(texto_de_archivo)
            self.posicionar_componentes()
    
    def obtener_informacion_de_fichero(self, ruta_archivo: str):
        """Analiza el fichero de texto y obtiene las estadisticas, genera la imagen y obtiene
        el texto"""
        info = obtener_estadisticas(ruta_archivo)
        ruta_a_imagen = obtener_diagrama(info.letras)
        texto_de_archivo = obtener_texto(ruta_archivo)
        return info, ruta_a_imagen, texto_de_archivo
    
    def mostrar_informacion_estadistica(self, info: Estadisticas):
        """Muestra el contenido obtenido tras el analisis del fichero en la aplicacion"""
        self.num_palabras_val.config(text=info.num_palabras)
        self.num_lineas_val.config(text=info.num_lineas)
        self.num_caracteres_val.config(text=info.num_caracteres)

    def mostrar_imagen(self, ruta_imagen):
        """Mostrando la imagen generada en la aplicacion"""
        img = tk.PhotoImage(file=ruta_imagen)
        # self.imagen_analisis = tk.Label(self, image=img)
        self.imagen_analisis.config(image=img)
        self.imagen_analisis.image = img  # Es necesario mantener una referencia
    
    def mostrar_informacion_fichero(self, texto_de_fichero):
        """Agrega el contenido del fichero al componente texto_del_fichero dejando el componente
        como solo lectura"""
        self.texto_del_fichero.config(state=NORMAL)
        self.texto_del_fichero.delete('1.0', END)
        self.texto_del_fichero.insert(END, texto_de_fichero)
        self.texto_del_fichero.config(state=DISABLED)

if __name__ == '__main__':
    raiz = tk.Tk()
    raiz.title('Analizador de textos')
    raiz.geometry("800x800")
    app = AnalizadorDeTextos(master=raiz)
    raiz.mainloop()
    