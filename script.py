import mediapipe as mp
import cv2
import time
from datetime import datetime
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'pose_landmarker_full.task'

UPPER_BODY_LANDMARKS = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
UMBRAL = 0.3
last_result = None

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global last_result 
    last_result = result
    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
        for i in UPPER_BODY_LANDMARKS: 
            punto = landmarks[i]
            if punto.visibility >= UMBRAL:
                print(f"Landmark {i} x={punto.x:.3f} y={punto.y:.3f} z={punto.z:.3f} vis={punto.visibility:.2f}")

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0) #Primera camara que encuentre

    while True:
        ok, frame = cap.read()

        if not ok:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   #convertir BGR -> RGB
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)  #envolverlo
        timestamp_ms = int(time.time()*1000)
        landmarker.detect_async(mp_image, timestamp_ms)

        if last_result != None:
            landmarks = last_result.pose_landmarks[0]
            for i in UPPER_BODY_LANDMARKS: 
                point = landmarks[i]
                if point.visibility >= UMBRAL:
                    height, width = frame.shape[:2]
                    x_px = int(point.x*width)
                    y_px = int(point.y*height)
                    cv2.circle(frame, (x_px, y_px), 5, (255, 0, 0), -1) #cv2.circle(frame, (x_px, y_px), radio, color, grosor)


        cv2.imshow("Mi camara", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
