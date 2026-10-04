from src.processing.landmark import Landmark
import math
 
FACTOR_EXTENSION = 1.4
ultimo_gesto = {}
 
def calcular_distancia(punto1, punto2):
    dx = punto2.x - punto1.x
    dy = punto2.y - punto1.y
    return math.sqrt(dx**2 + dy**2)
 
def clasificar_landmarks(landmarks):
    puntas = {}
    mcps = {}
    mano_muneca = None
 
    for landmark in landmarks:
        if landmark.nombre.endswith("_punta"):
            dedo = landmark.nombre.replace("_punta", "")
            puntas[dedo] = landmark
        elif landmark.nombre.endswith("_mcp"):
            dedo = landmark.nombre.replace("_mcp", "")
            mcps[dedo] = landmark
        elif landmark.nombre == "mano_muñeca":
            mano_muneca = landmark
 
    return puntas, mcps, mano_muneca
 
def mano_extendida(landmarks):
    puntas, mcps, mano_muneca = clasificar_landmarks(landmarks)
 
    if mano_muneca is None:
        return False
 
    for dedo, punta in puntas.items():
        if dedo not in mcps:
            return False 
        mcp = mcps[dedo]
        if calcular_distancia(mano_muneca, punta) < FACTOR_EXTENSION * calcular_distancia(mano_muneca, mcp):
            return False
 
    return True
 
def puno_cerrado(landmarks):
    puntas, mcps, mano_muneca = clasificar_landmarks(landmarks)
 
    if mano_muneca is None:
        return False
 
    for dedo, punta in puntas.items():
        if dedo not in mcps:
            return False
        mcp = mcps[dedo]
        if calcular_distancia(mano_muneca, punta) > FACTOR_EXTENSION * calcular_distancia(mano_muneca, mcp):
            return False
 
    return True
 
def pulgar_arriba(landmarks):
    puntas, mcps, mano_muneca = clasificar_landmarks(landmarks)
 
    if mano_muneca is None:
        return False
 
    if "pulgar" not in mcps or "pulgar" not in puntas:
        return False
    
    for dedo, punta in puntas.items():
        if dedo not in mcps:
            return False
        mcp = mcps[dedo]
        if (calcular_distancia(mano_muneca, punta) > FACTOR_EXTENSION * calcular_distancia(mano_muneca, mcp)
            and dedo != "pulgar"):
            return False
 
    dx = puntas["pulgar"].x - mcps["pulgar"].x
    dy = puntas["pulgar"].y - mcps["pulgar"].y
 
    if abs(dy) < abs(dx) or dy >= 0:
        return False
 
    return True
    
def seleccionar_gesto(landmarks):
    if mano_extendida(landmarks):
        return "mano_extendida"
    if pulgar_arriba(landmarks): 
        return "pulgar_arriba"
    if puno_cerrado(landmarks):
        return "puño_cerrado" 
 
    return "ninguno"
 
def detectar_gesto(landmarks, mano):
    gesto = seleccionar_gesto(landmarks)
    global ultimo_gesto
    if (gesto == ultimo_gesto.get(mano)):
        return None
    else:
        ultimo_gesto[mano] = gesto
        return gesto
 

