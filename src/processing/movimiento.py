class ProcesadorMovimiento:

    def calcular_desplazamiento(self, posicion_anterior, posicion_actual):
        desplazamiento_x = posicion_actual[0] - posicion_anterior[0]
        desplazamiento_y = posicion_actual[1] - posicion_anterior[1]

        return desplazamiento_x, desplazamiento_y