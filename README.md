# 🎮 Gesture Controlled VLC Media Player (Jetson Compatible)

A Computer Vision–based system that allows users to control **VLC Media Player** using real-time hand gestures via webcam.

This project integrates:

* **OpenCV** – Video capture & display
* **MediaPipe** – Hand landmark detection
* **Python-VLC** – Media playback control
* **Jetson Linux Environment Support**

---

# 📌 Features

* ✋ Real-time hand gesture recognition
* 🎬 Play / Pause control
* ⏩ Seek forward / backward
* 🔊 Volume up / down
* 🔇 Mute toggle
* 🔁 Restart video
* ⏭ Next / Previous video
* 🛑 Exit control
* 🧠 Gesture hold detection (prevents accidental triggers)

---

# 🛠️ System Requirements

## Hardware

* NVIDIA Jetson device (Nano / Xavier / Orin)
* USB Webcam
* HDMI display
* Internet connection (for setup)

## Software

* Ubuntu (Jetson Linux)
* Python 3.8+
* VLC Media Player

---

# 📦 Complete Setup Guide (For New Jetson Device)

The following steps must be performed on a fresh Jetson system.

---

## Step 1 — Update System

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2 — Install System Dependencies

Install required multimedia and GUI libraries:

```bash
sudo apt install -y \
python3-pip \
python3-dev \
libgtk-3-dev \
libavcodec-dev \
libavformat-dev \
libswscale-dev \
v4l-utils \
cmake \
gstreamer1.0-tools \
gstreamer1.0-plugins-base \
gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad \
gstreamer1.0-plugins-ugly
```

---

## Step 3 — Install VLC Media Player

```bash
sudo apt install vlc -y
```

Verify installation:

```bash
vlc --version
```

---

## Step 4 — Install Python Dependencies

It is recommended to create a virtual environment:

```bash
python3 -m venv gesture_env
source gesture_env/bin/activate
```

Upgrade pip:

```bash
pip install --upgrade pip
```

Install required Python libraries:

```bash
pip install opencv-python mediapipe python-vlc
```

---

## Step 5 — Camera Permission Setup (Important for Jetson)

Add your user to the video group:

```bash
sudo usermod -aG video $USER
```

Then reboot:

```bash
sudo reboot
```

After reboot, verify camera:

```bash
ls /dev/video*
```

---

# 📂 Project Structure

```
gesture-vlc-control/
│
├── sample.mp4
├── sample2.mp4
├── sample3.mp4
├── main.py
└── README.md
```

---

# ▶️ How to Run the Project

Activate environment:

```bash
source gesture_env/bin/activate
```

Run:

```bash
python main.py
```

Ensure:

* Webcam is connected
* Videos exist in the project directory
* Display is properly configured

---

# ✋ Gesture Controls

| Gesture Pattern         | Action              |
| ----------------------- | ------------------- |
| ✊ (0 fingers)           | Pause               |
| 🖐 (5 fingers)          | Play                |
| Thumb only              | Seek Backward (10s) |
| Pinky only              | Seek Forward (10s)  |
| Index only              | Volume Up           |
| Index + Middle + Pinky  | Volume Down         |
| Index + Middle          | Restart             |
| Four fingers (no thumb) | Mute                |
| Thumb + Index + Middle  | Next Video          |
| Thumb + Index           | Previous Video      |
| Index + Pinky           | Exit                |

> Hold each gesture for **0.8 seconds** to trigger the action.

---

# ⚙️ How the System Works

1. Webcam captures live frames using OpenCV
2. MediaPipe detects 21 hand landmarks
3. Finger states are calculated
4. Gesture is classified
5. Corresponding VLC command is executed

---

# 🎞️ Playlist Configuration

Videos are loaded from the current directory:

```python
playlist = {
    0: "sample.mp4",
    1: "sample2.mp4",
    2: "sample3.mp4"
}
```

You may modify this dictionary to add additional videos.

---

# 🧠 Gesture Stability Mechanism

To avoid false triggers:

* A gesture must be held for **0.8 seconds**
* Action executes only after stable detection

This ensures smooth and reliable control.

---

# 🛑 Exit Options

* Show **Index + Pinky** gesture
  OR
* Press **Q** key

---

# 🐞 Troubleshooting (Jetson Specific)

### Camera Not Opening

* Verify `/dev/video0` exists
* Try changing index:

  ```python
  cap = cv2.VideoCapture(1)
  ```

### VLC Not Playing

* Confirm VLC is installed
* Reinstall python-vlc:

  ```bash
  pip uninstall python-vlc
  pip install python-vlc
  ```

### libva / GPU Warnings

These are common on Jetson and usually harmless.
They do not affect functionality.

---

# 📌 Future Enhancements

* Graphical User Interface
* Auto playlist folder scanning
* Adjustable gesture sensitivity
* Multi-hand support
* Fullscreen gesture mode

---

# 📜 License

This project is intended for academic and research purposes.

---

# 👨‍💻 Author

Developed as a Computer Vision and Embedded AI project using OpenCV, MediaPipe, and VLC on NVIDIA Jetson platform.

---

⭐ If you find this project useful, please consider starring the repository.
