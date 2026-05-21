# Smart Wellness Monitor 🖥️👀

A real-time computer vision project that helps improve **health and productivity while using a computer** by monitoring:

- 👀 **Eye Distance / Drowsiness Detection**
-  **Posture Detection**
-  **Real-Time Alerts**

This project uses **Python, OpenCV, and MediaPipe** to analyze facial landmarks and body posture through a webcam and notify the user when unhealthy habits are detected.

---

## Features 

### 👀 Eye Distance / Drowsiness Detection
- Detects **eye closure using Eye Aspect Ratio (EAR)**.
- Identifies prolonged eye closure that may indicate **drowsiness or fatigue**.
- Gives an **alert/sound notification** when eyes remain closed beyond a threshold.

### 🧍 Posture Detection
- Tracks body posture using **MediaPipe Pose Estimation**.
- Detects:
  - Slouching
  - Neck bending
  - Poor sitting posture
- Provides feedback when posture becomes unhealthy.

### ⚡ Real-Time Monitoring
- Live webcam feed.
- Instant posture and drowsiness tracking.
- Lightweight and beginner-friendly implementation.

---

## Tech Stack 🛠️

- **Python**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **Pygame** *(for alert sound, if used)*

---

## Project Structure 📂

```bash
project-folder/
│── posture.py              # Posture detection
│── eye_detection.py        # Eye distance / drowsiness detection
│── alert_sound.mp3         # Alert sound file
│── requirements.txt        # Dependencies
│── README.md               # Project documentation
```

---

## Installation 🚀

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

### 2. Navigate into the project folder

```bash
cd your-repository-name
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install opencv-python mediapipe numpy pygame
```

---

## Usage ▶️

### Run Eye Distance / Drowsiness Detection

```bash
python eye_detection.py
```

### Run Posture Detection

```bash
python posture.py
```

Make sure your webcam is enabled.

---

## How It Works 🧠

### Eye Detection
The system calculates the **Eye Aspect Ratio (EAR)** using facial landmarks.  
If the eye remains closed below a threshold for a certain duration, an alert is triggered.

### Posture Detection
The system tracks body landmarks such as:
- Shoulders
- Neck
- Head alignment

Bad posture is detected based on body angles and alignment.

---

## Future Improvements 🚀
- Add a **dashboard for analytics**
- Track screen time
- Smart break reminders
- AI-based posture correction suggestions
- Save posture and drowsiness history

---

## Screenshots 📸


---

## Author 👩‍💻

Built with curiosity, code, and a lot of debugging ☕
by **Suravi**
