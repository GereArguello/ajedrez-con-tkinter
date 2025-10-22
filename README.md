# Proyecto Ajedrez en Python

Este proyecto es un juego de ajedrez implementado en Python utilizando **Tkinter** para la interfaz gráfica. Permite jugar partidas con todas las piezas, movimientos válidos y detección de jaque y jaque mate.

## Funcionalidades principales

- Tablero de 8x8 con casillas coloreadas.
- Movimientos válidos para todas las piezas:
  - Torre
  - Alfil
  - Caballo
  - Reina
  - Rey
  - Peón
- Detección de jaque y jaque mate.
- Captura de piezas.
- Turnos alternados entre jugadores blanco y negro.
- Interfaz visual usando imágenes `.png` para cada pieza.

## Estructura de archivos
```
Ajedrez/
├── Main/
│ ├── ajedrez.py
│ ├── Piezas/ # Carpeta con imágenes de las piezas
│ │ ├── AB.png
│ │ ├── AN.png
│ │ └── ...
│ └── README.md
```

## Requisitos

- Python 3.x
- Tkinter (generalmente incluido con Python)


## Mejoras futuras
- interfaz gráfica más dinámica

- Implementar enroque, promoción de peones y captura al paso.

- Añadir historial de movimientos.

- Implementar un sistema de guardado/carga de partidas.

- IA básica para jugar contra la computadora.

## Cómo ejecutar

1. Abrir una terminal en la carpeta `Main`.
2. Ejecutar el archivo principal:

```bash
python ajedrez.py