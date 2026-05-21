import cv2
import mediapipe as mp
import numpy as np
import time
import os
import threading
from playsound import playsound

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(static_image_mode=False,min_detection_confidence=0.5,min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()
print("Webcam opened successfully")

is_calibrated = False
calibration_frames = 0

calibration_shoulder_angles = []
calibration_neck_angles = []

shoulder_threshold = 0
neck_threshold = 0

last_alert_time = 0
alert_cooldown = 5  # seconds

sound_file = "alert.mp3"

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    denominator = np.linalg.norm(ba) * np.linalg.norm(bc)

    if denominator == 0:
        return 0

    cosine_angle = np.dot(ba, bc) / denominator
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)

    angle = np.degrees(np.arccos(cosine_angle))

    return angle

def draw_angle(frame, a, b, c, angle, color):
    cv2.line(frame, b, a, color, 2)
    cv2.line(frame, b, c, color, 2)

    cv2.circle(frame, a, 5, color, -1)
    cv2.circle(frame, b, 5, color, -1)
    cv2.circle(frame, c, 5, color, -1)

    cv2.putText(
        frame,
        f"{angle:.1f}",
        (b[0] + 10, b[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA
    )

def play_alert():
    if os.path.exists(sound_file):
        threading.Thread(
            target=playsound,
            args=(sound_file,),
            daemon=True
        ).start()

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        print("Failed to read frame")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    if results.pose_landmarks:

        landmarks = results.pose_landmarks.landmark
        h, w, _ = frame.shape

        left_shoulder = (
            int(landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].x * w),

            int(landmarks[
                mp_pose.PoseLandmark.LEFT_SHOULDER.value
            ].y * h)
        )

        right_shoulder = (
            int(landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            ].x * w),

            int(landmarks[
                mp_pose.PoseLandmark.RIGHT_SHOULDER.value
            ].y * h)
        )

        left_ear = (
            int(landmarks[
                mp_pose.PoseLandmark.LEFT_EAR.value
            ].x * w),

            int(landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y * h)
        )

        shoulder_angle = calculate_angle(left_shoulder,right_shoulder,(right_shoulder[0], 0))

        neck_angle = calculate_angle(left_ear,left_shoulder,(left_shoulder[0], 0))

        if not is_calibrated and calibration_frames < 30:

            calibration_shoulder_angles.append(
                shoulder_angle
            )

            calibration_neck_angles.append(
                neck_angle
            )

            calibration_frames += 1

            cv2.putText(frame,f"Calibrating... {calibration_frames}/30",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 255),2,cv2.LINE_AA) 

        elif not is_calibrated:

            shoulder_threshold = (
                np.mean(
                    calibration_shoulder_angles
                ) - 10
            )

            neck_threshold = (
                np.mean(calibration_neck_angles
                ) - 10
            )
            is_calibrated = True

            print("Calibration Complete!")

            print(f"Shoulder Threshold: "f"{shoulder_threshold:.1f}")

            print( f"Neck Threshold: " f"{neck_threshold:.1f}")

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        midpoint = (
            (left_shoulder[0] +
             right_shoulder[0]) // 2,

            (left_shoulder[1] +
             right_shoulder[1]) // 2
        )
        draw_angle(frame,left_shoulder,midpoint,(midpoint[0], 0),shoulder_angle,(255, 0, 0))

        draw_angle(frame,left_ear,left_shoulder,(left_shoulder[0], 0),neck_angle,(0, 255, 0))

        if is_calibrated:

            current_time = time.time()

            if (shoulder_angle < shoulder_threshold
                or
                neck_angle < neck_threshold ):

                status = "Poor Posture"
                color = (0, 0, 255)

                if (current_time -last_alert_time > alert_cooldown):

                    print("Poor posture detected!")
                    play_alert()

                    last_alert_time = (
                        current_time
                    )

            else:

                status = "Good Posture"
                color = (0, 255, 0)

            cv2.putText(frame,status,(10, 30),cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2,
                cv2.LINE_AA
            )

            cv2.putText(frame,f"Shoulder: "f"{shoulder_angle:.1f}/"f"{shoulder_threshold:.1f}",(10, 60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 255),2 )

            cv2.putText(frame,f"Neck: "f"{neck_angle:.1f}/"f"{neck_threshold:.1f}",(10, 90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 255, 255),2)
    cv2.namedWindow("Posture Corrector", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Posture Corrector", 900, 700)
    cv2.imshow("Posture Corrector",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()