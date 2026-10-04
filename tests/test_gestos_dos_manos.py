"""
Pruebas auxiliares para el escenario de dos manos de gestos.py

Objetivo
--------
Validar, con landmarks sinteticos, que detectar_gesto(landmarks, mano)
mantiene un estado separado para "Left" y "Right", cubriendo los
puntos clave del Definition of Done:

- Ambas manos pueden mantener gestos distintos al mismo tiempo.
- Cambiar el gesto de una mano no afecta el estado de la otra.
- No se generan eventos repetidos mientras un gesto se mantiene.
- Retirar una mano no afecta el estado de la otra.
- Al reaparecer una mano, su reconocimiento se recupera correctamente
  (incluso si el gesto es el mismo que tenia antes de desaparecer).

No reemplaza la prueba real con camara y ambas manos que pide la
Issue -- es para detectar errores de logica antes de esa prueba.

Como correrlo
--------------
Ejecutar:
    python3 test_gestos_dos_manos.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.processing.landmark import Landmark
import src.processing.gestos as gestos


# --- Geometria sintetica de una mano (ver test_gestos_manual.py) --------

DEDOS_ANGULOS = {
    "pulgar": 100,
    "indice": 80,
    "medio": 90,
    "anular": 100,
    "menique": 110,
}
MUNECA_XY = (0.5, 0.9)


def _punto_desde_muneca(angulo_grados, distancia):
    angulo = math.radians(angulo_grados)
    x = MUNECA_XY[0] + distancia * math.cos(angulo)
    y = MUNECA_XY[1] - distancia * math.sin(angulo)
    return x, y


def construir_mano(dedos_extendidos=None, direccion_pulgar=None):
    if dedos_extendidos is None:
        dedos_extendidos = []

    landmarks = [Landmark("mano_muñeca", 0, MUNECA_XY[0], MUNECA_XY[1], 0, "hand")]

    for dedo, angulo in DEDOS_ANGULOS.items():
        mcp_x, mcp_y = _punto_desde_muneca(angulo, 0.15)
        landmarks.append(Landmark(f"{dedo}_mcp", 1, mcp_x, mcp_y, 0, "hand"))

        if dedo == "pulgar" and direccion_pulgar == "arriba":
            punta_xy = (mcp_x + 0.01, mcp_y - 0.25)
        elif dedo in dedos_extendidos:
            punta_xy = _punto_desde_muneca(angulo, 0.38)
        else:
            punta_xy = _punto_desde_muneca(angulo, 0.08)

        landmarks.append(Landmark(f"{dedo}_punta", 4, punta_xy[0], punta_xy[1], 0, "hand"))

    return landmarks


TODOS_LOS_DEDOS = ["pulgar", "indice", "medio", "anular", "menique"]

ABIERTA = construir_mano(dedos_extendidos=TODOS_LOS_DEDOS)
PUNO = construir_mano(dedos_extendidos=[], direccion_pulgar=None)
PULGAR_ARRIBA = construir_mano(dedos_extendidos=[], direccion_pulgar="arriba")
SIN_MANO = []


def correr_prueba():
    print("=== Prueba de estado independiente por mano (detectar_gesto) ===")

    gestos.ultimo_gesto = {}  #Reinicia el estado global antes de la prueba

    pasos = [
        ("Left=abierta, Right=puño (simultaneo)", ABIERTA, "Left", "mano_extendida"),
        ("Right=puño (mismo frame)", PUNO, "Right", "puño_cerrado"),
        ("Left se mantiene abierta (no debe repetir)", ABIERTA, "Left", None),
        ("Right se mantiene en puño (no debe repetir)", PUNO, "Right", None),
        ("Left cambia a pulgar_arriba (Right no debe verse afectada)", PULGAR_ARRIBA, "Left", "pulgar_arriba"),
        ("Left desaparece", SIN_MANO, "Left", "ninguno"),
        ("Right sigue en puño, sin verse afectada por la ausencia de Left", PUNO, "Right", None),
        ("Left reaparece con el MISMO gesto de antes de desaparecer", PULGAR_ARRIBA, "Left", "pulgar_arriba"),
    ]

    for descripcion, landmarks, mano, esperado in pasos:
        resultado = gestos.detectar_gesto(landmarks, mano)
        estado = "OK" if resultado == esperado else "REVISAR"
        print(f"[{estado}] {descripcion}")
        print(f"       mano={mano} esperado={esperado!r} obtenido={resultado!r}")

    print()
    print("Estado final de gestos.ultimo_gesto:", gestos.ultimo_gesto)


if __name__ == "__main__":
    correr_prueba()
