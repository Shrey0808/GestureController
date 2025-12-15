
-----

# GestureController 👆🖱️

**GestureController** is a computer vision-based application that turns your hand into a high-precision virtual mouse. Using a standard webcam, it tracks hand landmarks to control cursor movement, clicks, and scrolling in real-time.

It utilizes **MediaPipe** for robust hand detection and implements the **1€ Filter** (One Euro Filter) to smooth out jitter, ensuring a fluid and usable experience compared to raw tracking data.

  

-----

## 🌟 Key Features

  * **Smooth Tracking:** Uses the *1€ Filter* algorithm to eliminate cursor jitter while maintaining low latency.
  * **Gesture Recognition:** Supports Left Click, Right Click, Drag-and-Drop, and Scrolling.
  * **ROI-Based Control:** Uses a specific Region of Interest (ROI) on the camera feed to map hand movements to the full screen, reducing arm fatigue.
  * **Visual Feedback UI:** A floating widget shows the camera feed, current mode, and tracking status, overlaying other windows.
  * **Customizable:** All sensitivity, colors, and gesture thresholds are easily adjustable in `config.py`.

-----

## 🛠️ Installation

### Prerequisites

Ensure you have **Python 3.8+** installed.

### 1\. Clone the Repository

```bash
git clone https://github.com/Shrey0808/GestureController

cd GestureController
```

### 2\. Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

*(Note: On Linux, you may need to install `python3-tk` and `python3-dev` for PyAutoGUI)*

-----

## 🚀 Usage

1.  Run the main script:
    ```bash
    python main.py
    ```
2.  A window named **"Touch Controller"** will appear on the right side of your screen.
3.  Place your hand inside the colored box (ROI) shown in the window.
4.  Perform gestures to control the mouse.

### 🛑 To Exit

Press **`q`** on your keyboard while the "Touch Controller" window is active to quit the application.

-----

## 🖐️ Gesture Guide

| Action | Gesture | Visual Indicator |
| :--- | :--- | :--- |
| **Move Cursor** | Move your hand with **fingers open**. The cursor tracks your **Index Knuckle**. | 🟢 Green Border |
| **Left Click** | Pinch **Thumb** and **Index Finger** together. | 🔵 Cyan Border |
| **Drag & Drop** | Pinch **Thumb** + **Index** and **move** your hand. | 🟡 Yellow Border |
| **Right Click** | Pinch **Thumb** and **Middle Finger** together. | 🟠 Orange Border |
| **Scroll** | Pinch **Middle** + **Ring Finger** and move hand **Up/Down**. | 🟣 Magenta Border |
| **Pause (Clutch)** | Close your hand into a **Fist**. Tracking stops. | 🔴 Red Border |

-----

## ⚙️ Configuration

You can tweak the sensitivity and behavior by editing `config.py`:

  * **Camera Settings:** Change `WIDTH_CAM` and `HEIGHT_CAM` if your webcam resolution differs.
  * **Tracking Area:** Adjust `ROI_X`, `ROI_Y`, `ROI_W`, `ROI_H` to change the size and position of the active tracking box.
  * **Motion Physics:**
      * `MOTION_THRESHOLD`: Increase if the cursor jitters too much when stationary.
      * `SCROLL_SENSITIVITY`: Lower value = Faster scrolling.
  * **Smoothing:**
      * `MIN_CUTOFF`: Decrease to reduce jitter (but increase lag).
      * `BETA`: Increase to reduce lag (but increase jitter).


-----

## 🔧 Troubleshooting

  * **Jittery Cursor:** Increase `MIN_CUTOFF` in `config.py` or ensure your room is well-lit.
  * **Gestures Not Triggering:** Adjust the `CLICK_DIST` or `SCROLL_TOUCH_DIST` thresholds in `config.py`. Every hand size is different\!
  * **Hand Not Detected:** Ensure the background is not too cluttered and your hand is clearly visible to the camera.
  * **Window Not on Top:** Some operating systems prevent the `cv2.WND_PROP_TOPMOST` flag from working. You may need to manually click the window to keep it visible.

-----

## 🔮 Future Improvements

  * [ ] Add "Double Click" gesture logic.
  * [ ] Auto-calibration of gesture thresholds based on hand size.
  * [ ] Support for left-handed mode (currently optimized for right hand).

-----

## 📜 License

This project is licensed under the MIT License.

**Credits:**

  * Computer Vision via [OpenCV](https://opencv.org/). 
  * Hand Tracking powered by [MediaPipe](https://developers.google.com/mediapipe).
  * Mouse Control via [PyAutoGUI](https://pyautogui.readthedocs.io/).
  * 1€ Filter Algorithm by [Casiez et al](http://cristal.univ-lille.fr/~casiez/1euro/).