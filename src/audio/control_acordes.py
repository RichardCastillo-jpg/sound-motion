
# ---------------------------------------------------------------------
# Configuración (todo lo ajustable está aquí, al inicio del archivo)
# ---------------------------------------------------------------------

# Marcador de silencio: la mano de notas no hace ningún gesto de nota.
NOTA_SILENCIO = "0"

GESTO_A_NOTA = {
    "indice": "C",
    "indice_medio": "D",
    "indice_medio_anular": "E",
    "indice_medio_anular_menique": "F",
    "medio_anular_menique": "G",
    "indice_menique": "A",
    "menique": "B",
    "ninguno": NOTA_SILENCIO,
}

# Gestos de la mano de tipo -> tipo de acorde.
GESTO_A_TIPO = {
    "mano_extendida": "mayor",
    "puño_cerrado": "menor",
}

# Tipo de acorde cuando la mano de tipo no se muestra.
TIPO_SIN_MANO = "normal"

# Número MIDI de cada nota raíz, en la octava 4 (C4 = 60 = do central).
NOTA_MIDI = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}

# Intervalos en semitonos desde la raíz.
#   mayor:  raíz, tercera mayor (4) y quinta (7).
#   menor:  raíz, tercera menor (3) y quinta (7).
#   normal: solo la raíz (una nota sola, sin acorde).
INTERVALOS_ACORDE = {
    "mayor": (0, 4, 7),
    "menor": (0, 3, 7),
    TIPO_SIN_MANO: (0,),
}

# Cuántos fotogramas seguidos debe mantenerse un gesto 
FRAMES_ESTABLES = 1

FRECUENCIA_LA4 = 440.0  # A4 = MIDI 69


def midi_a_frecuencia(nota_midi):
    """Convierte un número MIDI a frecuencia en Hz (afinación temperada)."""
    return FRECUENCIA_LA4 * 2 ** ((nota_midi - 69) / 12)


class ControlAcordes:

    def __init__(self, frames_estables=FRAMES_ESTABLES):
        # Hasta que el usuario elija una nota no existe acorde que sonar.
        self.nota_actual = None
        # La mano de tipo empieza sin mostrarse: "normal".
        self.tipo_acorde = TIPO_SIN_MANO

        self.frames_estables = frames_estables
        self._candidato = {"nota": None, "tipo": None}
        self._conteo = {"nota": 0, "tipo": 0}

    def _confirmar(self, clave, candidato):

        if candidato is None:
            self._candidato[clave] = None
            self._conteo[clave] = 0
            return None

        if candidato == self._candidato[clave]:
            self._conteo[clave] += 1
        else:
            self._candidato[clave] = candidato
            self._conteo[clave] = 1

        if self._conteo[clave] >= self.frames_estables:
            return candidato
        return None

    def actualizar(self, gesto_notas, gesto_tipo, mano_tipo_visible):

        nota_anterior = self.nota_actual

        nota = self._confirmar("nota", GESTO_A_NOTA.get(gesto_notas))
        if nota is not None:
            self.nota_actual = nota

        if mano_tipo_visible:
            candidato_tipo = GESTO_A_TIPO.get(gesto_tipo)
        else:
            candidato_tipo = TIPO_SIN_MANO
        tipo = self._confirmar("tipo", candidato_tipo)
        if tipo is not None:
            self.tipo_acorde = tipo

        return self.nota_actual != nota_anterior

    def obtener_acorde(self):

        if self.nota_actual is None:
            return None
        if self.nota_actual == NOTA_SILENCIO:
            return "silencio"
        if self.tipo_acorde == TIPO_SIN_MANO:
            return self.nota_actual
        return f"{self.nota_actual} {self.tipo_acorde}"

    def obtener_frecuencias(self):

        if self.nota_actual is None or self.nota_actual == NOTA_SILENCIO:
            return []
        raiz = NOTA_MIDI[self.nota_actual]
        return [
            midi_a_frecuencia(raiz + intervalo)
            for intervalo in INTERVALOS_ACORDE[self.tipo_acorde]
        ]