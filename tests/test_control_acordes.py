import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import pytest

import src.processing.gestos as gestos
from src.audio.control_acordes import ControlAcordes, midi_a_frecuencia
from src.audio.sintetizador import FRECUENCIA_MUESTREO, VOLUMEN, generar_onda
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
    ("medio_anular_menique", "G"),
    ("indice_menique", "A"),
    ("menique", "B"),
])
def test_gesto_selecciona_nota(control, gesto, nota):
    assert control.actualizar(gesto, "ninguno", False) is True
    assert control.nota_actual == nota


@pytest.mark.parametrize("gesto", ["mano_extendida", "puño_cerrado"])
def test_gestos_de_tipo_no_seleccionan_nota(control, gesto):
    control.actualizar("indice", "ninguno", False)  # C
    assert control.actualizar(gesto, "ninguno", False) is False
    assert control.nota_actual == "C"


def test_gesto_none_conserva_la_nota(control):
    control.actualizar("indice", "ninguno", False)
    assert control.actualizar(None, "ninguno", False) is False
    assert control.nota_actual == "C"


# --- Silencio: la mano de notas no hace gesto -------------------------

def test_sin_gesto_de_nota_pasa_a_silencio(control):
    control.actualizar("indice", "mano_extendida", True)   # C mayor
    assert control.actualizar("ninguno", "mano_extendida", True) is True
    assert control.obtener_acorde() == "silencio"
    assert control.obtener_frecuencias() == []


@pytest.mark.parametrize("gesto_tipo, visible", [
    ("mano_extendida", True),   # mayor
    ("puño_cerrado", True),     # menor
    (None, False),              # normal
])
def test_silencio_no_genera_tonos_en_ningun_tipo(control, gesto_tipo, visible):
    # Antes, el silencio con tipo mayor o menor generaba tonos de ~10 Hz.
    control.actualizar("indice", gesto_tipo, visible)
    control.actualizar("ninguno", gesto_tipo, visible)
    assert control.obtener_frecuencias() == []


# --- Mano de tipo: mayor / menor / normal -----------------------------

def test_mano_extendida_es_mayor(control):
    control.actualizar("indice", "mano_extendida", True)
    assert control.obtener_acorde() == "C mayor"


def test_puno_cerrado_es_menor(control):
    control.actualizar("indice", "puño_cerrado", True)
    assert control.obtener_acorde() == "C menor"


def test_mano_de_tipo_no_visible_es_normal(control):
    control.actualizar("indice", "mano_extendida", True)   # C mayor
    control.actualizar("indice", "mano_extendida", False)  # la mano desaparece
    assert control.tipo_acorde == "normal"
    assert control.obtener_acorde() == "C"


def test_mano_de_tipo_visible_con_gesto_no_reconocido_conserva_el_tipo(control):
    control.actualizar("indice", "puño_cerrado", True)     # C menor
    control.actualizar("indice", "ninguno", True)          # pose intermedia
    assert control.obtener_acorde() == "C menor"


def test_gesto_de_nota_en_la_mano_de_tipo_no_hace_nada(control):
    control.actualizar("indice", "mano_extendida", True)           # C mayor
    control.actualizar("indice", "indice_medio", True)             # D en la mano de tipo
    assert control.obtener_acorde() == "C mayor"


# --- La mano de tipo NUNCA hace sonar ---------------------------------

def test_la_mano_de_tipo_nunca_hace_sonar(control):
    control.actualizar("indice", "ninguno", False)   # suena C
    for gesto_tipo, visible in [("mano_extendida", True),
                                ("puño_cerrado", True),
                                ("puño_cerrado", False),
                                ("mano_extendida", True)]:
        # El acorde cambia (C, C mayor, C menor...) pero nunca retorna True.
        assert control.actualizar("indice", gesto_tipo, visible) is False
    assert control.obtener_acorde() == "C mayor"


GESTOS_MANO_IZQUIERDA = [
    "mano_extendida", "puño_cerrado", "indice", "indice_medio",
    "indice_medio_anular", "indice_medio_anular_menique",
    "medio_anular_menique", "indice_menique", "menique", "ninguno", None,
]


@pytest.mark.parametrize("gesto_notas", ["ninguno", "indice"])  # sin gesto / sosteniendo C
@pytest.mark.parametrize("gesto_tipo", GESTOS_MANO_IZQUIERDA)
@pytest.mark.parametrize("mano_tipo_visible", [True, False])
def test_ningun_gesto_de_la_mano_de_tipo_hace_sonar(control, gesto_notas,
                                                    gesto_tipo, mano_tipo_visible):
    control.actualizar(gesto_notas, None, False)   # estado previo de la mano de notas
    assert control.actualizar(gesto_notas, gesto_tipo, mano_tipo_visible) is False


def test_el_tipo_se_aplica_en_la_siguiente_nota(control):
    control.actualizar("indice", "ninguno", False)         # C suena
    control.actualizar("indice", "puño_cerrado", True)     # tipo menor, sin sonido
    assert control.actualizar("indice_medio", "puño_cerrado", True) is True
    assert control.obtener_acorde() == "D menor"


# --- Independencia de nota y tipo -------------------------------------

def test_cambiar_nota_conserva_tipo(control):
    control.actualizar("indice", "puño_cerrado", True)         # C menor
    control.actualizar("indice_medio", "puño_cerrado", True)   # D
    assert control.obtener_acorde() == "D menor"


def test_cambiar_tipo_conserva_nota(control):
    control.actualizar("indice_medio_anular", "puño_cerrado", True)    # E menor
    control.actualizar("indice_medio_anular", "mano_extendida", True)  # mayor
    assert control.obtener_acorde() == "E mayor"


# --- Cuándo suena -----------------------------------------------------

def test_misma_nota_sostenida_no_vuelve_a_sonar(control):
    assert control.actualizar("indice", "ninguno", False) is True
    assert control.actualizar("indice", "ninguno", False) is False


def test_repetir_la_misma_nota_despues_de_soltar(control):
    control.actualizar("indice", "mano_extendida", True)   # C mayor
    control.actualizar("ninguno", "puño_cerrado", True)    # suelta la nota, tipo menor
    assert control.actualizar("indice", "puño_cerrado", True) is True
    assert control.obtener_acorde() == "C menor"


# --- Filtro de fotogramas (frames_estables) ---------------------------

def test_un_fotograma_aislado_no_cambia_el_acorde():
    control = ControlAcordes(frames_estables=5)
    for _ in range(10):
        control.actualizar("indice", "mano_extendida", True)
    assert control.obtener_acorde() == "C mayor"

    # La cámara pierde la mano de notas durante un solo fotograma.
    assert control.actualizar("ninguno", "mano_extendida", True) is False
    assert control.obtener_acorde() == "C mayor"

    # Y pierde la mano de tipo durante un solo fotograma.
    control.actualizar("indice", "mano_extendida", False)
    assert control.obtener_acorde() == "C mayor"


def _sonidos(control, secuencia_notas):
    return sum(control.actualizar(gesto, "ninguno", False) for gesto in secuencia_notas)


def test_sin_filtro_un_parpadeo_corta_y_repite_el_sonido():

    secuencia = ["indice_medio"] * 6 + ["ninguno"] + ["indice_medio"] * 6
    assert _sonidos(ControlAcordes(frames_estables=1), secuencia) == 3


def test_con_filtro_de_3_un_parpadeo_no_afecta_el_sonido():
    secuencia = ["indice_medio"] * 6 + ["ninguno"] + ["indice_medio"] * 6
    assert _sonidos(ControlAcordes(frames_estables=3), secuencia) == 1


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


def test_normal_es_una_sola_nota(control):
    control.actualizar("indice", "mano_extendida", False)
    frecuencias = control.obtener_frecuencias()
    assert len(frecuencias) == 1
    assert frecuencias[0] == pytest.approx(261.63, abs=0.01)


# --- Sintetizador (solo generación de onda, sin reproducir) -----------

def test_el_volumen_configurado_no_supera_1():
    assert 0 < VOLUMEN <= 1.0


@pytest.mark.parametrize("gesto_tipo, visible", [
    ("mano_extendida", True),   # acorde mayor (3 notas)
    ("puño_cerrado", True),     # acorde menor (3 notas)
    (None, False),              # nota sola
])
def test_onda_no_satura_y_tiene_senal(control, gesto_tipo, visible):
    control.actualizar("indice", gesto_tipo, visible)
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

ETIQUETA_MANO_NOTAS = "Right"
ETIQUETA_MANO_TIPO = "Left"


class Simulador:
    def __init__(self):
        gestos.ultimo_gesto = {}
        self.control = ControlAcordes(frames_estables=1)
        self.actual = {"Left": "ninguno", "Right": "ninguno"}

    def fotogramas(self, cantidad, landmarks_notas, landmarks_tipo):
        """Retorna los acordes que SONARON (cuando actualizar() dio True)."""
        manos = {ETIQUETA_MANO_NOTAS: landmarks_notas, ETIQUETA_MANO_TIPO: landmarks_tipo}
        sonaron = []
        for _ in range(cantidad):
            for etiqueta, landmarks in manos.items():
                gesto = gestos.detectar_gesto(landmarks, etiqueta)
                if gesto is not None:
                    self.actual[etiqueta] = gesto
            if self.control.actualizar(
                self.actual[ETIQUETA_MANO_NOTAS],
                self.actual[ETIQUETA_MANO_TIPO],
                bool(landmarks_tipo),
            ):
                sonaron.append(self.control.obtener_acorde())
        return sonaron


@pytest.mark.parametrize("dedos, nota", [
    (["indice"], "C"),
    (["indice", "medio"], "D"),
    (["indice", "medio", "anular"], "E"),
    (["indice", "medio", "anular", "menique"], "F"),
    (["medio", "anular", "menique"], "G"),
    (["indice", "menique"], "A"),
    (["menique"], "B"),
])
def test_los_siete_gestos_reales_producen_su_nota(dedos, nota):
    sim = Simulador()
    assert sim.fotogramas(3, construir_mano(dedos), SIN_MANO) == [nota]


def test_flujo_completo_solo_suena_con_la_mano_de_notas():
    sim = Simulador()
    indice = construir_mano(["indice"])
    indice_medio = construir_mano(["indice", "medio"])

    # Solo la mano de notas: suena C.
    assert sim.fotogramas(8, indice, SIN_MANO) == ["C"]
    # La mano de tipo cambia a mayor y luego a menor: NO suena nada.
    assert sim.fotogramas(8, indice, MANO_ABIERTA) == []
    assert sim.control.obtener_acorde() == "C mayor"
    assert sim.fotogramas(8, indice, MANO_PUNO) == []
    assert sim.control.obtener_acorde() == "C menor"
    # Nota nueva: suena con el tipo que ya estaba elegido.
    assert sim.fotogramas(8, indice_medio, MANO_PUNO) == ["D menor"]
    # La mano de tipo desaparece: vuelve a normal y NO suena nada.
    assert sim.fotogramas(8, indice_medio, SIN_MANO) == []
    assert sim.control.obtener_acorde() == "D"


def test_flujo_completo_la_mano_de_notas_baja_y_vuelve():
    sim = Simulador()
    sim.fotogramas(8, construir_mano(["indice"]), MANO_PUNO)      # C menor

    # La mano de notas baja: se corta el sonido (silencio), no se queda
    # el último acorde ni suena ningún tono.
    assert sim.fotogramas(8, SIN_MANO, MANO_PUNO) == ["silencio"]
    assert sim.control.obtener_frecuencias() == []

    # Vuelve con otro gesto y el sistema responde con el tipo conservado.
    assert sim.fotogramas(8, construir_mano(["menique"]), MANO_PUNO) == ["B menor"]


def test_flujo_completo_gesto_de_nota_en_la_mano_de_tipo_se_ignora():
    sim = Simulador()
    indice = construir_mano(["indice"])
    assert sim.fotogramas(8, indice, indice) == ["C"]
    assert sim.control.tipo_acorde == "normal"