from posiciones import Posiciones
from utils import obtener_fila_columna, definir_clase
import copy


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
            
            clase = definir_clase(pieza)


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

        clase = definir_clase(pieza)


        pieza_destino = self.estructura.piezas[fila_d][col_d]

        if pieza_destino != "--" and pieza_destino.endswith(self.turno):
            self.tablero.colorear_opciones([])
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
                self.interfaz.mostrar_temporal("Movimiento ilegal", 2000, "Rey en jaque!")
                return

            self.capturar_pieza(fila_d, col_d)  #Captura antes de mover
            self.aplicar_movimiento(f_o, c_o, fila_d, col_d, pieza)
            self.interfaz.ocultar_mensaje()
            self.tablero.colorear_opciones([])
            
            #Abrimos pestaña emergente
            if pieza[0] == "P" and (fila_d == 0 or fila_d == 7):
                from interfaz import Pestaña_Promoción
                ventana = Pestaña_Promoción(self.interfaz, self.turno, fila_d, col_d, imagenes= self.interfaz.imagenes)
                ventana.ventana.grab_set()
                ventana.ventana.wait_window()
                pieza = ventana.pieza_elegida
                print (f"Ahora la pieza es {pieza}")
                self.estructura.piezas[fila_d][col_d] = pieza #Actualiza lógica
                self.tablero.mover_pieza(fila_d,col_d, fila_d, col_d, pieza) #Actualiza la imagen


            # Verifica si el movimiento actual pone en jaque al rival
            color_rival = "N" if self.turno == "B" else "B"


            if self.es_jaque(tablero=self.estructura.piezas, turno=color_rival):
                if not self.puede_escapar(color_rival, self.estructura.piezas):
                    self.pieza_seleccionada = None
                    self.interfaz.mostrar_notificacion("Jaque Mate!")
                    self.tablero.canvas.unbind("<Button-1>")
                    print("Jaque Mate!")
                else:
                    self.interfaz.mostrar_notificacion("Rey en jaque!")
            else:
                if not self.puede_escapar(color_rival, self.estructura.piezas):
                    self.interfaz.mostrar_notificacion("Rey ahogado!")
                    self.tablero.canvas.unbind("<Button-1>")
            self.tablero.actualizar_jaque(self.estructura.piezas, color_rival)

            #Cambiar el turno
            self.turno = "N" if self.turno == "B" else "B"
            self.interfaz.actualizar_turno(self.turno)


        else:
            self.tablero.colorear_opciones([])

            if self.es_jaque(tablero=self.estructura.piezas, turno=self.turno):
                # Secuencia de notificaciones: primero movimiento inválido, luego jaque
                self.interfaz.mostrar_temporal("Movimiento inválido", 2000, "Rey en jaque!")
            else:
                # Solo mostrar movimiento inválido
                self.interfaz.mostrar_temporal("Movimiento inválido", 2000)


        if not self.interfaz.juego_iniciado:
            self.interfaz.reloj_id = self.interfaz.ventana.after(1000, self.interfaz.actualizar_reloj)
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
            self.interfaz.actualizar_eliminadas()

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
                    clase = definir_clase(pieza)

                    if clase.movimiento_valido(fila_o, col_o, fila_rey, col_rey, tablero):
                        print(f"{pieza} {fila_o} {col_o} está amenazando al rey")
                        return True
        return False
    

    def puede_escapar(self, color_rival, tablero):
        for fila, fila_piezas in enumerate(tablero):
            for col, pieza in enumerate(fila_piezas):
                if pieza.endswith(color_rival):
                    clase = definir_clase(pieza)

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