# main.py
import cv2
import pyautogui
import time
import math
import numpy as np

# Custom Modules
import config
from hand_detector import HandDetector
from filters import OneEuroFilter
from ui import create_widget_view

# Disable FailSafe
pyautogui.FAILSAFE = False

def main():
    # --- SETUP ---
    print("[SYSTEM] Initializing...")
    cap = cv2.VideoCapture(0)
    cap.set(3, config.WIDTH_CAM)
    cap.set(4, config.HEIGHT_CAM)
    
    detector = HandDetector(max_hands=1)
    
    # Filters
    fx = OneEuroFilter()
    fy = OneEuroFilter()
    
    # Screen size
    screen_w, screen_h = pyautogui.size()
    
    # State Variables
    prev_scr_x, prev_scr_y = 0, 0
    mode = "MOVE"
    last_mode = ""
    click_state = {"left": False, "right": False}
    scroll_origin_y = 0 
    
    # Timer for Drag Logic
    click_start_time = 0
    
    # Window
    window_name = "Touch Controller"
    
    # 1. Create the window
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    
    # 2. POSITION: Move window to the Right-Middle of screen
    cv2.moveWindow(window_name, screen_w - config.ROI_W - 20, (screen_h // 2) - (config.ROI_H // 2))
    
    # 3. STAY ON TOP: This command forces the window to overlay others
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

    print("[SYSTEM] Ready.")

    try:
        while True:
            success, img = cap.read()
            if not success: continue
            
            img = cv2.flip(img, 1)
            now = time.time()
            
            img = detector.find_hands(img, draw=False) 
            lm = detector.find_position(img, draw=False) 
            
            hand_center = None

            if lm:
                thumb, index = lm[4], lm[8]
                middle, ring = lm[12], lm[16]
                
                # Tracking point: Knuckle (Index Base)
                raw_x, raw_y = lm[5][1], lm[5][2]
                hand_center = (raw_x, raw_y)

                # --- CLUTCH (PAUSE) ---
                fingers_up = detector.fingers_up()
                if fingers_up[1:] == [0, 0, 0, 0]: mode = "PAUSE"
                elif mode == "PAUSE" and fingers_up[1] == 1: mode = "MOVE"

                if mode != "PAUSE":
                    # --- MAPPING & FILTERING ---
                    sx = fx.filter(raw_x, now)
                    sy = fy.filter(raw_y, now)

                    x_min, x_max = config.ROI_X + config.MARGIN, config.ROI_X + config.ROI_W - config.MARGIN
                    y_min, y_max = config.ROI_Y + config.MARGIN, config.ROI_Y + config.ROI_H - config.MARGIN

                    target_x = np.interp(sx, (x_min, x_max), (0, screen_w))
                    target_y = np.interp(sy, (y_min, y_max), (0, screen_h))
                    target_x = np.clip(target_x, 0, screen_w)
                    target_y = np.clip(target_y, 0, screen_h)

                    # --- GESTURE LOGIC ---
                    dist_idx_thumb = math.hypot(thumb[1]-index[1], thumb[2]-index[2])
                    dist_mid_thumb = math.hypot(thumb[1]-middle[1], thumb[2]-middle[2])
                    dist_mid_ring = math.hypot(middle[1]-ring[1], middle[2]-ring[2])
                    move_dist = math.hypot(target_x - prev_scr_x, target_y - prev_scr_y)

                    # 1. SCROLL
                    if dist_mid_ring < config.SCROLL_TOUCH_DIST:
                        current_tips_y = (middle[2] + ring[2]) / 2
                        if mode != "SCROLL":
                            scroll_origin_y = current_tips_y
                            mode = "SCROLL"
                        else:
                            offset = current_tips_y - scroll_origin_y
                            if abs(offset) > config.SCROLL_DEADZONE:
                                speed = int(-offset / config.SCROLL_SENSITIVITY)
                                pyautogui.scroll(speed)
                    
                    # 2. LEFT CLICK / DRAG (UPDATED LOGIC)
                    elif dist_idx_thumb < config.CLICK_DIST:
                        if not click_state["left"]:
                            # --- CLICK START ---
                            click_state["left"] = True
                            click_start_time = time.time()  # Start timer
                            pyautogui.mouseDown()
                            mode = "L-CLICK"
                        else:
                            # --- HOLDING ---
                            # Only switch to DRAG if > 1 second has passed
                            if time.time() - click_start_time > 1.0:
                                mode = "DRAG"
                            else:
                                mode = "L-CLICK"
                    
                    # 3. RIGHT CLICK
                    elif dist_mid_thumb < config.CLICK_DIST:
                         if not click_state["right"]:
                            mode = "R-CLICK"
                            pyautogui.rightClick()
                            click_state["right"] = True
                            time.sleep(0.2)
                    
                    # 4. RELEASE
                    else:
                        if mode in ["SCROLL", "L-CLICK", "R-CLICK", "DRAG"]: mode = "MOVE"
                        
                        # Release Left Click
                        if click_state["left"] and dist_idx_thumb > config.CLICK_DIST + 10:
                            pyautogui.mouseUp()
                            click_state["left"] = False
                            
                        # Release Right Click lock
                        if click_state["right"] and dist_mid_thumb > config.CLICK_DIST + 10:
                            click_state["right"] = False

                    # --- MOVE MOUSE ---
                    # IMPORTANT: Removed "L-CLICK" from list so cursor freezes while clicking (waiting for drag)
                    if mode in ["MOVE", "DRAG"]:
                        thresh = config.MOTION_THRESHOLD if mode == "MOVE" else 2.0
                        if move_dist > thresh:
                            pyautogui.moveTo(target_x, target_y)
                            prev_scr_x, prev_scr_y = target_x, target_y

            # --- RENDER UI ---
            if mode != last_mode:
                print(f"[STATE] {mode}")
                last_mode = mode

            widget_img = create_widget_view(img, mode, 
                                          (config.ROI_X, config.ROI_Y, config.ROI_W, config.ROI_H), 
                                          hand_center)
            cv2.imshow(window_name, widget_img)
            
            # Re-assert window on top every frame (optional)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)

            if cv2.waitKey(1) & 0xFF == ord('q'): break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()