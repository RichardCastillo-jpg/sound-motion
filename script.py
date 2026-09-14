import mediapipe as mp
import cv2
import time
from pythonosc import udp_client

osc_client = udp_client.SimpleUDPClient("127.0.0.1", 9000)

model_path = 'pose_landmarker_full.task'
hand_model_path = 'hand_landmarker.task'

UPPER_BODY_LANDMARKS = [11, 12, 13, 14, 15, 16, 23, 24]

LANDMARKS_NAMES = {
    11: "hombro_izquierdo",
    12: "hombro_derecho",
    13: "codo_izquierdo",
    14: "codo_derecho",
    15: "muneca_izquierda",
    16: "muneca_derecha",
    23: "cadera_izquierda",
    24: "cadera_derecha",
    }

HAND_LANDMARKS_NAMES = {
    0: "muneca",
    1: "pulgar_base",
    2: "pulgar_articulacion1",
    3: "pulgar_articulacion2",
    4: "pulgar_punta",
    5: "indice_base",
    6: "indice_articulacion1",
    7: "indice_articulacion2",
    8: "indice_punta",
    9: "medio_base",
    10: "medio_articulacion1",
    11: "medio_articulacion2",
    12: "medio_punta",
    13: "anular_base",
    14: "anular_articulacion1",
    15: "anular_articulacion2",
    16: "anular_punta",
    17: "menique_base",
    18: "menique_articulacion1",
    19: "menique_articulacion2",
    20: "menique_punta",
}
UMBRAL = 0.3
last_result = None
last_hand_result = None

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

def on_hands_result (result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_hand_result
    last_hand_result = result

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
    cap = cv2.VideoCapture(0) #Primera camara que encuentre

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

        if last_result != None is not last_result.pose_landmarks:
            landmarks = last_result.pose_landmarks[0]
            for i in UPPER_BODY_LANDMARKS: 
                point = landmarks[i]
                if point.visibility >= UMBRAL: 
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    cv2.circle(frame, (x_px, y_px), 5, (255, 0, 0), -1) #cv2.circle(frame, (x_px, y_px), radio, color, grosor)

                    osc_client.send_message("/pose/"+LANDMARKS_NAMES[i], [point.x, point.y, point.z])


        if last_hand_result is not None:
            for hand, hand_info in zip(last_hand_result.hand_landmarks, last_hand_result.handedness): 
                for i, point in enumerate(hand):
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    cv2.circle(frame, (x_px, y_px), 5, (0, 0, 255), -1) 

                    osc_client.send_message(f"/hand/{hand_info[0].category_name}/{HAND_LANDMARKS_NAMES[i]}", [point.x, point.y, point.z])


        cv2.imshow("Mi camara", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
