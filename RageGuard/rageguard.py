import cv2
import time
import csv
import os
from datetime import datetime
from collections import Counter
from deepface import DeepFace

# OPTIONAL SOUND
try:
    import winsound
    SOUND_AVAILABLE = True
except:
    SOUND_AVAILABLE = False

# OPTIONAL MICROPHONE
try:
    import sounddevice as sd
    import numpy as np
    VOICE_AVAILABLE = True
except:
    VOICE_AVAILABLE = False

# SETTINGS
CHECK_DELAY = 3
VOICE_CHECK_DELAY = 2
VOICE_THRESHOLD = 0.10
CONFIDENCE_THRESHOLD = 40

ANGER_THRESHOLD = 4
MAX_ANGER = 10

ALERT_DURATION = 4
ALERT_COOLDOWN = 10
SOUND_COOLDOWN = 10

CALIBRATION_SECONDS = 8
LOG_FILE = "rageguard_session_log.csv"

# CAMERA
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not working")
    exit()

# VARIABLES
last_check = 0
last_voice_check = 0
last_alert_time = 0
last_sound_time = 0
last_log_time = 0

emotion_history = []
current_emotion = "Starting"
current_confidence = 0

anger_level = 0
alert_active = False
alert_start_time = 0

voice_level = 0
voice_rage_detected = False

calibrating = True
calibration_start = time.time()
calibration_emotions = []
normal_emotion = "neutral"

# CREATE LOG FILE
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "emotion",
            "confidence",
            "anger_level",
            "voice_level",
            "voice_spike"
        ])

# DRAW HELPERS
def draw_text(frame, text, x, y,
              scale=0.5,
              color=(255, 255, 255),
              thickness=1):

    cv2.putText(
        frame,
        text,
        (x, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA
    )


# FIXED STABLE PANEL FUNCTION

def draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               border_color,
               fill_color=(10, 10, 10),
               thickness=2,
               alpha=0.7):

    overlay = frame.copy()

    # transparent fill
    cv2.rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        fill_color,
        -1
    )

    # blend
    cv2.addWeighted(
        overlay,
        alpha,
        frame,
        1 - alpha,
        0,
        frame
    )

    # border
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        border_color,
        thickness
    )


# COLORS
def get_emotion_color(emotion):

    if emotion == "angry":
        return (0, 0, 255)

    elif emotion == "happy":
        return (0, 255, 0)

    elif emotion == "sad":
        return (255, 180, 0)

    return (180, 180, 180)


# UI PANELS
def draw_top_header(frame):

    width = frame.shape[1]

    draw_text(
        frame,
        "RAGEGUARD AI",
        20,
        32,
        0.9,
        (0, 0, 255),
        2
    )

    cv2.line(
        frame,
        (18, 45),
        (width - 18, 45),
        (50, 50, 50),
        1
    )

    cv2.circle(frame, (width - 40, 28), 5, (0, 255, 0), -1)

    draw_text(
        frame,
        "LIVE",
        width - 85,
        32,
        0.45,
        (0, 255, 0),
        1
    )


# EMOTION PANEL

def draw_emotion_panel(frame):

    color = get_emotion_color(current_emotion)

    x1 = 18
    y1 = 60
    x2 = 240
    y2 = 145

    draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               color,
               (5, 5, 5),
               2,
               0.65)

    draw_text(frame,
              "EMOTION",
              x1 + 12,
              y1 + 22,
              0.4,
              color,
              1)

    draw_text(frame,
              current_emotion.upper(),
              x1 + 12,
              y1 + 58,
              0.9,
              color,
              2)

    draw_text(frame,
              f"CONF: {int(current_confidence)}%",
              x1 + 12,
              y1 + 82,
              0.4,
              (220, 220, 220),
              1)


# ANGER BAR

def draw_bottom_anger_bar(frame):

    height, width, _ = frame.shape

    x1 = 20
    x2 = width - 20
    y1 = height - 70
    y2 = height - 28

    draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               (0, 0, 180),
               (5, 5, 5),
               2,
               0.6)

    draw_text(frame,
              "ANGER",
              x1 + 12,
              y1 + 26,
              0.55,
              (0, 0, 255),
              2)

    draw_text(frame,
              f"{anger_level}/{MAX_ANGER}",
              x2 - 65,
              y1 + 26,
              0.55,
              (0, 0, 255),
              2)

    bar_x1 = x1 + 85
    bar_x2 = x2 - 85
    bar_y1 = y1 + 14
    bar_y2 = y1 + 28

    cv2.rectangle(frame,
                  (bar_x1, bar_y1),
                  (bar_x2, bar_y2),
                  (45, 45, 45),
                  -1)

    fill_width = int(
        ((bar_x2 - bar_x1) * anger_level) / MAX_ANGER
    )

    if anger_level < 4:
        color = (0, 255, 0)
    elif anger_level < 7:
        color = (0, 255, 255)
    else:
        color = (0, 0, 255)

    cv2.rectangle(frame,
                  (bar_x1, bar_y1),
                  (bar_x1 + fill_width, bar_y2),
                  color,
                  -1)


# AI ASSISTANT

def get_assistant_message():

    if anger_level >= 8:
        return "Pause for 1 minute."

    elif anger_level >= 6:
        return "Relax your shoulders."

    elif anger_level >= 4:
        return "Breathe slowly."

    return "Stable. Stay focused."


# ASSISTANT PANEL

def draw_ai_assistant(frame):

    width = frame.shape[1]

    x2 = width - 20
    x1 = width - 320
    y1 = 60
    y2 = 145

    draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               (255, 180, 0),
               (5, 10, 14),
               2,
               0.65)

    draw_text(frame,
              "AI ASSISTANT",
              x1 + 12,
              y1 + 22,
              0.4,
              (255, 180, 0),
              1)

    draw_text(frame,
              get_assistant_message(),
              x1 + 12,
              y1 + 56,
              0.45,
              (255, 255, 255),
              1)

    draw_text(frame,
              f"NORMAL: {normal_emotion.upper()}",
              x1 + 12,
              y1 + 82,
              0.35,
              (180, 180, 180),
              1)


# WARNING PANEL

def draw_warning_panel(frame, current_time):

    width = frame.shape[1]

    blink = int(current_time * 5) % 2 == 0

    x2 = width - 20
    x1 = width - 280
    y1 = 165
    y2 = 240

    draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               (0, 0, 255),
               (18, 0, 0),
               2,
               0.72)

    if blink:
        cv2.rectangle(frame,
                      (x1, y1),
                      (x2, y2),
                      (0, 0, 255),
                      3)

    draw_text(frame,
              "RAGE DETECTED",
              x1 + 12,
              y1 + 24,
              0.55,
              (0, 0, 255),
              2)

    draw_text(frame,
              "Take a breath.",
              x1 + 12,
              y1 + 50,
              0.42,
              (255, 255, 255),
              1)

    draw_text(frame,
              f"ANGER: {anger_level}/{MAX_ANGER}",
              x1 + 12,
              y1 + 70,
              0.4,
              (0, 255, 255),
              1)


# FACE TRACKING

def draw_face_tracking(frame):

    height, width, _ = frame.shape

    cx = width // 2
    cy = height // 2

    size = 85
    line = 28

    color = (0, 255, 0)

    if anger_level >= ANGER_THRESHOLD:
        color = (0, 0, 255)

    x1 = cx - size
    y1 = cy - size
    x2 = cx + size
    y2 = cy + size

    cv2.line(frame, (x1, y1), (x1 + line, y1), color, 2)
    cv2.line(frame, (x1, y1), (x1, y1 + line), color, 2)

    cv2.line(frame, (x2, y1), (x2 - line, y1), color, 2)
    cv2.line(frame, (x2, y1), (x2, y1 + line), color, 2)

    cv2.line(frame, (x1, y2), (x1 + line, y2), color, 2)
    cv2.line(frame, (x1, y2), (x1, y2 - line), color, 2)

    cv2.line(frame, (x2, y2), (x2 - line, y2), color, 2)
    cv2.line(frame, (x2, y2), (x2, y2 - line), color, 2)


# MICROPHONE METER

def draw_mic_meter(frame):

    height = frame.shape[0]

    x1 = 20
    y1 = height - 115
    x2 = 170
    y2 = height - 82

    draw_panel(frame,
               x1,
               y1,
               x2,
               y2,
               (0, 255, 0),
               (5, 5, 5),
               1,
               0.6)

    draw_text(frame,
              "MIC",
              x1 + 10,
              y1 + 21,
              0.4,
              (0, 255, 0),
              1)

    meter_x1 = x1 + 42
    meter_x2 = x2 - 10
    meter_y1 = y1 + 10
    meter_y2 = y1 + 20

    cv2.rectangle(frame,
                  (meter_x1, meter_y1),
                  (meter_x2, meter_y2),
                  (40, 40, 40),
                  -1)

    fill_width = int(
        ((meter_x2 - meter_x1) * voice_level) / 100
    )

    color = (0, 255, 0)

    if voice_level > 45:
        color = (0, 255, 255)

    if voice_level > 70:
        color = (0, 0, 255)

    cv2.rectangle(frame,
                  (meter_x1, meter_y1),
                  (meter_x1 + fill_width, meter_y2),
                  color,
                  -1)


# FOOTER

def draw_footer(frame):

    height, width, _ = frame.shape

    y = height - 6

    voice_text = "VOICE: ON" if VOICE_AVAILABLE else "VOICE: OFF"
    sound_text = "SOUND: ON" if SOUND_AVAILABLE else "SOUND: OFF"

    draw_text(frame,
              voice_text,
              20,
              y,
              0.33,
              (160, 160, 160),
              1)

    draw_text(frame,
              sound_text,
              145,
              y,
              0.33,
              (160, 160, 160),
              1)

    draw_text(frame,
              "LOGGING: ON",
              260,
              y,
              0.33,
              (160, 160, 160),
              1)

    draw_text(frame,
              "Q: QUIT",
              width - 75,
              y,
              0.33,
              (160, 160, 160),
              1)


# CALIBRATION SCREEN

def draw_calibration_screen(frame, seconds_left):

    height, width, _ = frame.shape

    overlay = frame.copy()

    cv2.rectangle(overlay,
                  (0, 0),
                  (width, height),
                  (0, 0, 0),
                  -1)

    cv2.addWeighted(overlay,
                    0.55,
                    frame,
                    0.45,
                    0,
                    frame)

    x = max(30, width // 2 - 200)
    y = height // 2 - 40

    draw_text(frame,
              "RAGEGUARD CALIBRATION",
              x,
              y,
              0.8,
              (0, 255, 255),
              2)

    draw_text(frame,
              "Keep a normal face.",
              x,
              y + 35,
              0.5,
              (255, 255, 255),
              1)

    draw_text(frame,
              f"Starting in: {seconds_left}s",
              x,
              y + 70,
              0.65,
              (0, 255, 0),
              2)

# LOGIC
def play_alert_sound(current_time):

    global last_sound_time

    if current_time - last_sound_time < SOUND_COOLDOWN:
        return

    last_sound_time = current_time

    if SOUND_AVAILABLE:
        winsound.Beep(900, 120)
        winsound.Beep(650, 120)


# VOICE DETECTION

def detect_voice_rage():

    global voice_level
    global voice_rage_detected
    global anger_level

    if not VOICE_AVAILABLE:
        return

    try:
        duration = 0.1
        sample_rate = 16000

        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        volume = np.linalg.norm(audio) / len(audio)

        voice_level = min(100, int(volume * 1000))

        if volume > VOICE_THRESHOLD:
            voice_rage_detected = True
            anger_level = min(MAX_ANGER, anger_level + 1)
        else:
            voice_rage_detected = False

    except:
        voice_level = 0
        voice_rage_detected = False


# ANGER LOGIC

def apply_anger_logic(emotion):

    global anger_level

    if emotion == "angry":
        anger_level += 1

    elif emotion in ["disgust", "fear"]:
        anger_level += 1

    elif emotion == normal_emotion:
        anger_level -= 2

    else:
        anger_level -= 1

    anger_level = max(0, min(MAX_ANGER, anger_level))


# LOG SESSION

def log_session(current_time):

    global last_log_time

    if current_time - last_log_time < CHECK_DELAY:
        return

    last_log_time = current_time

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            current_emotion,
            int(current_confidence),
            anger_level,
            voice_level,
            voice_rage_detected
        ])

# MAIN LOOP
while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera not working")
        break

    current_time = time.time()

    # emotion detection
    if current_time - last_check >= CHECK_DELAY:

        last_check = current_time

        try:
            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            emotions = result[0]["emotion"]

            detected_emotion = max(emotions,
                                   key=emotions.get)

            confidence = emotions[detected_emotion]

            current_confidence = confidence

            if confidence > CONFIDENCE_THRESHOLD:

                emotion_history.append(detected_emotion)

                if len(emotion_history) > 5:
                    emotion_history.pop(0)

                current_emotion = Counter(
                    emotion_history
                ).most_common(1)[0][0]

                if calibrating:
                    calibration_emotions.append(current_emotion)
                else:
                    apply_anger_logic(current_emotion)

        except:
            current_emotion = "No face"
            current_confidence = 0

    # calibration mode
    if calibrating:

        elapsed = current_time - calibration_start

        seconds_left = max(
            0,
            int(CALIBRATION_SECONDS - elapsed)
        )

        draw_calibration_screen(frame,
                                seconds_left)

        if elapsed >= CALIBRATION_SECONDS:

            calibrating = False

            if calibration_emotions:
                normal_emotion = Counter(
                    calibration_emotions
                ).most_common(1)[0][0]
            else:
                normal_emotion = "neutral"

            anger_level = 0
            emotion_history.clear()

        cv2.imshow("RageGuard AI", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    # voice detection
    if current_time - last_voice_check >= VOICE_CHECK_DELAY:

        last_voice_check = current_time
        detect_voice_rage()

    # alerts
    if anger_level >= ANGER_THRESHOLD:

        if current_time - last_alert_time >= ALERT_COOLDOWN:

            alert_active = True
            alert_start_time = current_time
            last_alert_time = current_time

            play_alert_sound(current_time)

    if alert_active:

        if (
            anger_level < ANGER_THRESHOLD
            or current_time - alert_start_time > ALERT_DURATION
        ):
            alert_active = False

    # logging
    log_session(current_time)

    # draw UI
    draw_top_header(frame)
    draw_face_tracking(frame)
    draw_emotion_panel(frame)
    draw_ai_assistant(frame)
    draw_bottom_anger_bar(frame)
    draw_mic_meter(frame)

    if alert_active:
        draw_warning_panel(frame,
                           current_time)

    draw_footer(frame)

    cv2.imshow("RageGuard AI", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# CLEANUP
camera.release()
cv2.destroyAllWindows()
