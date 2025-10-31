# Ajedrez en Python

Este proyecto es un **juego de ajedrez completo** implementado en **Python** utilizando **Tkinter** para la interfaz gráfica. Permite jugar partidas con movimientos válidos, detección de jaque y jaque mate, captura de piezas y promoción de peones mediante una ventana emergente.

---

## Características principales

- **Tablero visual de 8x8** con casillas coloreadas alternadas.
- Movimientos válidos implementados para todas las piezas:
  - Torre
  - Alfil
  - Caballo
  - Reina
  - Rey
  - Peón
- **Detección de jaque y jaque mate**.
- **Captura de piezas** y actualización del tablero lógico y visual.
- Turnos alternados entre jugadores **blanco** y **negro**.
- **Promoción de peones** con ventana emergente que permite elegir entre Torre, Alfil, Caballo o Reina.
- Coloreado de opciones de movimiento y resaltado del rey en jaque.
- Botón de **reinicio** del tablero.
- Optimización en la carga de imágenes y manejo de ventanas emergentes.

---

## Estructura del proyecto

Ajedrez/
├── Main/
│ ├── ajedrez.py # Archivo principal
│ ├── Piezas/ # Carpeta con imágenes de las piezas (.png)
│ │ ├── AB.png
│ │ ├── AN.png
│ │ ├── CB.png
│ │ ├── CN.png
│ │ ├── KB.png
│ │ ├── KN.png
│ │ ├── PB.png
│ │ ├── PN.png
│ │ ├── QB.png
│ │ ├── QN.png
│ │ ├── TB.png
│ │ └── TN.png
│ └── README.md

---

## Clases principales

- **Posiciones**: Define la disposición inicial de las piezas y opciones de promoción.
- **Pieza** y sus subclases (`Torre`, `Alfil`, `Caballo`, `Reina`, `Rey`, `Peon`): Definen movimiento válido y lógica de captura.
- **Tablero**: Representación visual y manejo de casillas y piezas.
- **Juego**: Lógica de turnos, selección de piezas, movimientos válidos, detección de jaque y jaque mate, y promoción de peones.
- **Interfaz**: Configuración de la ventana principal, botones, turnos y ejecución del juego.
- **Pestaña_Promoción**: Ventana emergente para elegir pieza al promocionar un peón.

---

## Requisitos

- **Python 3.x**
- **Tkinter** (generalmente incluido con Python)
- Imágenes de piezas en formato `.png` en la carpeta `Piezas/`.

---

## Cómo ejecutar

1. Abrir una terminal en la carpeta `Main`.
2. Ejecutar el archivo principal:

```bash
python ajedrez.py

