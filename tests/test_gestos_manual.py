"""
Pruebas auxiliares para src/processing/gestos.py

Objetivo
--------
Mientras src/vision/script.py todavia no genera instancias reales de
Landmark (la integracion con MediaPipe + landmark.py esta pendiente),
este script construye landmarks de mano sinteticos (coordenadas
inventadas a mano) para poder probar la logica de gestos.py de forma
aislada, sin necesidad de camara ni del resto del pipeline.

No reemplaza las pruebas reales con camara, sirve para detectar errores 
de logica/sintaxis temprano, y para calibrar FACTOR_EXTENSION mas adelante 
comparando contra casos reales.

Como correrlo
--------------
Ejecuta:
    python3 test_gestos_manual.py
"""

import math
import os
import sys


sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from src.processing.landmark import Landmark
from src.processing import gestos


# --- Geometria sintetica de una mano -----------------------------------
#
# Se modela la muñeca en un punto fijo y cada dedo como una linea recta
# que sale de la muñeca en un angulo propio. No es anatomicamente
# perfecto, pero es suficiente para ejercitar la logica de distancias
# y direccion que usa gestos.py.

DEDOS_ANGULOS = {
    "pulgar": 100,
    "indice": 80,
    "medio": 90,
    "anular": 100,
    "menique": 110,
}

MUNECA_XY = (0.5, 0.9)
DISTANCIA_MCP = 0.15
DISTANCIA_PUNTA_EXTENDIDA = 0.38
DISTANCIA_PUNTA_FLEXIONADA = 0.08
DESPLAZAMIENTO_PULGAR = 0.25


def _punto_desde_muneca(angulo_grados, distancia):
    angulo = math.radians(angulo_grados)
    x = MUNECA_XY[0] + distancia * math.cos(angulo)
    y = MUNECA_XY[1] - distancia * math.sin(angulo)
    return x, y


def construir_mano(dedos_extendidos=None, direccion_pulgar=None, incluir_muneca=True):
    """
    Construye una lista de Landmark simulando una mano.

    dedos_extendidos: lista de nombres de dedos (sin incluir "pulgar",
        que se controla aparte) que deben quedar EXTENDIDOS. El resto
        queda flexionado (puño).

    direccion_pulgar: "arriba", "lado", "abajo" o None (flexionado,
        pegado a la palma, como en un puño normal).

    incluir_muneca: si es False, no se agrega el landmark de la
        muñeca -- util para probar el caso de landmarks incompletos.
    """
    if dedos_extendidos is None:
        dedos_extendidos = []

    landmarks = []
    if incluir_muneca:
        landmarks.append(
            Landmark("mano_muñeca", 0, MUNECA_XY[0], MUNECA_XY[1], 0, "hand")
        )

    for dedo, angulo in DEDOS_ANGULOS.items():
        mcp_x, mcp_y = _punto_desde_muneca(angulo, DISTANCIA_MCP)
        landmarks.append(Landmark(f"{dedo}_mcp", 1, mcp_x, mcp_y, 0, "hand"))

        if dedo == "pulgar" and direccion_pulgar is not None:
            if direccion_pulgar == "arriba":
                punta_xy = (mcp_x + 0.01, mcp_y - DESPLAZAMIENTO_PULGAR)
            elif direccion_pulgar == "lado":
                punta_xy = (mcp_x + DESPLAZAMIENTO_PULGAR, mcp_y + 0.01)
            elif direccion_pulgar == "abajo":
                punta_xy = (mcp_x + 0.01, mcp_y + DESPLAZAMIENTO_PULGAR)
            else:
                punta_xy = _punto_desde_muneca(angulo, DISTANCIA_PUNTA_FLEXIONADA)
        elif dedo in dedos_extendidos:
            punta_xy = _punto_desde_muneca(angulo, DISTANCIA_PUNTA_EXTENDIDA)
        else:
            punta_xy = _punto_desde_muneca(angulo, DISTANCIA_PUNTA_FLEXIONADA)

        landmarks.append(Landmark(f"{dedo}_punta", 4, punta_xy[0], punta_xy[1], 0, "hand"))

    return landmarks


# --- Casos de prueba -----------------------------------------------------

TODOS_LOS_DEDOS = ["pulgar", "indice", "medio", "anular", "menique"]

CASOS = [
    ("Mano abierta (todos extendidos)",
     construir_mano(dedos_extendidos=TODOS_LOS_DEDOS),
     "mano_extendida"),

    ("Puño cerrado (todo flexionado, pulgar pegado)",
     construir_mano(dedos_extendidos=[], direccion_pulgar=None),
     "puño_cerrado"),

    ("Pulgar arriba (resto flexionado)",
     construir_mano(dedos_extendidos=[], direccion_pulgar="arriba"),
     "pulgar_arriba"),

    ("Gesto mixto -- solo el indice extendido (sin definir)",
     construir_mano(dedos_extendidos=["indice"]),
     "ninguno"),

    ("Sin landmark de muñeca (dato incompleto)",
     construir_mano(dedos_extendidos=TODOS_LOS_DEDOS, incluir_muneca=False),
     "ninguno"),

    ("Lista de landmarks vacia (mano no detectada)",
     [],
     "ninguno"),
]


def correr_pruebas_seleccionar_gesto():
    print("=== Pruebas de seleccionar_gesto (sin estado) ===")
    for descripcion, landmarks, esperado in CASOS:
        resultado = gestos.seleccionar_gesto(landmarks)
        estado = "OK" if resultado == esperado else "REVISAR"
        print(f"[{estado}] {descripcion}")
        print(f"       esperado={esperado!r}  obtenido={resultado!r}")
    print()


def correr_prueba_estado():
    print("=== Prueba de detectar_gesto (con estado / cambios) ===")

    gestos.ultimo_gesto = None  # reinicia el estado global antes de la prueba

    abierta = construir_mano(dedos_extendidos=TODOS_LOS_DEDOS)
    puno = construir_mano(dedos_extendidos=[], direccion_pulgar=None)
    sin_mano = []

    secuencia = [
        ("mano abierta (1ra vez)", abierta, "mano_extendida"),
        ("mano abierta (se mantiene)", abierta, None),
        ("cambia a puño", puno, "puño_cerrado"),
        ("puño se mantiene", puno, None),
        ("se retira la mano", sin_mano, "ninguno"),
    ]

    for descripcion, landmarks, esperado in secuencia:
        resultado = gestos.detectar_gesto(landmarks)
        estado = "OK" if resultado == esperado else "REVISAR"
        print(f"[{estado}] {descripcion}: esperado={esperado!r} obtenido={resultado!r}")
    print()


if __name__ == "__main__":
    correr_pruebas_seleccionar_gesto()
    correr_prueba_estado()
