import tkinter as tk
from utils import cargar_imagenes, definir_clase

# TABLERO VISUAL (TKINTER)
# --------------------------------------------------------------------
class Tablero:
    def __init__(self, frame, cuadrado, piezas):
        self.cuadrado = cuadrado
        self.frame = frame
        self.piezas = piezas
        self.imagenes = cargar_imagenes(carpeta="Piezas", tamanio_base= cuadrado)
        self.ids = {}
        self.resaltados = {}
        self.resaltado_rey = {}
        self.canvas = tk.Canvas(frame, width=cuadrado*8, height=cuadrado*8, highlightthickness=0)
        self.canvas.pack()
        self.dibujar_casillas()
        self.mostrar_piezas()

    def dibujar_casillas(self):
        for i in range(8):
            for j in range(8):
                color = "#ffe6de" if (i+j)%2==0 else "#87bac7"
                self.canvas.create_rectangle(
                    i*self.cuadrado, j*self.cuadrado,
                    (i+1)*self.cuadrado, (j+1)*self.cuadrado,
                    fill=color,outline=""
                )



    def mostrar_piezas(self):
        for f, fila in enumerate(self.piezas): #Iteramos lista por lista
            for c, pieza in enumerate(fila): #Iteramos elemento por elemento
                if pieza != "--":
                    self.ids[(f,c)] = self.canvas.create_image(
                        c*self.cuadrado, f*self.cuadrado, #Eje X e Y
                        image=self.imagenes[pieza], anchor="nw" #Accedemos a las claves de imagenes
                    )

    def colorear_opciones(self, movimiento_valido):
        for (fila, col), id in self.resaltados.items():
            self.canvas.delete(id)
        self.resaltados.clear()

        for fila, col in movimiento_valido:
            self.resaltados[(fila,col)] = self.canvas.create_rectangle(
                col*self.cuadrado, fila*self.cuadrado,
                (col+1)*self.cuadrado,(fila+1)*self.cuadrado,
                fill="yellow",
                stipple="gray25",
                outline="orange"
            )
    
    def colorear_jaque(self, f_rey, c_rey):

        self.resaltado_rey[f_rey,c_rey] = self.canvas.create_rectangle(
            c_rey*self.cuadrado, f_rey*self.cuadrado,
            (c_rey+1)*self.cuadrado, (f_rey+1)*self.cuadrado,
            fill="",
            outline="red",
            width=3
        )

    def actualizar_jaque(self, tablero, turno):
        """Actualiza el color de jaque según si el rey sigue amenazado."""
        color_rival = turno
        # Primero borramos cualquier resaltado previo
        for id in self.resaltado_rey.values():
            self.canvas.delete(id)
        self.resaltado_rey.clear()

        # Buscamos si el rey está en jaque
        f_rey = c_rey = None
        for fila, fila_piezas in enumerate(tablero):
            for col, pieza in enumerate(fila_piezas):
                if pieza.startswith("K") and pieza.endswith(color_rival):
                    f_rey, c_rey = fila, col
                    break
            if f_rey is not None:
                break
        if f_rey is None:
            return
            


        # Verificamos si está en jaque
        jaque = False
        for fila_o, fila_piezas in enumerate(tablero):
            for col_o, pieza in enumerate(fila_piezas):
                if pieza != "--" and not pieza.endswith(color_rival):
                    clase = definir_clase(pieza)

                    if clase.movimiento_valido(fila_o, col_o, f_rey, c_rey, tablero):
                        jaque = True
                        break
            if jaque:
                break

        if jaque:
            self.colorear_jaque(f_rey, c_rey)



    def mover_pieza(self, f_o, c_o, f_d, c_d, pieza):
        
        self.canvas.delete(self.ids[(f_o, c_o)])
        nueva_id = self.canvas.create_image(
            c_d*self.cuadrado, f_d*self.cuadrado,
            image=self.imagenes[pieza], anchor="nw"
        )
        del self.ids[(f_o, c_o)]
        self.ids[(f_d, c_d)] = nueva_id
