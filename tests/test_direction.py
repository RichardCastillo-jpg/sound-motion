import sys
from pathlib import Path

# Permite que los tests importen módulos de src/processing/
# sin necesidad de __init__.py ni cambiar los imports existentes.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "processing"))
import pytest
from movimiento import ProcesadorMovimiento

 
@pytest.fixture
def procesador():
    return ProcesadorMovimiento()
 
 
def mostrar_resultado(nombre_prueba, posicion_anterior, posicion_actual, desplazamiento, esperado, obtenido):
    print(f"\n{nombre_prueba}")
    print(f"  posicion_anterior = {posicion_anterior}")
    print(f"  posicion_actual   = {posicion_actual}")
    print(f"  desplazamiento    = {desplazamiento}")
    print(f"  direccion esperada = {esperado}")
    print(f"  direccion obtenida = {obtenido}")
 

def test_prueba1_derecha(procesador):
    posicion_anterior = (0.30, 0.50)
    posicion_actual = (0.45, 0.50)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 1 — Derecha", posicion_anterior, posicion_actual, desplazamiento, "derecha", direccion)
    assert direccion == "derecha"
 

def test_prueba2_izquierda(procesador):
    posicion_anterior = (0.45, 0.50)
    posicion_actual = (0.30, 0.50)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 2 — Izquierda", posicion_anterior, posicion_actual, desplazamiento, "izquierda", direccion)
    assert direccion == "izquierda"
 

def test_prueba3_arriba(procesador):
    posicion_anterior = (0.50, 0.60)
    posicion_actual = (0.50, 0.40)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 3 — Arriba", posicion_anterior, posicion_actual, desplazamiento, "arriba", direccion)
    assert direccion == "arriba"
 

def test_prueba4_abajo(procesador):
    posicion_anterior = (0.50, 0.40)
    posicion_actual = (0.50, 0.60)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 4 — Abajo", posicion_anterior, posicion_actual, desplazamiento, "abajo", direccion)
    assert direccion == "abajo"
 

def test_prueba5_sin_movimiento(procesador):
    posicion_anterior = (0.50, 0.50)
    posicion_actual = (0.50, 0.50)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 5 — Sin movimiento", posicion_anterior, posicion_actual, desplazamiento, "sin_movimiento", direccion)
    assert direccion == "sin_movimiento"
 

def test_prueba6_movimiento_pequeno(procesador):
    posicion_anterior = (0.500, 0.500)
    posicion_actual = (0.505, 0.498)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 6 — Movimiento pequeño (bajo el umbral)", posicion_anterior, posicion_actual, desplazamiento, "sin_movimiento", direccion)
    assert direccion == "sin_movimiento"
 

def test_prueba7_cambio_de_direccion(procesador):
    secuencia_posiciones = [
        (0.30, 0.50),
        (0.45, 0.50),  # derecha
        (0.30, 0.50),  # izquierda
        (0.30, 0.30),  # arriba
        (0.30, 0.50),  # abajo
    ]
    direcciones_esperadas = ["derecha", "izquierda", "arriba", "abajo"]
 
    print("\nPrueba 7 — Cambio de dirección (secuencia)")
    direcciones_obtenidas = []
    for i, (anterior, actual) in enumerate(zip(secuencia_posiciones, secuencia_posiciones[1:]), start=1):
        desplazamiento = procesador.calcular_desplazamiento(anterior, actual)
        direccion = procesador.determinar_direccion(desplazamiento)
        direcciones_obtenidas.append(direccion)
        print(f"  paso {i}: {anterior} -> {actual} | desplazamiento = {desplazamiento} "
              f"| esperado = {direcciones_esperadas[i-1]} | obtenido = {direccion}")
 
    assert direcciones_obtenidas == direcciones_esperadas
 

def test_prueba8_diagonal_prioriza_horizontal(procesador):
    posicion_anterior = (0.30, 0.50)
    posicion_actual = (0.50, 0.55)  # dx=0.20 (dominante), dy=0.05
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 8a — Diagonal, prioriza X", posicion_anterior, posicion_actual, desplazamiento, "derecha", direccion)
    assert direccion == "derecha"
 
 
def test_prueba8_diagonal_prioriza_vertical(procesador):
    posicion_anterior = (0.30, 0.50)
    posicion_actual = (0.35, 0.70)  # dx=0.05, dy=0.20 (dominante)
 
    desplazamiento = procesador.calcular_desplazamiento(posicion_anterior, posicion_actual)
    direccion = procesador.determinar_direccion(desplazamiento)
 
    mostrar_resultado("Prueba 8b — Diagonal, prioriza Y", posicion_anterior, posicion_actual, desplazamiento, "abajo", direccion)
    assert direccion == "abajo"
