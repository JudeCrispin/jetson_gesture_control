import cv2
import mediapipe as mp
import time
import vlc
import os

# ================= VIDEO PLAYLIST =================
VIDEO_DIR = os.getcwd()

playlist = {
    0: os.path.join(VIDEO_DIR, "sample.mp4"),
    1: os.path.join(VIDEO_DIR, "sample2.mp4"),
    2: os.path.join(VIDEO_DIR, "sample3.mp4")
}

current_index = 0

# ================= VLC SETUP =================
instance = vlc.Instance()
player = instance.media_player_new()

def load_video(index):
    global current_index

    if index not in playlist:
        print("⚠ No more videos in playlist")
        return

    path = playlist[index]

    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return

    current_index = index
    media = instance.media_new(path)
    player.set_media(media)
    player.play()
    time.sleep(0.5)
    player.audio_set_volume(70)

    #print(f"🎬 Playing Video Index: {current_index}")

load_video(current_index)

# ================= MEDIAPIPE =================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# ================= CAMERA =================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not opened")
    exit()
else:
    print("✅ Camera opened")

# ================= GESTURE HOLD =================
GESTURE_HOLD_TIME = 0.2
gesture_start_time = None
last_gesture = None

# ================= FINGER STATE =================
def fingers_state(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    fingers.append(1 if hand_landmarks.landmark[4].x <
                   hand_landmarks.landmark[3].x else 0)

    # Other fingers
    for tip in tips[1:]:
        fingers.append(1 if hand_landmarks.landmark[tip].y <
                       hand_landmarks.landmark[tip-2].y else 0)

    return fingers


print("🚀 Gesture VLC Control Started")
print("Hold gesture for 1 sec")
print("Press 'q' to quit")

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(frame, hand_landmarks,
                                   mp_hands.HAND_CONNECTIONS)

            fingers = fingers_state(hand_landmarks)
            finger_count = sum(fingers)
            gesture_id = None

            # ================= GESTURES =================
            if finger_count == 0:
                gesture_id = "PAUSE"
            elif finger_count == 5:
                gesture_id = "PLAY"
            elif fingers == [0,0,0,0,1]:
                gesture_id = "SEEK_FORWARD"
            elif fingers == [1,0,0,0,0]:
                gesture_id = "SEEK_BACK"
            elif fingers == [0,1,0,0,0]:
                gesture_id = "VOL_UP"
            elif fingers == [0,1,1,0,1]:
                gesture_id = "VOL_DOWN"
            elif fingers == [0,1,1,0,0]:
                gesture_id = "RESTART"
            elif fingers == [0,1,1,1,1]:
                gesture_id = "MUTE"
            elif fingers == [1,1,1,0,0]:
                gesture_id = "NEXT_VIDEO"
            elif fingers == [1,1,0,0,0]:
                gesture_id = "PREV_VIDEO"
            elif fingers == [0,1,0,0,1]:
                gesture_id = "EXIT"

            current_time = time.time()

            if gesture_id:
                if gesture_id != last_gesture:
                    gesture_start_time = current_time
                    last_gesture = gesture_id

                elif current_time - gesture_start_time >= GESTURE_HOLD_TIME:

                    # ================= ACTIONS =================
                    if gesture_id == "PAUSE":
                        player.pause()
                        print("⏸ Pause")

                    elif gesture_id == "PLAY":
                        player.play()
                        print("▶️ Play")

                    elif gesture_id == "SEEK_BACK":
                        t = player.get_time()
                        if t != -1:
                            player.set_time(max(t - 10000, 0))
                        print("⬅️ Seek Back")

                    elif gesture_id == "SEEK_FORWARD":
                        t = player.get_time()
                        l = player.get_length()
                        if t != -1 and l > 0:
                            player.set_time(min(t + 10000, l - 1000))
                        print("➡️ Seek Forward")

                    elif gesture_id == "VOL_UP":
                        vol = player.audio_get_volume()
                        if vol == -1: vol = 50
                        player.audio_set_volume(min(vol + 10, 100))
                        print("🔊 Volume Up: ", player.audio_get_volume())

                    elif gesture_id == "VOL_DOWN":
                        vol = player.audio_get_volume()
                        if vol == -1: vol = 50
                        player.audio_set_volume(max(vol - 10, 0))
                        print("🔉 Volume Down: ", player.audio_get_volume())

                    elif gesture_id == "MUTE":
                        player.audio_toggle_mute()
                        print("🔇 Toggle Mute")

                    elif gesture_id == "RESTART":
                        player.set_time(0)
                        player.play()
                        print("🔁 Restart")

                    elif gesture_id == "NEXT_VIDEO":
                        print("⏭ Next Video")
                        load_video(current_index + 1)

                    elif gesture_id == "PREV_VIDEO":
                        print("⏮ Previous Video")
                        load_video(current_index - 1)

                    elif gesture_id == "EXIT":
                        print("🛑 Exit")
                        player.stop()
                        cap.release()
                        cv2.destroyAllWindows()
                        exit()

                    gesture_start_time = None
                    last_gesture = None
            else:
                last_gesture = None
                gesture_start_time = None

            # ===== SHOW ONLY FINGER COUNT =====
            cv2.putText(frame, f"Fingers: {finger_count}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Gesture VLC Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
player.stop()

