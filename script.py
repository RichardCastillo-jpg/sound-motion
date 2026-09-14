import mediapipe as mp
import cv2
import time
from datetime import datetime
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'pose_landmarker_full.task'
hand_model_path = 'hand_landmarker.task'

UPPER_BODY_LANDMARKS = [11, 12, 13, 14, 15, 16, 23, 24]
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


def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_result 
    last_result = result

def print_hands_result (result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_hand_result
    last_hand_result = result

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

hand_options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=hand_model_path),
        num_hands=2,
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_hands_result)

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

        if last_result != None and last_result.pose_landmarks:
            landmarks = last_result.pose_landmarks[0]
            for i in UPPER_BODY_LANDMARKS: 
                point = landmarks[i]
                if point.visibility >= UMBRAL:
                    height, width = frame.shape[:2]
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    cv2.circle(frame, (x_px, y_px), 5, (255, 0, 0), -1) #cv2.circle(frame, (x_px, y_px), radio, color, grosor)

        if last_hand_result != None:
            for hand in last_hand_result.hand_landmarks: 
                for point in hand:
                    height, width = frame.shape[:2]
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    cv2.circle(frame, (x_px, y_px), 5, (0, 0, 255), -1) 


        cv2.imshow("Mi camara", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
