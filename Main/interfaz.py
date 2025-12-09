import tkinter as tk
from utils import cargar_imagenes, obtener_fila_columna
from tablero import Tablero
from posiciones import Posiciones
from juego import Juego
import copy


# -- INTERFAZ COMPLETA -- 

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ajedrez")
        self.ventana.geometry("772x921+100+50")
        self.ventana.resizable(0,0)

        self.tiempo_blancas = 600
        self.tiempo_negras = 600
        self.reloj_activo = "B"
        self.reloj_id = None
        self.juego_iniciado = False

        self.after_id = None  # ← ID del after activo (para cancelar notificaciones previas
        # -- Imagenes --

        self.imagenes = cargar_imagenes()
        self.imagenes_mini = cargar_imagenes(tamanio_base=18)
        self.img_blancas = self.imagenes["PB"]
        self.img_negras = self.imagenes["PN"]

        # -- contenedores de piezas eliminadas --
        self.celdas_blancas = []
        self.celdas_negras = []


        # -- Frames main --
        self.main_frame = tk.Frame(self.ventana, bg="#347F9C")
        self.main_frame.pack()


        # -- Contenedor central que agrupa las franjas y el tablero --
        self.centro_frame = tk.Frame(self.main_frame, bg="#347F9C")
        self.centro_frame.pack(expand=True, fill="both")

        # -- Franja superior --
        self.top_frame = tk.Frame(self.centro_frame, bg="#347F9C", height=80, bd=2, relief="solid")
        self.top_frame.pack(side="top", fill="x")
        self.top_frame.pack_propagate(False)


        # Configurar columnas para centrar el label
        self.top_frame.columnconfigure(0, weight=0)  # botón
        self.top_frame.columnconfigure(1, weight=0)  # turno
        self.top_frame.columnconfigure(2, weight=1)  # cartel (se expande)
        self.top_frame.columnconfigure(3, weight=0)  # cronómetro

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
            compound="right", font=("Arial", 22), bg="#347F9C"
        )
        self.label_turno.grid(row=0, column=1, sticky="w", padx=20)



        #Label notificatorio
        self.label_cartel = tk.Label(self.top_frame, text="", bg="#00BAC7", font=("Arial", 14), height=2)
        self.label_cartel.grid(row=0, column=2, sticky="ew", padx=5)  # se expande horizontalmente
        self.label_cartel.config(highlightbackground="black", highlightthickness=2)
        self.label_cartel.grid_remove()

        # Cronómetro a la derecha
        self.label_cronómetro = tk.Label(self.top_frame, text="10:00",font=("Arial", 14), bg="#C0C0C0", width=8, height=3, bd=2, relief="solid")
        self.label_cronómetro.grid(row=0, column=3, sticky="e")

        # -- Contenedor del tablero (centrado) --
        self.frame_tablero = tk.Frame(self.centro_frame, bg="#bebebe",bd=1,relief="solid",highlightbackground="black",highlightthickness=1)
        self.frame_tablero.pack(side="top")

        # -- Franja inferior simétrica --
        self.bottom_frame = tk.Frame(self.centro_frame, bg="#347F9C", height=80)
        self.bottom_frame.pack(side="bottom", fill="x")
        self.bottom_frame.pack_propagate(False)

        self.bottom_frame.columnconfigure(0, weight=1)  # Izquierda
        self.bottom_frame.columnconfigure(1, weight=1)  # Centro expansible
        self.bottom_frame.columnconfigure(2, weight=0)  # Derecha (cronómetro)

        # -- ELIMINADOS BLANCOS -- #

        self.frame_blanco = tk.Frame(self.bottom_frame, height=3, bg="#347F9C", bd=2, relief="solid")
        self.frame_blanco.grid(row=0, column=0, sticky="nsew")


        self.label1 = tk.Label(self.frame_blanco, text= "Piezas eliminadas:", font=("Arial", 12),fg= "white", bg="#347F9C")
        self.label1.pack(side="left",padx=5, pady=(0,20))

        self.blancos_eliminados = tk.Frame(self.frame_blanco, height=1, bg="#347F9C")
        self.blancos_eliminados.pack(side="left", padx=5, expand=False)


        for fila in range(2):
            for columna in range(8):
                celda = tk.Frame(self.blancos_eliminados, width=20, height=20, bg="#347F9C", bd=0, highlightthickness=0)
                if fila == 0:
                    celda.grid(row=fila, column=columna,pady=(0,5))
                elif fila == 1:
                    celda.grid(row=fila, column=columna,pady=(5,0))
                self.celdas_blancas.append(celda)


                
        # -- ELIMINADOS NEGROS -- #

        self.frame_negro = tk.Frame(self.bottom_frame, height=3, bg="#347F9C", bd=2, relief="solid")
        self.frame_negro.grid(row=0, column=1, sticky="nsew")

        self.label2 = tk.Label(self.frame_negro, text= "Piezas eliminadas:", font=("Arial", 12), fg= "white", bg="#347F9C")
        self.label2.pack(side="left",padx=5, pady=(0,20))

        self.negros_eliminados = tk.Frame(self.frame_negro, height=1, bg="#347F9C")
        self.negros_eliminados.pack(side="left", padx=5, expand=False)


        for fila in range(2):
            for columna in range(8):
                celda = tk.Frame(self.negros_eliminados, width=20, height=20, bg="#347F9C", bd=0, highlightthickness=0)
                if fila == 0:
                    celda.grid(row=fila, column=columna,pady=(0,5))
                elif fila == 1:
                    celda.grid(row=fila, column=columna,pady=(5,0))
                self.celdas_negras.append(celda)

        # Cronómetro a la derecha
        self.label_cronómetro_2 = tk.Label(self.bottom_frame, text="10:00",font=("Arial", 14), bg="#C0C0C0", width=8, height=3, bd=2, relief="solid")
        self.label_cronómetro_2.grid(row=0, column=2, sticky="e", padx=(0,1),pady=(0,5))



        # -- Tablero Visual y Lógico --
        self.tablero = Tablero(self.frame_tablero, 96, piezas=Posiciones().piezas)
        self.juego = (Juego(self.tablero, self))







    def mostrar_notificacion(self, mensaje):
        """Muestra una notificación persistente hasta que se oculte manualmente."""
        # Cancelar notificación pendiente si la hay
        if self.after_id:
            self.ventana.after_cancel(self.after_id)
            self.after_id = None

        self.label_cartel.config(text=mensaje)
        self.label_cartel.grid()

    def ocultar_mensaje(self):
        """Oculta la notificación actual."""
        if self.after_id:
            self.ventana.after_cancel(self.after_id)
            self.after_id = None

        self.label_cartel.grid_remove()

    def mostrar_temporal(self, mensaje, duracion=2000, siguiente=None):
        """Muestra una notificación temporal y opcionalmente encadena otra."""
        # Cancelar cualquier mensaje pendiente
        if self.after_id:
            self.ventana.after_cancel(self.after_id)
            self.after_id = None

        self.label_cartel.config(text=mensaje)
        self.label_cartel.grid()

        def finalizar():
            self.after_id = None
            if siguiente:
                self.mostrar_notificacion(siguiente)
            else:
                self.ocultar_mensaje()

        # Guardamos el ID del after para poder cancelarlo después
        self.after_id = self.ventana.after(duracion, finalizar)

 
    def actualizar_turno(self, color):

        if hasattr(self, "reloj_id") and self.reloj_id:
            self.ventana.after_cancel(self.reloj_id)
            self.reloj_id = None

        self.reloj_activo = color

        
        if self.reloj_activo == "B":
            self.label_cronómetro.config(bg="#C0C0C0")
            self.label_turno.config(text="Turno de:", image=self.img_blancas)
            minutos, segundos = divmod(self.tiempo_blancas, 60)
            texto = f"{minutos:02}:{segundos:02}"
            self.label_cronómetro_2.config(text=texto, bg="#12AA1F")
        else:
            self.label_cronómetro_2.config(bg="#C0C0C0")
            self.label_turno.config(text="Turno de:", image=self.img_negras)
            minutos, segundos = divmod(self.tiempo_negras, 60)
            texto = f"{minutos:02}:{segundos:02}"
            self.label_cronómetro.config(text=texto, bg="#12AA1F")
        
        if self.juego_iniciado:
            self.reloj_id = self.ventana.after(1000,self.actualizar_reloj)
        



    def actualizar_reloj(self):
        if self.reloj_activo is None:
            return

        if self.reloj_activo == "B":
            self.tiempo_blancas -= 1

            if self.tiempo_blancas <= 0:
                self.label_cronómetro_2.config(text="00:00")
                self.mostrar_notificacion("Ganador: NEGRAS")
                self.tablero.canvas.unbind("<Button-1>")
                self.reloj_activo = None
                return  # ⛔ Detiene completamente el cronómetro

            minutos, segundos = divmod(self.tiempo_blancas, 60)
            self.label_cronómetro_2.config(text=f"{minutos:02}:{segundos:02}")

        else:
            self.tiempo_negras -= 1

            if self.tiempo_negras <= 0:
                self.label_cronómetro.config(text="00:00")
                self.mostrar_notificacion("Ganador: BLANCAS")
                self.tablero.canvas.unbind("<Button-1>")
                self.reloj_activo = None
                return  #  Detiene completamente el cronómetro

            minutos, segundos = divmod(self.tiempo_negras, 60)
            self.label_cronómetro.config(text=f"{minutos:02}:{segundos:02}")


        self.reloj_id = self.ventana.after(1000, self.actualizar_reloj)

    def reiniciar_cronómetros(self):
        if hasattr(self, "reloj_id") and self.reloj_id:
            self.ventana.after_cancel(self.reloj_id)
            self.reloj_id = None
            self.tiempo_blancas = 600
            self.tiempo_negras = 600
            self.label_cronómetro.config(text="10:00", bg="#C0C0C0")
            self.label_cronómetro_2.config(text="10:00", bg="#C0C0C0")

            self.juego_iniciado = False

    def actualizar_eliminadas(self):

        # Limpiar celdas
        for celda in self.celdas_blancas + self.celdas_negras:
            celda.grid_propagate(False)
            for widget in celda.winfo_children():
                widget.destroy()

        # Mostrar piezas eliminadas
        blancas = [p for p in self.juego.piezas_eliminadas if p.endswith("B")]
        negras = [p for p in self.juego.piezas_eliminadas if p.endswith("N")]

        self.imagenes_eliminadas = []

        for i, pieza in enumerate(blancas[:16]):  # hasta 16 eliminadas máx.
            img = self.imagenes_mini[pieza]
            label = tk.Label(self.celdas_blancas[i], image=img, bg="#347F9C")
            label.image = img
            label.pack(expand=True)
            self.imagenes_eliminadas.append(img)

        for i, pieza in enumerate(negras[:16]):
            img = self.imagenes_mini[pieza]
            label = tk.Label(self.celdas_negras[i], image=img, bg="#347F9C")
            label.image = img
            label.pack(expand=True)
            self.imagenes_eliminadas.append(img)

    

            

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
        self.tablero.canvas.bind("<Button-1>", self.juego.clic)
        self.juego.estructura = Posiciones()
        self.juego.turno = "B"
        self.juego.pieza_seleccionada = None
        self.juego.piezas_eliminadas.clear()
        self.juego.movimientos_validos = []
        # Actualizar indicador de turno
        self.reiniciar_cronómetros()
        self.actualizar_eliminadas()
        self.actualizar_turno(self.juego.turno)
        self.ocultar_mensaje()


        # Redibujar piezas
        self.tablero.mostrar_piezas()

    def fin_de_partida(self, mensaje):
        self.mostrar_notificacion(mensaje)

        # Deshabilitar tablero
        self.tablero.canvas.unbind("<Button-1>")

        # Detener reloj
        if hasattr(self, "reloj_id") and self.reloj_id:
            self.ventana.after_cancel(self.reloj_id)
            self.reloj_id = None

        self.reloj_activo = None

    def run(self):
        self.ventana.mainloop()

class Pestaña_Promoción:
    def __init__(self, interfaz, color_peon, fila, col, imagenes):
        self.interfaz = interfaz
        self.color = color_peon
        self.fila = fila
        self.col = col
        self.pieza_seleccionada = None


        #Con esto obtenemos el mini tablero lógico
        self.opciones = Posiciones.obtener_opciones_promocion(self.color)

        self.imagenes = imagenes
        self.ids = {}
        self.ids_color = {}

        self.ventana = tk.Toplevel()
        self.ventana.resizable(0,0)
        self.ventana.title("Promoción")


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
            command=self.invocar_pieza # tu función
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
    
    def invocar_pieza(self):
        if self.pieza_seleccionada is not None:
            fila, col = self.pieza_seleccionada
            self.pieza_elegida = self.opciones[fila][col]
            print(f"Pieza: {self.pieza_elegida}")
            self.ventana.destroy()
