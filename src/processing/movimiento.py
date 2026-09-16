import math
import time
class ProcesadorMovimiento:

    def __init__(self):
        self.posiciones_anterior = {}
        self.tiempo_anterior = None

    def calcular_distancia(self, punto1, punto2):
        dx = punto2[0] - punto1[0]
        dy = punto2[1] - punto1[1]
        dz = punto2[2] - punto1[2]

        distancia = math.sqrt(
            dx ** 2 +
            dy ** 2 +
            dz ** 2
        )

        return distancia

    def calcular_velocidad(self, nombre, posicion_actual):
        tiempo_actual = time.time()

        if self.tiempo_anterior is None:
            self.posiciones_anterior[nombre] = posicion_actual
            self.tiempo_anterior = tiempo_actual
            return 0.0

        if nombre not in self.posiciones_anterior:
            self.posiciones_anterior[nombre] = posicion_actual
            return 0.0

        posicion_anterior = self.posiciones_anterior[nombre]

        distancia = self.calcular_distancia(
            posicion_anterior,
            posicion_actual
        )

        tiempo = tiempo_actual - self.tiempo_anterior

        self.posiciones_anterior[nombre] = posicion_actual

        if tiempo <= 0:
            return 0.0

        return distancia / tiempo

    def actualizar_tiempo(self):
        self.tiempo_anterior = time.time()

