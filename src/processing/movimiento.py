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

    UMBRAL_MOVIMIENTO = 0.02

    def determinar_direccion(self, movimiento, umbral=UMBRAL_MOVIMIENTO):

        valor_x, valor_y = movimiento

        hay_movimiento_x = abs(valor_x) >= umbral

        hay_movimiento_y = abs(valor_y) >= umbral


        if not hay_movimiento_x and not hay_movimiento_y:

            return "sin_movimiento"
        

        if hay_movimiento_x and hay_movimiento_y:

            if abs(valor_x) >= abs(valor_y):

                hay_movimiento_y = False

            else:

                hay_movimiento_x = False


        if hay_movimiento_x:

            return "derecha" if valor_x > 0 else "izquierda"


        return "abajo" if valor_y > 0 else "arriba"
