import cv2
import time
import numpy as np
import mediapipe as mp
from deepface import DeepFace
import os

# Logging function
def log_event(state):
    with open("log.txt", "a") as log:
        log.write(f"{time.ctime()}: {state}\n")
    if state == "stress":
        open("pause.flag", "w").close()

# Eye tracking setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()
blink_start = None
blink_threshold = 3.0  # reduced to 3 seconds for quicker fatigue detection

cap = cv2.VideoCapture(0)
last_check = time.time()
current_emotion = "Analyzing..."

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    fatigue = False
    if results.multi_face_landmarks:
        blink_start = time.time()
    elif blink_start and time.time() - blink_start > blink_threshold:
        fatigue = True
        log_event("fatigue")
        blink_start = None

    # Emotion detection every 3 seconds
    if time.time() - last_check > 3:
        try:
            analysis = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
            dominant_emotion = analysis[0]["dominant_emotion"]
            current_emotion = dominant_emotion  # Show on screen

            if dominant_emotion in ["angry", "sad", "fear"]:
                log_event("stress")
            else:
                log_event("normal")
        except Exception as e:
            print("Emotion detection failed:", e)
            current_emotion = "Error"
        last_check = time.time()

    # Display the current emotion on the video feed
    cv2.putText(frame, f"Emotion: {current_emotion}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show fatigue warning on screen
    if fatigue:
        cv2.putText(frame, "Fatigue Detected!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("AI DevOps Cognitive Monitor", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
