import tkinter as tk
import os
import copy

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
        if (self.color == "B" and fila_o == 6) or (self.color == "N" and fila_o == 1):
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
        self.resaltados = {}
        self.resaltado_rey = {}
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
                    fill=color,outline=""
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
                    clase = {
                        "T": Torre, "A": Alfil, "C": Caballo,
                        "Q": Reina, "K": Rey, "P": Peon
                    }[pieza[0]](pieza[1])
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
            
            clase = {
                "T": Torre, "A": Alfil, "C": Caballo,
                "Q": Reina, "K": Rey, "P": Peon
            }[pieza[0]](pieza[1])

            self.pieza_seleccionada = (fila, col)

            # Calcular todos los movimientos válidos
            self.movimientos_validos = []
            for fila_d in range(8):
                for col_d in range(8):
                    destino = self.estructura.piezas[fila_d][col_d]
                    # Ignorar casillas con piezas propias
                    if destino != "--" and destino.endswith(self.turno):
                        continue
                    # Verificar si el movimiento es válido
                    if clase.movimiento_valido(fila, col, fila_d, col_d, self.estructura.piezas):
                        self.movimientos_validos.append((fila_d, col_d))

            # Llamar a la función visual para colorear opciones

            self.tablero.colorear_opciones(self.movimientos_validos)

            print(f"Pieza seleccionada: {pieza} ({fila},{col})")

    def mover(self, fila_d, col_d):
        f_o, c_o = self.pieza_seleccionada
        pieza = self.estructura.piezas[f_o][c_o]


        color = pieza[-1] #Accede a la última letra de pieza: "B" o "N"
        clase = {
            "T": Torre, "A": Alfil, "C": Caballo, "Q": Reina, "K": Rey, "P": Peon
        }[pieza[0]](color) #Le asignamos a la pieza la clase y color correspondiente

        pieza_destino = self.estructura.piezas[fila_d][col_d]

        if pieza_destino != "--" and pieza_destino.endswith(self.turno):
            self.tablero.colorear_opciones([])
            print("No podés moverte sobre una pieza aliada.")
            self.pieza_seleccionada = None
            return
        
            #llama al método de la clase correspondiente, lo cual tambien hereda el método camino_libre
        if clase.movimiento_valido(f_o, c_o, fila_d, col_d, self.estructura.piezas):

            copia_tablero = copy.deepcopy(self.estructura.piezas) #Hacemos copia para simular jaque
            copia_tablero[fila_d][col_d] = copia_tablero[f_o][c_o]
            copia_tablero[f_o][c_o] = "--"

            if self.es_jaque(tablero=copia_tablero, turno=self.turno):
                self.tablero.colorear_opciones([])
                self.pieza_seleccionada = None
                print("Movimiento ilegal: dejaría al rey en jaque.")
                return

            self.capturar_pieza(fila_d, col_d)  #Captura antes de mover
            self.aplicar_movimiento(f_o, c_o, fila_d, col_d, pieza)
            self.tablero.colorear_opciones([])

            # Verifica si el movimiento actual pone en jaque al rival
            color_rival = "N" if self.turno == "B" else "B"


            if self.es_jaque(tablero=self.estructura.piezas, turno=color_rival):
                if not self.puede_escapar(color_rival, self.estructura.piezas):
                    self.pieza_seleccionada = None
                    print("Jaque Mate!")
                else:
                    print("Rey en jaque")
            else:
                if not self.puede_escapar(color_rival, self.estructura.piezas):
                    print ("Rey ahogado")
            self.tablero.actualizar_jaque(self.estructura.piezas, color_rival)

            #Cambiar el turno
            self.turno = "N" if self.turno == "B" else "B"


        else:
            print("Movimiento inválido")

        self.pieza_seleccionada = None


    def capturar_pieza(self, fila, col):
        pieza_objetivo = self.estructura.piezas[fila][col]
        if pieza_objetivo != "--" and not pieza_objetivo.endswith(self.turno):
            #  Borrar la imagen visual de la pieza capturada
            if (fila, col) in self.tablero.ids:
                self.tablero.canvas.delete(self.tablero.ids[(fila, col)])
                del self.tablero.ids[(fila, col)]

            #  Borrar la pieza lógica
            self.estructura.piezas[fila][col] = "--"


    def aplicar_movimiento(self, f_o, c_o, f_d, c_d, pieza):
        # Actualiza el tablero lógico
        self.estructura.piezas[f_d][c_d] = pieza
        self.estructura.piezas[f_o][c_o] = "--"

        # Actualiza el tablero visual
        self.tablero.mover_pieza(f_o, c_o, f_d, c_d, pieza)

    def encontrar_rey(self, color, tablero):
        for fila, i in enumerate(tablero):
            for columna, j in enumerate(i):
                if j.startswith("K") and j.endswith(f"{color}"):
                    return fila, columna
        return None, None

    def es_jaque(self, tablero, turno):
        fila_rey, col_rey = self.encontrar_rey(turno, tablero)

        if fila_rey is None or col_rey is None:
        # El rey no está en el tablero, no tiene sentido seguir
            return False
        for fila_o, i in enumerate(tablero):
            for col_o, pieza in enumerate(i):
                if pieza != "--" and not pieza.endswith(turno):
                    clase = {
                        "T": Torre, "A": Alfil, "C": Caballo, "Q": Reina, "K": Rey, "P": Peon
                    }[pieza[0]](pieza[1])
                    if clase.movimiento_valido(fila_o, col_o, fila_rey, col_rey, tablero):
                        print(f"{pieza} {fila_o} {col_o} está amenazando al rey")
                        return True
        return False
    

    def puede_escapar(self, color_rival, tablero):
        for fila, fila_piezas in enumerate(tablero):
            for col, pieza in enumerate(fila_piezas):
                if pieza.endswith(color_rival):
                    clase = {
                        "T": Torre, "A": Alfil, "C": Caballo,
                        "Q": Reina, "K": Rey, "P": Peon
                    }[pieza[0]](color_rival)
                    
                    for fila_d in range(8):
                        for col_d in range(8):
                            copia_tablero = copy.deepcopy(tablero)

                            destino = copia_tablero[fila_d][col_d]
                        
                            # No podemos mover sobre pieza aliada
                            if destino != "--" and destino.endswith(color_rival):
                                continue
                                
                                # Simular movimiento
                            if clase.movimiento_valido(fila, col, fila_d, col_d, copia_tablero):
                                copia_tablero[fila_d][col_d] = copia_tablero[fila][col]
                                copia_tablero[fila][col] = "--"
                                    
                                if not self.es_jaque(tablero=copia_tablero, turno=color_rival):
                                    return True  # Hay escape posible
        return False  # Ningún movimiento salva al rey



    def run(self):
            self.ventana.mainloop()


# --------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------
if __name__ == "__main__":
    juego = Juego(96)
    juego.run()
