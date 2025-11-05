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