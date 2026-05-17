import cv2
import time
from collections import Counter
from deepface import DeepFace

camera = cv2.VideoCapture(0)

last_check = 0
check_delay = 2

emotion_history = []
current_emotion = "Starting..."

anger_level = 0
ANGER_THRESHOLD = 3

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera not working")
        break

    current_time = time.time()

    if current_time - last_check > check_delay:

        last_check = current_time

        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            emotions = result[0]["emotion"]

            detected_emotion = max(emotions, key=emotions.get)
            confidence = emotions[detected_emotion]

            if confidence > 40:

                emotion_history.append(detected_emotion)

                if len(emotion_history) > 5:
                    emotion_history.pop(0)

                current_emotion = Counter(
                    emotion_history
                ).most_common(1)[0][0]

                # anger system
                if current_emotion == "angry":
                    anger_level += 1
                else:
                    anger_level = max(0, anger_level - 1)

        except:
            current_emotion = "No face"

    # emotion text
    cv2.putText(frame,
                f"Emotion: {current_emotion}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2)

    # anger level text
    cv2.putText(frame,
                f"Anger Level: {anger_level}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2)

    # warning system
    if anger_level >= ANGER_THRESHOLD:

        cv2.putText(frame,
                    "RageGuard Warning!",
                    (30, 170),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3)

        cv2.putText(frame,
                    "Take a short break.",
                    (30, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3)

    cv2.imshow("RageGuard AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()