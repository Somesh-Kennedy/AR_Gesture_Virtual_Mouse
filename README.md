# AR Gesture Virtual Mouse

This project implements a virtual mouse that can be controlled using **hand gestures** captured by a webcam. It uses computer vision techniques from the **Mediapipe** library for hand tracking and **OpenCV (`cv2`)** for video processing, allowing users to move the cursor, click, scroll, and take screenshots through specific hand movements.

---

## Features

* **Cursor Movement:** Control the mouse cursor by moving your **index finger**.
* **Clicking:** Perform a **left-click** by bringing the **index and middle fingers together** (when the distance is less than 20).
* **Scrolling Up:** Scroll up by raising the **thumb and index finger** (and keeping the middle finger down)
* **Scrolling Down:** Scroll down by raising the **thumb only**.
* **Screenshot:** Take a **screenshot** by raising the **middle, ring, and pinky fingers** and checking if the distance between the thumb (point 4) and index finger (point 8) is less than 20

---

## Installation and Setup

### Prerequisites

You need **Python 3.x** installed on your system.

### Dependencies

Install the required Python packages using `pip`. The project relies on:
* `opencv-python` (used as `cv2`) for video capture and image processing.
* `mediapipe` for hand detection and tracking.
* `autopy` for controlling the mouse cursor and clicks.
* `numpy` for coordinate interpolation.
* `pyautogui` for scrolling and taking screenshots.
* `time` for calculating FPS.

```bash
pip install opencv-python mediapipe autopy numpy pyautogui
