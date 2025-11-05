
# ESTRUCTURA INICIAL DEL TABLERO

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

# ESTRUCTURA PROMOCIONES

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
