import tkinter as tk
import os
from piezas import Torre, Alfil, Caballo, Reina, Rey, Peon


def cargar_imagenes(carpeta="Piezas", tamanio_base=64):
    ruta_carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), carpeta)
    nombres = ["AB","AN","CB","CN","KB","KN","PB","PN","QB","QN","TB","TN"]
    imagenes = {}

    for nombre in nombres:
        ruta = os.path.join(ruta_carpeta, nombre + ".png")
        if os.path.exists(ruta):
            img = tk.PhotoImage(file=ruta)
            factor = max(1, img.width() // tamanio_base)
            imagenes[nombre] = img.subsample(factor, factor)

    return imagenes

def obtener_fila_columna(evento, tam_cuadro):
    fila = evento.y // tam_cuadro
    col = evento.x // tam_cuadro
    return fila, col

def definir_clase(pieza):
    clase = {
        "T": Torre, "A": Alfil, "C": Caballo,
        "Q": Reina, "K": Rey, "P": Peon
    }[pieza[0]](pieza[-1])
    return clase