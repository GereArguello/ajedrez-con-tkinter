import tkinter as tk
import os

# --------------------------------------------------------------------
# ESTRUCTURA INICIAL DEL TABLERO
# --------------------------------------------------------------------
class Posiciones:
    def __init__(self):
        self.piezas = [
            ["TN","CN","AN","QN","KN","AN","CN","TN"],
            ["PN","PN","PN","PN","PN","PN","PN","PN"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["PB","PB","PB","PB","PB","PB","PB","PB"],
            ["TB","CB","AB","QB","KB","AB","CB","TB"],
        ]


# --------------------------------------------------------------------
# CLASES DE PIEZAS Y VALIDACIÓN DE MOVIMIENTOS
# --------------------------------------------------------------------
class Pieza:
    def __init__(self, color):
        self.color = color  # "B" o "N"

    def camino_libre(self, fila_o, col_o, fila_d, col_d, piezas):
        """Comprueba que no haya piezas entre origen y destino (excepto caballo)."""
        if fila_o == fila_d:  # Movimiento horizontal
            paso = 1 if col_d > col_o else -1
            for c in range(col_o + paso, col_d, paso):
                if piezas[fila_o][c] != "--":
                    return False
        elif col_o == col_d:  # Movimiento vertical
            paso = 1 if fila_d > fila_o else -1
            for f in range(fila_o + paso, fila_d, paso):
                if piezas[f][col_o] != "--":
                    return False
        elif abs(fila_d - fila_o) == abs(col_d - col_o):  # Diagonal
            paso_f = 1 if fila_d > fila_o else -1
            paso_c = 1 if col_d > col_o else -1
            f, c = fila_o + paso_f, col_o + paso_c
            while f != fila_d and c != col_d:
                if piezas[f][c] != "--":
                    return False
                f += paso_f
                c += paso_c
        return True


class Torre(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        return (fila_o == fila_d or col_o == col_d) and self.camino_libre(fila_o, col_o, fila_d, col_d, piezas)


class Alfil(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        return abs(fila_d - fila_o) == abs(col_d - col_o) and self.camino_libre(fila_o, col_o, fila_d, col_d, piezas)


class Caballo(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        return (abs(fila_d - fila_o), abs(col_d - col_o)) in [(1, 2), (2, 1)]


class Reina(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        dif_f = abs(fila_d - fila_o)
        dif_c = abs(col_d - col_o)
        recta = fila_o == fila_d or col_o == col_d
        diagonal = dif_f == dif_c
        return (recta or diagonal) and self.camino_libre(fila_o, col_o, fila_d, col_d, piezas)


class Rey(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        return abs(fila_d - fila_o) <= 1 and abs(col_d - col_o) <= 1


class Peon(Pieza):
    def movimiento_valido(self, fila_o, col_o, fila_d, col_d, piezas):
        direccion = -1 if self.color == "B" else 1
        #Primer movimiento
        if fila_o == 1 or fila_o == 6:
            if col_o == col_d and piezas[fila_d][col_d] == "--":
                if fila_d - fila_o == direccion or fila_d - fila_o == direccion*2:
                    return True and self.camino_libre(fila_o, col_o, fila_d, col_d, piezas)
        # Movimiento simple
        if col_o == col_d and piezas[fila_d][col_d] == "--":
            if fila_d - fila_o == direccion:
                return True
        # Captura
        if abs(col_d - col_o) == 1 and fila_d - fila_o == direccion and piezas[fila_d][col_d] != "--":
            return True
        return False


# --------------------------------------------------------------------
# TABLERO VISUAL (TKINTER)
# --------------------------------------------------------------------
class Tablero:
    def __init__(self, ventana, cuadrado, piezas):
        self.cuadrado = cuadrado
        self.ventana = ventana
        self.piezas = piezas
        self.ids = {}
        self.canvas = tk.Canvas(ventana, width=cuadrado*8, height=cuadrado*8)
        self.canvas.pack()
        self.dibujar_casillas()
        self.cargar_imagenes()
        self.mostrar_piezas()

    def dibujar_casillas(self):
        for i in range(8):
            for j in range(8):
                color = "#ffe6de" if (i+j)%2==0 else "#87bac7"
                self.canvas.create_rectangle(
                    i*self.cuadrado, j*self.cuadrado,
                    (i+1)*self.cuadrado, (j+1)*self.cuadrado,
                    fill=color
                )

    def cargar_imagenes(self):
        carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Piezas") #Ruta absoluta, se vería algo así C:\Users\usuario\Desktop\Ajedrez\Main\Piezas
        self.imagenes = {}
        nombres = ["AB","AN","CB","CN","KB","KN","PB","PN","QB","QN","TB","TN"] #Mismos códigos que los archivos '.png'
        for nombre in nombres:
            ruta = os.path.join(carpeta, nombre + ".png")
            if os.path.exists(ruta):
                img = tk.PhotoImage(file=ruta)
                factor = max(1, img.width() // self.cuadrado) #Fórmula para decidir cuánto reducir la imagen
                self.imagenes[nombre] = img.subsample(factor, factor)

    def mostrar_piezas(self):
        for f, fila in enumerate(self.piezas):
            for c, pieza in enumerate(fila):
                if pieza != "--":
                    self.ids[(f,c)] = self.canvas.create_image(
                        c*self.cuadrado, f*self.cuadrado,
                        image=self.imagenes[pieza], anchor="nw"
                    )

    def mover_pieza(self, f_o, c_o, f_d, c_d, pieza):
        
        self.canvas.delete(self.ids[(f_o, c_o)])
        nueva_id = self.canvas.create_image(
            c_d*self.cuadrado, f_d*self.cuadrado,
            image=self.imagenes[pieza], anchor="nw"
        )
        del self.ids[(f_o, c_o)]
        self.ids[(f_d, c_d)] = nueva_id


            # self.canvas.delete(self.ids[(fila, col)])
            # del self.ids[(fila, col)]



# --------------------------------------------------------------------
# LÓGICA DEL JUEGO
# --------------------------------------------------------------------
class Juego:
    def __init__(self, cuadrado):
        self.cuadrado = cuadrado
        self.estructura = Posiciones()
        self.turno = "B"
        self.pieza_seleccionada = None

        self.ventana = tk.Tk()
        self.ventana.title("Ajedrez")
        self.ventana.resizable(0, 0)
        self.tablero = Tablero(self.ventana, cuadrado, self.estructura.piezas)
        self.tablero.canvas.bind("<Button-1>", self.clic)

    def clic(self, evento):
        fila = evento.y // self.cuadrado
        col = evento.x // self.cuadrado
        print(f"({fila},{col})")
        if self.pieza_seleccionada is None:
            self.seleccionar(fila, col)
        else:
            self.mover(fila, col)

    def seleccionar(self, fila, col):
        pieza = self.estructura.piezas[fila][col]
        if pieza != "--" and pieza.endswith(self.turno):
            self.pieza_seleccionada = (fila, col)
            print(f"Pieza seleccionada: {pieza} ({fila},{col})")

    def mover(self, fila_d, col_d):
        f_o, c_o = self.pieza_seleccionada
        pieza = self.estructura.piezas[f_o][c_o]
        color = pieza[-1]
        clase = {
            "T": Torre, "A": Alfil, "C": Caballo, "Q": Reina, "K": Rey, "P": Peon
        }[pieza[0]](color)

        pieza_destino = self.estructura.piezas[fila_d][col_d]

        if pieza_destino != "--" and pieza_destino.endswith(self.turno):
            print("No podés moverte sobre una pieza aliada.")
            self.pieza_seleccionada = None
            return

        if clase.movimiento_valido(f_o, c_o, fila_d, col_d, self.estructura.piezas):
            self.capturar_pieza(fila_d, col_d)  # 👈 Captura antes de mover
            self.aplicar_movimiento(f_o, c_o, fila_d, col_d, pieza)
            self.turno = "N" if self.turno == "B" else "B"
        else:
            print("Movimiento inválido")

        self.pieza_seleccionada = None


    def capturar_pieza(self, fila, col):
        pieza_objetivo = self.estructura.piezas[fila][col]
        if pieza_objetivo != "--" and not pieza_objetivo.endswith(self.turno):
            # 🔹 Borrar la imagen visual de la pieza capturada
            if (fila, col) in self.tablero.ids:
                self.tablero.canvas.delete(self.tablero.ids[(fila, col)])
                del self.tablero.ids[(fila, col)]

            # 🔹 Borrar la pieza lógica
            self.estructura.piezas[fila][col] = "--"


    def aplicar_movimiento(self, f_o, c_o, f_d, c_d, pieza):
        # Actualiza el tablero lógico
        self.estructura.piezas[f_d][c_d] = pieza
        self.estructura.piezas[f_o][c_o] = "--"

        # Actualiza el tablero visual
        self.tablero.mover_pieza(f_o, c_o, f_d, c_d, pieza)

    def run(self):
            self.ventana.mainloop()


# --------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------
if __name__ == "__main__":
    juego = Juego(96)
    juego.run()
