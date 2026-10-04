import mediapipe as mp
import cv2
import time
from pythonosc import udp_client
from src.integration.vision_processing import crear_landmarks_pose, crear_landmarks_hand
from src.processing.gestos import seleccionar_gesto
from src.processing.movimiento import ProcesadorMovimiento

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

model_path = 'pose_landmarker_full.task'
hand_model_path = 'hand_landmarker.task'

UPPER_BODY_LANDMARKS = [11, 12, 13, 14, 15, 16, 23, 24]

LANDMARKS_NAMES = {
    11: "hombro_izquierdo",
    12: "hombro_derecho",
    13: "codo_izquierdo",
    14: "codo_derecho",
    15: "muñeca_izquierda",
    16: "muñeca_derecha",
    23: "cadera_izquierda",
    24: "cadera_derecha",
    }

HAND_LANDMARKS_NAMES = {
    0: "mano_muñeca",
    1: "pulgar_cmc",
    2: "pulgar_mcp",
    3: "pulgar_ip",
    4: "pulgar_punta",
    5: "indice_mcp",
    6: "indice_pip",
    7: "indice_dip",
    8: "indice_punta",
    9: "medio_mcp",
    10: "medio_pip",
    11: "medio_dip",
    12: "medio_punta",
    13: "anular_mcp",
    14: "anular_pip",
    15: "anular_dip",
    16: "anular_punta",
    17: "menique_mcp",
    18: "menique_pip",
    19: "menique_dip",
    20: "menique_punta",
}

MAX_DESPLAZAMIENTO_MUNECA = 0.20
VISIBILITY_THRESHOLD = 0.7
last_hand_timestamp_ms = None
last_result = None
last_hand_result = None

procesador_movimiento = ProcesadorMovimiento()

posicion_anterior_muneca_derecha = None
tiempo_anterior_muneca_derecha = None
ultimo_timestamp_hand_procesado = None

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult


def on_pose_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_result 
    last_result = result

def on_hands_result(
    result: HandLandmarkerResult,
    output_image: mp.Image,
    timestamp_ms: int
):

    global last_hand_result, last_hand_timestamp_ms

    last_hand_result = result
    last_hand_timestamp_ms = timestamp_ms

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=on_pose_result)

hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=hand_model_path),
        num_hands=2,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=on_hands_result)

with PoseLandmarker.create_from_options(options) as landmarker, HandLandmarker.create_from_options(hand_options) as handLandmarker:
    cap = cv2.VideoCapture(0)  # Primera camara que encuentre

    while True:

        ok, frame = cap.read()

        if not ok:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #convertir BGR -> RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)  #envolverlo
        timestamp_ms = int(time.time()*1000)

        landmarker.detect_async(mp_image, timestamp_ms)
        handLandmarker.detect_async(mp_image, timestamp_ms)
        
        height, width = frame.shape[:2]

        # ---------------------------
        # POSE
        # ---------------------------

        pose_result = last_result

        if pose_result is not None and pose_result.pose_landmarks:
            landmarks = pose_result.pose_landmarks[0]
            datos_pose = []
            
            for i in UPPER_BODY_LANDMARKS: 
                point = landmarks[i]

                if point.visibility >= VISIBILITY_THRESHOLD: 
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    
                    cv2.circle(frame, (x_px, y_px), 5, (255, 0, 0), -1) #cv2.circle(frame, (x_px, y_px), radio, color, grosor)

                    osc_client.send_message("/pose/" + LANDMARKS_NAMES[i], [point.x, point.y, point.z])
                    datos_pose.append({
                        "nombre": LANDMARKS_NAMES[i],
                        "indice": i,
                        "x": point.x,
                        "y": point.y,
                        "z": point.z,
                        "visibilidad": point.visibility
                    })

            landmarks_pose = crear_landmarks_pose(datos_pose)


        # ---------------------------
        # HANDS
        # ---------------------------

        hand_result = last_hand_result
        hand_timestamp_ms = last_hand_timestamp_ms

        landmarks_left = []
        landmarks_right = []

        if hand_result is not None:
            for hand, hand_info in zip(
                hand_result.hand_landmarks,
                hand_result.handedness
            ):
                lateralidad = hand_info[0].category_name 
                datos_hand = []  

                for i, point in enumerate(hand):
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)

                    cv2.circle(frame, (x_px, y_px), 5, (0, 0, 255), -1) 

                    osc_client.send_message(f"/hand/{lateralidad}/{HAND_LANDMARKS_NAMES[i]}", [point.x, point.y, point.z])
                    datos_hand.append({
                        "nombre": HAND_LANDMARKS_NAMES[i],
                        "indice": i,
                        "x": point.x,
                        "y": point.y,
                        "z": point.z,
                        "lateralidad": lateralidad
                    })

                landmarks_hand = crear_landmarks_hand(datos_hand)
                if lateralidad == "Left":
                    landmarks_left = landmarks_hand
                elif lateralidad == "Right":
                    landmarks_right = landmarks_hand

        # ---------------------------
        # MOVIMIENTO MANO DERECHA
        # ---------------------------

        if not landmarks_right:
            posicion_anterior_muneca_derecha = None
            tiempo_anterior_muneca_derecha = None

        elif (
            hand_timestamp_ms is not None
            and hand_timestamp_ms != ultimo_timestamp_hand_procesado
        ):

            muneca_derecha = None

            for landmark in landmarks_right:
                if landmark.nombre == "mano_muñeca":
                    muneca_derecha = landmark
                    break

            if muneca_derecha is not None:
                if not (
                    0 <= muneca_derecha.x <= 1
                    and 0 <= muneca_derecha.y <= 1
                ):
                    posicion_anterior_muneca_derecha = None
                    tiempo_anterior_muneca_derecha = None

                else:
                    posicion_actual = (
                        muneca_derecha.x,
                        muneca_derecha.y
                    )

                    tiempo_actual = hand_timestamp_ms / 1000.0

                    if (
                        posicion_anterior_muneca_derecha is not None
                        and tiempo_anterior_muneca_derecha is not None
                    ):
                        desplazamiento = procesador_movimiento.calcular_desplazamiento(
                            posicion_anterior_muneca_derecha,
                            posicion_actual
                        )

                        dx, dy = desplazamiento

                        if (abs(dx) > MAX_DESPLAZAMIENTO_MUNECA or abs(dy) > MAX_DESPLAZAMIENTO_MUNECA):
                            posicion_anterior_muneca_derecha = None
                            tiempo_anterior_muneca_derecha = None
                        else:
                            tiempo_transcurrido = (
                                tiempo_actual
                                - tiempo_anterior_muneca_derecha
                            )

                            velocidad = procesador_movimiento.calcular_velocidad(
                                desplazamiento,
                                tiempo_transcurrido
                            )

                            direccion = procesador_movimiento.determinar_direccion(
                                desplazamiento
                            )
                            posicion_anterior_muneca_derecha = posicion_actual
                            tiempo_anterior_muneca_derecha = tiempo_actual

                    else:
                        posicion_anterior_muneca_derecha = posicion_actual
                        tiempo_anterior_muneca_derecha = tiempo_actual

            ultimo_timestamp_hand_procesado = hand_timestamp_ms

        # ---------------------------
        # GESTOS
        # ---------------------------

        gesto_left = detectar_gesto(landmarks_left, "Left")
        gesto_right = detectar_gesto(landmarks_right, "Right")

        # ---------------------------
        # MOSTRAR CAMARA
        # ---------------------------

        cv2.imshow("Mi camara", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
