import cv2
import mediapipe as mp
import math
import time
import os

camera = cv2.VideoCapture(0)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

blink_count = 0
eye_closed = False

THRESHOLD = 55   # Blink threshold (adjust if needed)

start_time = time.time()

alert_played = False

while True:
    success, frame = camera.read()

    if not success:
        break

    # Mirror effect (optional but feels natural)
    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            h, w, c = frame.shape

            left_top = face_landmarks.landmark[159]
            left_bottom = face_landmarks.landmark[145]

            x1 = int(left_top.x * w)
            y1 = int(left_top.y * h)

            x2 = int(left_bottom.x * w)
            y2 = int(left_bottom.y * h)

            cv2.circle(frame, (x1, y1), 5, (0,255,255), -1)
            cv2.circle(frame, (x2, y2), 5, (0,255,255), -1)

            cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 2)

            left_distance = math.sqrt(
                (x2 - x1)**2 +
                (y2 - y1)**2
            )

            right_top = face_landmarks.landmark[386]
            right_bottom = face_landmarks.landmark[374]

            x3 = int(right_top.x * w)
            y3 = int(right_top.y * h)

            x4 = int(right_bottom.x * w)
            y4 = int(right_bottom.y * h)

            cv2.circle(frame, (x3, y3), 5, (0,255,255), -1)
            cv2.circle(frame, (x4, y4), 5, (0,255,255), -1)

            cv2.line(frame, (x3, y3), (x4, y4), (0,255,0), 2)

            right_distance = math.sqrt(
                (x4 - x3)**2 +
                (y4 - y3)**2
            )

            avg_distance = (
                left_distance +
                right_distance
            ) / 2

            cv2.putText(
                frame,
                f"Eye Distance: {avg_distance:.2f}",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            if avg_distance < THRESHOLD:

                if not eye_closed:
                    blink_count += 1
                    eye_closed = True

            else:
                eye_closed = False

            cv2.putText(
                frame,
                f"Blinks: {blink_count}",
                (50, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            left_eye_corner = face_landmarks.landmark[33]
            right_eye_corner = face_landmarks.landmark[263]

            x_left = int(left_eye_corner.x * w)
            x_right = int(right_eye_corner.x * w)

            eye_width = abs(x_right - x_left)

            cv2.putText(
                frame,
                f"Screen Distance Score: {eye_width}",
                (50, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,255),
                2
            )

            if eye_width > 350:

                cv2.putText(
                    frame,
                    "Too Close!! Move Back!",
                    (50, 170),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,0,255),
                    3
                )
            

    elapsed_time = time.time() - start_time

    if elapsed_time > 20:

        cv2.putText(
            frame,
            "Take a Break 😭",
            (100, 250),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )

        if not alert_played:
            os.system(
                "afplay /System/Library/Sounds/Glass.aiff"
            )
            alert_played = True

    cv2.imshow("Smart Eye Tracker 😭", frame)

    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()