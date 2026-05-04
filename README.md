# 🏋️ AI FitCoach

> Real-time AI-powered personal trainer that analyzes your exercise form and provides instant voice feedback using computer vision.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.13-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 Overview

AI FitCoach uses **MediaPipe Pose Estimation** and **OpenCV** to track your body movements in real-time through any camera. It counts your reps, analyzes your form, and gives you instant **voice feedback** — just like having a personal trainer watching you.

No gym equipment needed. No wearables. Just a camera and your body.

---

## ✨ Features

- 🔴 **Real-time pose estimation** — 33 body landmarks tracked at every frame
- 🔢 **Automatic rep counting** — counts only valid, complete repetitions
- 🎙️ **Voice feedback** — tells you exactly what to fix using Google TTS
- 📐 **Form analysis** — detects poor posture and gives correction cues
- 📷 **IP Camera support** — works with RTSP streams from smartphones
- 🔄 **Switch exercises on the fly** — press 1, 2, or 3 to change mode

---

## 🏃 Supported Exercises

| Exercise | Detection | Form Checks |
|----------|-----------|-------------|
| **Push-ups** | Elbow angle + body alignment | Depth, back straightness, hip position |
| **Squats** | Knee angle + back angle | Depth, chest position, knee alignment, stance width |
| **Pull-ups** | Elbow angle + shoulder position | Height reached, full extension |

---

## 🗣️ Voice Feedback Examples

**Push-ups:**
- *"Go lower!"* — not reaching full depth
- *"Keep your back straight!"* — sagging spine
- *"Lower your hips!"* — hips too high
- *"Lock your arms at the top!"* — incomplete extension
- *"Great rep!"* — perfect execution

**Squats:**
- *"Squat deeper!"* — not reaching parallel
- *"Keep your chest up!"* — excessive forward lean
- *"Keep your knees behind your toes!"* — knees caving forward
- *"Widen your stance!"* — feet too close together
- *"Stand up fully!"* — incomplete lockout

**Pull-ups:**
- *"Pull higher!"* — chin not clearing the bar
- *"Full extension at the bottom!"* — not fully extending arms

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **MediaPipe** | Pose estimation — 33 body landmarks |
| **OpenCV** | Video capture, frame processing, UI rendering |
| **gTTS** | Google Text-to-Speech for voice feedback |
| **NumPy** | Angle calculations between body joints |
| **pyttsx3** | Fallback TTS engine |

---

## 📁 Project Structure

```
AI-FitCoach/
│
├── main.py                  # Entry point — camera loop & UI
│
├── exercises/
│   ├── __init__.py
│   ├── pushups.py           # Push-up counter & form analysis
│   ├── squats.py            # Squat counter & form analysis
│   └── pullups.py           # Pull-up counter & form analysis
│
├── voice/
│   ├── __init__.py
│   └── feedback.py          # Google TTS voice feedback engine
│
├── utils/
│   ├── __init__.py
│   └── angles.py            # Joint angle calculation utilities
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10
- Webcam or smartphone with IP Webcam app

### Installation

```bash
# Clone the repository
git clone https://github.com/abd07-comma/AI-FitCoach.git
cd AI-FitCoach

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install mediapipe==0.10.13
pip install opencv-python
pip install numpy
pip install gtts
pip install playsound==1.2.2
pip install pyttsx3
```

> ⚠️ **Platform Notes:**
>
> **Windows** — use `playsound==1.2.2` (included above)
>
> **Linux / macOS** — replace `playsound` with `pygame` for audio playback:
> ```bash
> pip install pygame
> ```
> Then in `voice/feedback.py`, replace:
> ```python
> import playsound
> playsound.playsound(audio_file)
> ```
> With:
> ```python
> import pygame
> pygame.mixer.init()
> pygame.mixer.music.load(audio_file)
> pygame.mixer.music.play()
> while pygame.mixer.music.get_busy():
>     pygame.time.Clock().tick(10)
> ```

### Configuration

In `main.py`, set your camera source:

```python
# For webcam
CAMERA_URL = 0

# For smartphone IP camera (use IP Webcam app)
CAMERA_URL = "rtsp://192.168.x.x:8080/h264.sdp"

# Choose exercise: "pushup", "squat", "pullup"
EXERCISE = "pushup"
```

### Run

```bash
python main.py
```

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `1` | Switch to Push-ups |
| `2` | Switch to Squats |
| `3` | Switch to Pull-ups |
| `R` | Reset rep counter |
| `Q` | Quit |

---

## 📱 Using Smartphone as Camera

1. Install **IP Webcam** app (Android) on your phone
2. Start the server in the app
3. Copy the RTSP URL shown in the app
4. Paste it as `CAMERA_URL` in `main.py`

**Best camera angles:**
- Push-ups → side view (90°)
- Squats → side view (90°)
- Pull-ups → front or side view

---

## 🧠 How It Works

```
Camera Frame
     │
     ▼
MediaPipe Pose Estimation
     │
     ▼
33 Body Landmarks (x, y coordinates)
     │
     ▼
Joint Angle Calculation (NumPy)
     │
     ├──► Rep Counter Logic (stage machine: up/down)
     │
     ├──► Form Analysis (angle thresholds)
     │
     └──► Voice Feedback (Google TTS)
```

**Angle-based detection:**
- Elbow angle < 90° → bottom of push-up
- Elbow angle > 160° → top of push-up
- Knee angle < 90° → parallel squat depth
- Body alignment checked via shoulder-hip-knee angle

---

## 🔮 Future Plans

- [ ] Add more exercises (lunges, deadlifts, planks)
- [ ] Session summary with performance stats
- [ ] Web interface using Streamlit
- [ ] Mobile app deployment
- [ ] Docker containerization
- [ ] Workout history & progress tracking

---

## 👨‍💻 Author

**Abdolla Abutolybov**
Computer Vision Engineer

[![GitHub](https://img.shields.io/badge/GitHub-abd07--comma-black?logo=github)](https://github.com/abd07-comma)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-abdolla--abutolybov-blue?logo=linkedin)](https://linkedin.com/in/abdolla-abutolybov-79b84b352)

---

## 📄 License

MIT License — feel free to use and modify for your projects.
