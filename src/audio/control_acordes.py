"""
Control de acordes de SoundMotion.

Interpreta los gestos reconocidos por gestos.py y mantiene el estado musical:

- Mano de notas (derecha del usuario): el gesto elige la nota raíz
  (C, D, E, F, G, A o B).
- Mano de tipo (izquierda del usuario):
    * mano extendida -> acorde mayor
    * puño cerrado   -> acorde menor
    * mano no visible -> "nada" (se toca solo la nota raíz)

Separación de responsabilidades:
- gestos.py solo reconoce QUÉ gesto hace cada mano.
- Este módulo decide QUÉ SIGNIFICA ese gesto musicalmente.
- No depende de MediaPipe, de la cámara ni de ninguna librería de audio.
"""

# ---------------------------------------------------------------------
# Configuración (todo lo ajustable está aquí, al inicio del archivo)
# ---------------------------------------------------------------------

# Gestos de la mano de notas -> nota raíz.
# Los nombres de los gestos son exactamente los que devuelve
# seleccionar_gesto() en gestos.py.
# Criterio: de C a G, la cantidad de dedos extendidos coincide con la
# posición de la nota (1 dedo = C ... 5 dedos = G). A y B usan los dos
# gestos restantes.
GESTO_A_NOTA = {
    "indice": "C",
    "indice_medio": "D",
    "indice_medio_anular": "E",
    "indice_medio_anular_menique": "F",
    "medio_anular_menique": "G",
    "indice_menique": "A",
    "menique": "B",
    "ninguno": "0"
}

# Gestos de la mano de tipo -> tipo de acorde.
GESTO_A_TIPO = {
    "mano_extendida": "mayor",
    "puño_cerrado": "menor",
}

# Tipo de acorde cuando la mano de tipo no se muestra.
TIPO_SIN_MANO = "normal"

# Número MIDI de cada nota raíz, en la octava 4 (C4 = 60 = do central).
NOTA_MIDI = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71, "0":0}

# Intervalos en semitonos desde la raíz.
#   mayor: raíz, tercera mayor (4) y quinta (7).
#   menor: raíz, tercera menor (3) y quinta (7).
#   nada:  solo la raíz (una nota sola, sin acorde).
# Si se prefiere silencio en vez de la nota sola, usar () en "nada".
INTERVALOS_ACORDE = {
    "mayor": (0, 4, 7),
    "menor": (0, 3, 7),
    TIPO_SIN_MANO: (0,),
}

# Cuántos fotogramas seguidos debe mantenerse un gesto (o la ausencia de
# la mano) antes de aceptarlo. Evita que una detección fallida de un solo
# fotograma cambie el acorde o dispare el sonido por error.
FRAMES_ESTABLES = 1

FRECUENCIA_LA4 = 440.0  # A4 = MIDI 69


def midi_a_frecuencia(nota_midi):
    """Convierte un número MIDI a frecuencia en Hz (afinación temperada)."""
    if nota_midi == 0:
        return 0
    else:
        return FRECUENCIA_LA4 * 2 ** ((nota_midi - 69) / 12)


class ControlAcordes:
    """
    Mantiene de forma independiente la nota actual y el tipo de acorde.

    - Cambiar la nota conserva el tipo de acorde.
    - Cambiar el tipo de acorde conserva la nota.
    - Si la mano de notas deja de verse, se conserva la última nota.
    - Si la mano de tipo deja de verse, el tipo pasa a "normal".
    """

    def __init__(self, frames_estables=FRAMES_ESTABLES):
        # Hasta que el usuario elija una nota no existe acorde que sonar.
        self.nota_actual = None
        # La mano de tipo empieza sin mostrarse: "nada".
        self.tipo_acorde = TIPO_SIN_MANO

        self.frames_estables = frames_estables
        self._candidato = {"nota": None, "tipo": None}
        self._conteo = {"nota": 0, "tipo": 0}

    def _confirmar(self, clave, candidato):
        """
        Retorna el candidato solo si lleva frames_estables fotogramas
        seguidos siendo el mismo; en caso contrario retorna None.
        Un candidato None (gesto no reconocido) reinicia la cuenta.
        """
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
        """
        Debe llamarse una vez por fotograma.

        gesto_notas: gesto actual de la mano de notas (el de gestos.py).
                     "ninguno" o None conservan la nota actual.
        gesto_tipo: gesto actual de la mano de tipo. Si no es mayor ni
                    menor ("ninguno", None, otro gesto) conserva el tipo.
        mano_tipo_visible: True si la mano de tipo aparece en cámara.
                    Si es False el tipo pasa a "normal", sin importar
                    gesto_tipo.

        Retorna True si el acorde resultante cambió.
        """
        acorde_anterior = self.obtener_acorde()

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

        return self.obtener_acorde() != acorde_anterior

    def obtener_acorde(self):
        """
        Retorna el acorde actual como texto ("C menor", "C mayor"), o solo
        la nota ("C") si la mano de tipo no se muestra. Retorna None si
        aún no se ha seleccionado una nota.
        """
        if self.nota_actual is None:
            return None
        if self.tipo_acorde == TIPO_SIN_MANO:
            return self.nota_actual
        return f"{self.nota_actual} {self.tipo_acorde}"

    def obtener_frecuencias(self):
        """Retorna las frecuencias (Hz) del acorde actual, o una lista
        vacía si aún no hay acorde."""
        if self.nota_actual is None:    
            return []
        raiz = NOTA_MIDI[self.nota_actual]
        return [
            midi_a_frecuencia(raiz + intervalo)
            for intervalo in INTERVALOS_ACORDE[self.tipo_acorde]
        ]