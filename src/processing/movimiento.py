class ProcesadorMovimiento:

    def calcular_desplazamiento(self, posicion_anterior, posicion_actual):
        desplazamiento_x = posicion_actual[0] - posicion_anterior[0]
        desplazamiento_y = posicion_actual[1] - posicion_anterior[1]

        return desplazamiento_x, desplazamiento_y

    def calcular_velocidad(self, desplazamiento, tiempo):
        if tiempo <= 0:
            return 0.0, 0.0

        velocidad_x = desplazamiento[0] / tiempo
        velocidad_y = desplazamiento[1] / tiempo

        return velocidad_x, velocidad_y