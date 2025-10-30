import tkinter as tk
import os
import copy

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


    @staticmethod
    def obtener_opciones_promocion(color):
        if color == "B":  # blancas
            return [
                ["--", "AB", "--"],
                ["QB", "--", "CB"],
                ["--", "TB", "--"],
            ]
        else:  # negras
            return [
                ["--", "AN", "--"],
                ["QN", "--", "CN"],
                ["--", "TN", "--"],
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

# -- INTERFAZ COMPLETA -- 

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ajedrez")
        self.ventana.geometry("770x920+100+50")
        self.ventana.resizable(0,0)



        # -- Imagenes --

        imagenes = cargar_imagenes()
        self.img_blancas = imagenes["PB"]
        self.img_negras = imagenes["PN"]


        # -- Frames main --
        self.main_frame = tk.Frame(self.ventana, bg="#bebebe")
        self.main_frame.pack(fill="both")


        # -- Contenedor central que agrupa las franjas y el tablero --
        self.centro_frame = tk.Frame(self.main_frame, bg="#347F9C")
        self.centro_frame.pack(expand=True, fill="both")

        # -- Franja superior --
        self.top_frame = tk.Frame(self.centro_frame, bg="#347F9C", height=70)
        self.top_frame.pack(side="top", fill="x")

        # Configurar columnas para centrar el label
        self.top_frame.columnconfigure(0, weight=1)  # botón izquierda
        self.top_frame.columnconfigure(1, weight=2)  # label centrado
        self.top_frame.columnconfigure(2, weight=1)  # cronómetro derecha

        # Botón a la izquierda
        self.boton_reinicio = tk.Button(
            self.top_frame, bg="#ff6b6b", text="Reiniciar",
            font=("Arial", 12, "bold"), width=9, height=3, bd=2,
            command=self.reiniciar_tablero, relief="solid"
        )
        self.boton_reinicio.grid(row=0, column=0, sticky="w")
        self.boton_reinicio.config(highlightbackground="black", highlightthickness=2)

        # Label centrado
        self.label_turno = tk.Label(
            self.top_frame, text="Turno de:", image=self.img_blancas,
            compound="right", font=("Arial", 24), bg="#347F9C"
        )
        self.label_turno.grid(row=0, column=1,padx=(0,70))

        # Cronómetro a la derecha

        # -- Contenedor del tablero (centrado) --
        self.frame_tablero = tk.Frame(
            self.centro_frame, 
            bg="#bebebe",        # color interno del frame
            bd=2,                # grosor del borde
            relief="solid",      # estilo de borde
            highlightbackground="black",  # color del borde en algunos sistemas
            highlightthickness=2          # grosor del borde visible
        )
        self.frame_tablero.pack(side="top")

        # -- Franja inferior simétrica --
        self.bottom_frame = tk.Frame(self.centro_frame, bg="#347F9C", height=75)
        self.bottom_frame.pack(side="bottom", fill="x")

        # -- Tablero Visual y Lógico --
        self.tablero = Tablero(self.frame_tablero, 96, piezas=Posiciones().piezas)
        self.juego = (Juego(self.tablero, self))

    def actualizar_turno(self, color):
        if color == "B":
            self.label_turno.config(text="Turno de:", image=self.img_blancas)
        else:
            self.label_turno.config(text="Turno de:", image=self.img_negras)

    def reiniciar_tablero(self):
        print("Botón clickeado")

        # Borrar imágenes viejas
        for id in self.tablero.ids.values():
            self.tablero.canvas.delete(id)
        self.tablero.ids.clear()

        # Borrar resaltados
        for id in self.tablero.resaltados.values():
            self.tablero.canvas.delete(id)
        self.tablero.resaltados.clear()
        for id in self.tablero.resaltado_rey.values():
            self.tablero.canvas.delete(id)
        self.tablero.resaltado_rey.clear()

        # Restaurar posiciones iniciales
        self.tablero.piezas = copy.deepcopy(Posiciones().piezas)

        # Resetear atributos del juego
        self.juego.estructura = Posiciones()
        self.juego.turno = "B"
        self.juego.pieza_seleccionada = None
        self.juego.piezas_eliminadas.clear()
        self.juego.movimientos_validos = []

        # Actualizar indicador de turno
        self.actualizar_turno(self.juego.turno)

        # Redibujar piezas
        self.tablero.mostrar_piezas()

    def run(self):
            self.ventana.mainloop()

class Pestaña_Promoción:
    def __init__(self, interfaz, color_peon, fila, col):
        self.interfaz = interfaz
        self.color = color_peon
        self.fila = fila
        self.col = col
        self.pieza_seleccionada = None


        #Con esto obtenemos el mini tablero lógico
        self.opciones = Posiciones.obtener_opciones_promocion(self.color)

        self.imagenes = cargar_imagenes()
        self.ids = {}
        self.ids_color = {}

        self.ventana = tk.Toplevel()
        self.ventana.resizable(0,0)
        self.ventana.title("Promoción de Peón")


        # Frame principal que contiene todo
        self.Frame_principal = tk.Frame(self.ventana, bg= "#ffe6de" )
        self.Frame_principal.pack()

        # Franja superior con label
        self.Frame_label = tk.Frame(self.Frame_principal, bg="#347F9C", height=50)
        self.Frame_label.pack(side="top", fill="x")
        self.Label_mensaje = tk.Label(
            self.Frame_label,
            text="Selecciona la pieza que quieras invocar",
            font=("Arial", 12, "bold"),
            bg="#347F9C",
            fg="white"
        )
        self.Label_mensaje.pack()

        # Frame del mini tablero
        self.Frame_tablero = tk.Frame(self.Frame_principal, bg="#ffe6de")
        self.Frame_tablero.pack(side="left")

        self.canvas = tk.Canvas(self.Frame_tablero, width=64*3, height=64*3, bg="#ffe6de", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clic)

        #Guardar referencia de imagenes
        self.canvas.imagenes = self.imagenes


        # Botón de confirmar (derecha)
        self.boton_confirmar = tk.Button(
            self.Frame_principal,
            text="Confirmar",
            font=("Arial", 12, "bold"),
            bg="#6FC272",
            fg="white",
            width=11,
            height=9,  # altura en líneas de texto para que sea más largo
            command=None # tu función
        )
        self.boton_confirmar.pack(side="right")

        # Dibujar mini tablero
        self.mini_tablero()
        self.mini_piezas()


    def mini_tablero(self):
        for fila in range(3):
            for col in range (3):
                color = "#ffe6de" if (fila + col)%2==0 else "#87bac7"
                self.canvas.create_rectangle(
                    col*64, fila*64,
                    (col+1)*64, (fila+1)*64,
                    fill=color,outline=""
                )

    def mini_piezas(self):
        for row, fila in enumerate(self.opciones):
            for col, pieza in enumerate(fila):
                if pieza != "--":
                    x = col*64 + 32
                    y = row*64 + 32
                    self.ids[row,col]= self.canvas.create_image(x, y, image=self.imagenes[pieza], anchor="center")

    def clic(self,evento):
        fila, col = obtener_fila_columna(evento, 64)
        self.seleccionar(fila,col)
        print(f"Clic en {fila, col}")

    def seleccionar(self, fila, col):
        pieza = self.opciones[fila][col]
        if pieza != "--":
            self.pieza_seleccionada = (fila, col)
            print(f"Pieza seleccionada: {pieza}")
            self.colorear_opcion(fila, col)
            return fila, col
        else:
            print("Casilla vacía")

    def colorear_opcion(self,fila,col):
        for id in self.ids_color.values():
            self.canvas.delete(id)
        self.ids_color.clear()

        self.ids_color[fila,col] = self.canvas.create_rectangle(
            col*64, fila*64,
            (col+1)*64, (fila+1)*64,
            fill="",
            outline="yellow",
            width=3
        )
        


# --------------------------------------------------------------------
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
    def __init__(self, tablero_visual, interfaz):
        self.tablero = tablero_visual
        self.interfaz = interfaz
        self.estructura = Posiciones()
        self.turno = "B"
        self.pieza_seleccionada = None
        self.piezas_eliminadas = []
        self.tablero.canvas.bind("<Button-1>", self.clic)

    def clic(self, evento):

        fila, col = obtener_fila_columna(evento, self.tablero.cuadrado)
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
            
            #Abrimos pestaña emergente
            if pieza[0] == "P" and (fila_d == 0 or fila_d == 7):
                Pestaña_Promoción(self.interfaz, self.turno, fila_d, col_d)

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
            self.interfaz.actualizar_turno(self.turno)


        else:
            self.tablero.colorear_opciones([])
            print("Movimiento inválido")


        self.pieza_seleccionada = None


    def capturar_pieza(self, fila, col):
        pieza_objetivo = self.estructura.piezas[fila][col]
        if pieza_objetivo != "--" and not pieza_objetivo.endswith(self.turno):
            print (f"Pieza eliminada = {pieza_objetivo}")
            self.piezas_eliminadas.append(pieza_objetivo)
            print(f"Piezas eliminadas: {self.piezas_eliminadas}")
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





# --------------------------------------------------------------------
# EJECUCIÓN
# --------------------------------------------------------------------
if __name__ == "__main__":
    juego = Interfaz()
    juego.run()
