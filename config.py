# config.py

# ===================== CAMERA SETTINGS =====================
WIDTH_CAM = 640
HEIGHT_CAM = 480

# ===================== TRACKING AREA (ROI) =================
ROI_X = 340
ROI_Y = 240
ROI_W = 280
ROI_H = 200
MARGIN = 15

# ===================== MOTION PHYSICS ======================
MOTION_THRESHOLD = 8.0      # Minimum movement to register cursor change
SCROLL_SENSITIVITY = 5      # Lower = Faster scrolling
SCROLL_DEADZONE = 15        # Buffer before scrolling starts

# ===================== GESTURE THRESHOLDS ==================
CLICK_DIST = 20             # Index + Thumb pinch distance
SCROLL_TOUCH_DIST = 20      # Middle + Ring pinch distance

# ===================== SMOOTHING FILTER ====================
MIN_CUTOFF = 0.05
BETA = 1.5

# ===================== UI COLORS ===========================
# Colors in BGR format (Blue, Green, Red)
COLORS = {
    "MOVE": (0, 255, 0),      # Green
    "DRAG": (0, 255, 255),    # Yellow
    "SCROLL": (255, 0, 255),  # Magenta
    "PAUSE": (0, 0, 255),     # Red
    "L-CLICK": (255, 255, 0), # Cyan 
    "R-CLICK": (0, 165, 255)  # Orange
}