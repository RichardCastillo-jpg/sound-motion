"""
Pruebas del control de acordes y del sintetizador.

Como correrlas (desde la raíz del proyecto):
    python -m pytest tests/test_control_acordes.py -v
"""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

import src.processing.gestos as gestos
from src.audio.control_acordes import ControlAcordes, midi_a_frecuencia
from src.audio.sintetizador import FRECUENCIA_MUESTREO, generar_onda
from src.processing.landmark import Landmark


# --- Manos sintéticas (misma geometría que test_gestos_dos_manos.py) ------

DEDOS_ANGULOS = {"pulgar": 100, "indice": 80, "medio": 90, "anular": 100, "menique": 110}
MUNECA_XY = (0.5, 0.9)


def _punto_desde_muneca(angulo_grados, distancia):
    angulo = math.radians(angulo_grados)
    return (MUNECA_XY[0] + distancia * math.cos(angulo),
            MUNECA_XY[1] - distancia * math.sin(angulo))


def construir_mano(dedos_extendidos):
    landmarks = [Landmark("mano_muñeca", 0, MUNECA_XY[0], MUNECA_XY[1], 0, "hand")]
    for dedo, angulo in DEDOS_ANGULOS.items():
        mcp_x, mcp_y = _punto_desde_muneca(angulo, 0.15)
        landmarks.append(Landmark(f"{dedo}_mcp", 1, mcp_x, mcp_y, 0, "hand"))
        distancia = 0.38 if dedo in dedos_extendidos else 0.08
        punta_x, punta_y = _punto_desde_muneca(angulo, distancia)
        landmarks.append(Landmark(f"{dedo}_punta", 4, punta_x, punta_y, 0, "hand"))
    return landmarks


TODOS = ["pulgar", "indice", "medio", "anular", "menique"]
MANO_ABIERTA = construir_mano(TODOS)
MANO_PUNO = construir_mano([])
SIN_MANO = []


@pytest.fixture
def control():
    # frames_estables=1: cada llamada a actualizar() cuenta como un
    # fotograma ya estable, para probar la lógica sin repetir llamadas.
    return ControlAcordes(frames_estables=1)


# --- Estado inicial ---------------------------------------------------

def test_estado_inicial(control):
    assert control.nota_actual is None
    assert control.tipo_acorde == "normal"
    assert control.obtener_acorde() is None
    assert control.obtener_frecuencias() == []


# --- Mano de notas: gesto -> nota -------------------------------------

@pytest.mark.parametrize("gesto, nota", [
    ("indice", "C"),
    ("indice_medio", "D"),
    ("indice_medio_anular", "E"),
    ("indice_medio_anular_menique", "F"),
    ("mano_extendida", "G"),
    ("indice_menique", "A"),
    ("puño_cerrado", "B"),
])
def test_gesto_selecciona_nota(control, gesto, nota):
    control.actualizar(gesto, "ninguno", False)
    assert control.nota_actual == nota


# --- Mano de tipo: mayor / menor / nada -------------------------------

def test_mano_extendida_es_mayor(control):
    control.actualizar("indice", "mano_extendida", True)
    assert control.obtener_acorde() == "C mayor"


def test_puno_cerrado_es_menor(control):
    control.actualizar("indice", "puño_cerrado", True)
    assert control.obtener_acorde() == "C menor"


def test_mano_de_tipo_no_visible_es_nada(control):
    control.actualizar("indice", "mano_extendida", True)   # C mayor
    control.actualizar("indice", "mano_extendida", False)  # la mano desaparece
    assert control.tipo_acorde == "normal"
    assert control.obtener_acorde() == "C"


def test_mano_de_tipo_visible_con_gesto_no_reconocido_conserva_el_tipo(control):
    control.actualizar("indice", "puño_cerrado", True)     # C menor
    control.actualizar("indice", "ninguno", True)          # pose intermedia
    assert control.obtener_acorde() == "C menor"


# --- Independencia de nota y tipo -------------------------------------

def test_cambiar_nota_conserva_tipo(control):
    control.actualizar("indice", "puño_cerrado", True)         # C menor
    control.actualizar("indice_medio", "puño_cerrado", True)   # D
    assert control.obtener_acorde() == "D menor"


def test_cambiar_tipo_conserva_nota(control):
    control.actualizar("indice_medio_anular", "puño_cerrado", True)    # E menor
    control.actualizar("indice_medio_anular", "mano_extendida", True)  # mayor
    assert control.obtener_acorde() == "E mayor"


def test_mano_de_notas_no_visible_conserva_la_nota(control):
    control.actualizar("indice_menique", "mano_extendida", True)   # A mayor
    control.actualizar("ninguno", "mano_extendida", True)          # sin gesto
    assert control.obtener_acorde() == "A mayor"


# --- Pérdida y recuperación de la mano de tipo ------------------------

def test_recuperacion_de_la_mano_de_tipo(control):
    control.actualizar("indice", "puño_cerrado", True)   # C menor
    control.actualizar("indice", "puño_cerrado", False)  # desaparece -> C
    assert control.obtener_acorde() == "C"
    control.actualizar("indice", "puño_cerrado", True)   # reaparece
    assert control.obtener_acorde() == "C menor"


# --- Valor de retorno (¿cambió el acorde?) ----------------------------

def test_retorna_true_solo_si_el_acorde_cambia(control):
    assert control.actualizar("indice", "ninguno", False) is True    # aparece C
    assert control.actualizar("indice", "ninguno", False) is False   # igual
    assert control.actualizar("indice", "puño_cerrado", True) is True  # C menor


# --- Estabilidad (evita errores de un solo fotograma) -----------------

def test_un_fotograma_aislado_no_cambia_el_acorde():
    control = ControlAcordes()  # frames_estables por defecto
    for _ in range(10):
        control.actualizar("indice", "mano_extendida", True)
    assert control.obtener_acorde() == "C mayor"

    # La cámara pierde la mano de tipo durante un solo fotograma.
    assert control.actualizar("indice", "mano_extendida", False) is False
    assert control.obtener_acorde() == "C mayor"

    # Y la mano vuelve: el acorde nunca cambió.
    control.actualizar("indice", "mano_extendida", True)
    assert control.obtener_acorde() == "C mayor"


def test_ausencia_sostenida_si_cambia_el_acorde():
    control = ControlAcordes()
    for _ in range(10):
        control.actualizar("indice", "mano_extendida", True)
    for _ in range(10):
        control.actualizar("indice", "mano_extendida", False)
    assert control.obtener_acorde() == "C"
# --- Frecuencias ------------------------------------------------------

def test_frecuencia_de_referencia_la4():
    assert midi_a_frecuencia(69) == pytest.approx(440.0)


def test_frecuencias_c_mayor(control):
    control.actualizar("indice", "mano_extendida", True)
    c, e, g = control.obtener_frecuencias()
    assert c == pytest.approx(261.63, abs=0.01)
    assert e == pytest.approx(329.63, abs=0.01)
    assert g == pytest.approx(392.00, abs=0.01)


def test_c_menor_tiene_tercera_menor(control):
    control.actualizar("indice", "puño_cerrado", True)
    c, mi_bemol, g = control.obtener_frecuencias()
    assert mi_bemol == pytest.approx(311.13, abs=0.01)


def test_nada_es_una_sola_nota(control):
    control.actualizar("indice", "mano_extendida", False)
    frecuencias = control.obtener_frecuencias()
    assert len(frecuencias) == 1
    assert frecuencias[0] == pytest.approx(261.63, abs=0.01)


# --- Sintetizador (solo generación de onda, sin reproducir) -----------

def test_onda_no_satura_y_tiene_senal(control):
    control.actualizar("indice", "mano_extendida", True)
    onda = generar_onda(control.obtener_frecuencias())
    assert 0.05 < abs(onda).max() <= 1.0


def test_onda_contiene_las_notas_del_acorde(control):
    control.actualizar("indice", "puño_cerrado", True)  # C menor
    esperadas = control.obtener_frecuencias()
    onda = generar_onda(esperadas)

    espectro = np.abs(np.fft.rfft(onda))
    frecuencias = np.fft.rfftfreq(len(onda), 1 / FRECUENCIA_MUESTREO)
    picos = sorted(frecuencias[np.argsort(espectro)[-3:]])

    for pico, esperada in zip(picos, esperadas):
        assert pico == pytest.approx(esperada, abs=1.0)


def test_onda_sin_frecuencias_es_silencio():
    assert abs(generar_onda([])).max() == 0


# --- Flujo completo con gestos.py real --------------------------------
# Repite lo que hace script.py en cada fotograma: detectar_gesto() para
# cada mano, conservar el gesto actual y actualizar el control.
# MediaPipe etiqueta la mano DERECHA real como "Left" (imagen sin espejo),
# por eso la mano de notas es "Left" y la de tipo es "Right".

ETIQUETA_MANO_NOTAS = "Left"
ETIQUETA_MANO_TIPO = "Right"


class Simulador:
    def __init__(self):
        gestos.ultimo_gesto = {}
        self.control = ControlAcordes()
        self.actual = {"Left": "ninguno", "Right": "ninguno"}

    def fotogramas(self, cantidad, landmarks_left, landmarks_right):
        cambios = []
        for _ in range(cantidad):
            for mano, landmarks in (("Left", landmarks_left), ("Right", landmarks_right)):
                gesto = gestos.detectar_gesto(landmarks, mano)
                if gesto is not None:
                    self.actual[mano] = gesto
            cambio = self.control.actualizar(
                self.actual[ETIQUETA_MANO_NOTAS],
                self.actual[ETIQUETA_MANO_TIPO],
                bool(landmarks_right),
            )
            if cambio:
                cambios.append(self.control.obtener_acorde())
        return cambios


def test_flujo_completo_con_gestos_reales():
    sim = Simulador()
    indice = construir_mano(["indice"])
    indice_medio = construir_mano(["indice", "medio"])

    # Solo la mano de notas: nota sola.
    assert sim.fotogramas(8, indice, SIN_MANO) == ["C"]
    # Aparece la mano de tipo abierta: mayor.
    assert sim.fotogramas(8, indice, MANO_ABIERTA) == ["C mayor"]
    # La mano de tipo se cierra: menor.
    assert sim.fotogramas(8, indice, MANO_PUNO) == ["C menor"]
    # Cambia la nota: el tipo se conserva.
    assert sim.fotogramas(8, indice_medio, MANO_PUNO) == ["D menor"]
    # La mano de tipo desaparece: nada.
    assert sim.fotogramas(8, indice_medio, SIN_MANO) == ["D"]
    # Reaparece abierta: mayor, con la misma nota.
    assert sim.fotogramas(8, indice_medio, MANO_ABIERTA) == ["D mayor"]


def test_flujo_completo_la_mano_de_notas_desaparece():
    sim = Simulador()
    indice = construir_mano(["indice"])

    sim.fotogramas(8, indice, MANO_PUNO)  # C menor
    # La mano de notas se va: no cambia nada y el sistema no se bloquea.
    assert sim.fotogramas(8, SIN_MANO, MANO_PUNO) == []
    assert sim.control.obtener_acorde() == "C menor"
    # Vuelve con otro gesto y el sistema responde.
    assert sim.fotogramas(8, construir_mano(["indice", "menique"]), MANO_PUNO) == ["A menor"]