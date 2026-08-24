# Hand-Controlled PC

Control your computer mouse using hand gestures captured through a webcam.

The project uses **MediaPipe Hand Landmarker** to detect hand landmarks in real time, **OpenCV** to capture and display the webcam feed, and **ydotool / pydotool** to control the mouse on Linux systems running **Wayland**.

## Current Features

* **Move the mouse** using the index fingertip.
* **Left click** by pinching the thumb and index finger.
* **Drag and drop** by holding the thumb-index pinch.
* **Right click** by pinching the thumb and middle finger.
* Configurable active camera area.
* Mouse movement smoothing.
* Dead zone to reduce unwanted cursor jitter.
* Real-time hand landmark visualization.

## How It Works

The webcam captures frames using OpenCV.

MediaPipe processes each frame and returns **21 hand landmarks**:

```text
Webcam
   ↓
OpenCV frame
   ↓
BGR → RGB
   ↓
MediaPipe Hand Landmarker
   ↓
21 hand landmarks
   ↓
Gesture detection
   ↓
pydotool / ydotool
   ↓
Mouse control
```

Some important MediaPipe landmarks used by the project are:

```text
4   → Thumb fingertip
8   → Index fingertip
12  → Middle fingertip
16  → Ring fingertip
20  → Pinky fingertip
```

## Gestures

### Move Cursor

The cursor follows the position of the index fingertip.

The project maps only a configurable area of the camera image to the entire screen. This allows the user to control the whole screen while moving the hand over a relatively small area.

Example:

```python
X_MIN = 0.55
X_MAX = 0.95

Y_MIN = 0.55
Y_MAX = 0.95
```

This means that roughly the lower-right area of the camera is used as the active control region.

That region is normalized to the entire monitor:

```text
Camera active area
┌──────────┐
│          │
│   HAND   │
│   AREA   │
└──────────┘
      ↓
Entire screen
┌──────────────────────────────┐
│                              │
│                              │
│                              │
└──────────────────────────────┘
```

## Left Click

A left click is detected by measuring the distance between:

```text
Thumb fingertip → landmark 4
Index fingertip → landmark 8
```

The Euclidean distance between the two points is calculated:

```python
distance = math.hypot(
    hand[4].x - hand[8].x,
    hand[4].y - hand[8].y
)
```

If the distance becomes smaller than a threshold, a pinch is detected.

```python
PINCH_DISTANCE = 0.05
```

## Drag and Drop

The same thumb-index pinch is also used for drag and drop.

A short pinch produces a normal left click.

A pinch held for longer than:

```python
DRAG_TIME = 0.35
```

starts a drag operation.

```text
Thumb + Index pinch
        ↓
   wait 0.35 s
        ↓
    Mouse Down
        ↓
   Move the hand
        ↓
     Drag item
        ↓
 Separate fingers
        ↓
     Mouse Up
        ↓
       Drop
```

A different release threshold is used to avoid repeated clicks caused by small landmark fluctuations:

```python
PINCH_DISTANCE = 0.05
RELEASE_DISTANCE = 0.07
```

## Right Click

A right click uses a different pinch:

```text
Thumb fingertip  → landmark 4
Middle fingertip → landmark 12
```

When both fingers touch and are released, a right click is triggered.

## Cursor Smoothing

Hand landmarks naturally move slightly between frames, even when the hand appears stationary.

Without filtering, this causes the cursor to shake.

A simple smoothing algorithm is used:

```python
x_screen = prev_x + (target_x - prev_x) / SMOOTHING
y_screen = prev_y + (target_y - prev_y) / SMOOTHING
```

Example:

```python
SMOOTHING = 5
```

Higher values produce smoother but slower movement.

## Dead Zone

Very small movements can also be ignored:

```python
DEAD_ZONE = 1
```

If the detected movement is smaller than this threshold, the cursor position is not updated.

## Technologies

* Python 3
* OpenCV
* MediaPipe
* pydotool
* ydotool
* Linux / Ubuntu
* Wayland

## Requirements

A webcam is required.

The project was developed on **Ubuntu with Wayland**.

### Python Environment

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install Python dependencies:

```bash
pip install opencv-python mediapipe python-ydotool
```

## MediaPipe Model

The project requires the MediaPipe Hand Landmarker model:

```text
hand_landmarker.task
```

Place it in the project directory:

```text
Hand-controlled-PC/
│
├── main.py
├── handgestures.py
├── hand_landmarker.task
├── README.md
└── venv/
```

## Wayland Mouse Control

`PyAutoGUI` relies heavily on X11 and does not work correctly for this project under Wayland.

For this reason, the project uses **ydotool**, which sends input events through Linux `uinput`.

`ydotoold` must be running before starting the program.

Example:

```bash
sudo ydotoold
```

It can also be configured as a systemd service so that it starts automatically when the computer boots.

The Python application communicates with it using:

```python
import pydotool

pydotool.init()
```

## Running the Project

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run:

```bash
python3 main.py
```

Press:

```text
q
```

to close the application.

## Project Structure

```text
Hand-controlled-PC/
│
├── main.py
│   ├── Webcam capture
│   ├── MediaPipe detection
│   └── Landmark visualization
│
├── handgestures.py
│   ├── Gesture detection
│   ├── Cursor movement
│   ├── Left click
│   ├── Right click
│   └── Drag and drop
│
├── hand_landmarker.task
│
└── README.md
```

## Possible Future Improvements

Possible features to add next:

* Scroll using two fingers.
* Volume control using hand gestures.
* Play / pause media.
* Mute gesture.
* Switch between windows.
* Screenshot gesture.
* Enable / disable gesture control.
* Configurable sensitivity and smoothing.
* Gesture recognition using joint angles instead of only landmark coordinates.
* Machine-learning-based gesture classification.
* Configuration file for custom gesture mappings.
* On-screen indication of the currently detected gesture.

## Goal

The goal of this project is to explore **computer vision, human-computer interaction and real-time gesture recognition** by building a practical touchless interface using only a standard webcam.
