from src.processing.landmark import Landmark


def crear_landmark_pose(nombre, indice, x, y, z, visibilidad=None, lateralidad=None):
    return Landmark(
        nombre,
        indice,
        x,
        y,
        z,
        "pose",
        lateralidad,
        visibilidad
    )


def crear_landmark_hand(nombre, indice, x, y, z, lateralidad=None):
    return Landmark(
        nombre,
        indice,
        x,
        y,
        z,
        "hand",
        lateralidad
    )


def crear_landmarks_pose(datos):
    landmarks = []

    for dato in datos:
        landmark = crear_landmark_pose(
            dato["nombre"],
            dato["indice"],
            dato["x"],
            dato["y"],
            dato["z"],
            dato.get("visibilidad"),
            dato.get("lateralidad")
        )

        landmarks.append(landmark)

    return landmarks


def crear_landmarks_hand(datos):
    landmarks = []

    for dato in datos:
        landmark = crear_landmark_hand(
            dato["nombre"],
            dato["indice"],
            dato["x"],
            dato["y"],
            dato["z"],
            dato.get("lateralidad")
        )

        landmarks.append(landmark)

    return landmarks