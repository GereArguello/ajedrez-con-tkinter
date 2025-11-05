from interfaz import Interfaz
from tablero import Tablero
from juego import Juego
from posiciones import Posiciones

if __name__ == "__main__":

    interfaz = Interfaz()

    tablero_visual = Tablero(interfaz.ventana, 96, piezas=Posiciones().piezas)

    juego = Juego(tablero_visual, interfaz)

    interfaz.ventana.mainloop()

    