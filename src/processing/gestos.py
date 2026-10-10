from src.processing.landmark import Landmark
import math
 
FACTOR_EXTENSION = 1.6
FACTOR_CERRADO = 0.95
FACTOR_PULGAR_ANULAR = 0.9
ultimo_gesto = {}
 
def calcular_distancia(punto1, punto2):
    dx = punto2.x - punto1.x
    dy = punto2.y - punto1.y
    dz = punto2.z - punto1.z
    return math.sqrt(dx**2 + dy**2 + dz**2)
 
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
 
def puno_cerrado(landmarks):
    puntas, mcps, mano_muneca = clasificar_landmarks(landmarks)
 
    if mano_muneca is None:
        return False

    if "pulgar" not in puntas or "anular" not in puntas:
        return False

    for dedo, punta in puntas.items():
        if dedo not in mcps:
            return False
        mcp = mcps[dedo]
        if (calcular_distancia(mano_muneca, punta) > FACTOR_CERRADO * calcular_distancia(mano_muneca, mcp)
            and dedo != "pulgar"):
            return False

    referencia = calcular_distancia(mano_muneca, mcps["medio"])
    dist_pulgar_anular = calcular_distancia(puntas["pulgar"], puntas["anular"])

    if dist_pulgar_anular > FACTOR_PULGAR_ANULAR * referencia:
        return False

    return True

def configuracion_dedos(landmarks, dedos_arriba):
    puntas, mcps, mano_muneca = clasificar_landmarks(landmarks)

    if mano_muneca is None:
        return False

    for dedo_arr in dedos_arriba:
        if dedo_arr not in mcps or dedo_arr not in puntas:
            return False

    for dedo, punta in puntas.items():
        mcp = mcps[dedo]
        if (dedo in dedos_arriba and calcular_distancia(mano_muneca, punta) < 
            FACTOR_EXTENSION * calcular_distancia(mano_muneca, mcp)):
            return False

        if (dedo not in dedos_arriba and calcular_distancia(mano_muneca, punta) > 
            FACTOR_CERRADO * calcular_distancia(mano_muneca, mcp) and dedo!="pulgar"): #No se tiene en cuenta pulgar
            return False 

    return True

def indice_extendido(landmarks):
    return configuracion_dedos(landmarks, ["indice"])

def indice_medio_extendido(landmarks):
    return configuracion_dedos(landmarks, ["indice", "medio"])

def indice_medio_anular_extendido(landmarks):
    return configuracion_dedos(landmarks, ["indice", "medio", "anular"])

def indice_medio_anular_menique_extendido(landmarks):
    return configuracion_dedos(landmarks, ["indice", "medio", "anular", "menique"])

def indice_menique_extendido(landmarks):
    return configuracion_dedos(landmarks, ["indice", "menique"])

def mano_extendida(landmarks):
    return configuracion_dedos(landmarks, ["indice", "medio", "anular", "menique", "pulgar"])

def medio_anular_menique(landmarks):
    return configuracion_dedos(landmarks, ["medio", "anular", "menique"])

def menique(landmarks):
    return configuracion_dedos(landmarks, ["menique"])
    

def seleccionar_gesto(landmarks):
    if mano_extendida(landmarks):
        return "mano_extendida"
    if puno_cerrado(landmarks):
        return "puño_cerrado"
    if indice_extendido (landmarks):
        return ("indice")
    if indice_medio_extendido(landmarks):
        return ("indice_medio")
    if indice_medio_anular_extendido(landmarks):
        return ("indice_medio_anular")
    if indice_medio_anular_menique_extendido(landmarks):
        return ("indice_medio_anular_menique")
    if indice_menique_extendido(landmarks):
        return ("indice_menique")
    if medio_anular_menique(landmarks):
        return ("medio_anular_menique")
    if menique(landmarks):
        return ("menique")
 
    return "ninguno"
 
def detectar_gesto(landmarks, mano):
    gesto = seleccionar_gesto(landmarks)
    global ultimo_gesto
    if (gesto == ultimo_gesto.get(mano)):
        return None
    else:
        ultimo_gesto[mano] = gesto
        return gesto
 

