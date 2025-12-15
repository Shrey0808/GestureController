# ui.py
import cv2
import numpy as np  # Required for the fallback black image
import config

def create_widget_view(img, mode, box_coords, hand_center):
    """
    Creates the visual overlay widget showing the hand and current mode.
    Handles out-of-bounds cropping safely.
    """
    x, y, w, h = box_coords
    
    # Get actual image dimensions
    img_h, img_w = img.shape[:2]

    # 1. Clamp Crop Coordinates to Actual Image Size
    # We ensure x1/y1 are within bounds and y2/x2 don't exceed image limits
    y1 = max(0, min(y, img_h))
    y2 = max(0, min(y + h, img_h))
    x1 = max(0, min(x, img_w))
    x2 = max(0, min(x + w, img_w))
    
    # 2. Check if the crop is valid (width and height > 0)
    if (x2 - x1) > 0 and (y2 - y1) > 0:
        widget = img[y1:y2, x1:x2].copy()
    else:
        # Fallback: Create a black placeholder if ROI is completely out of frame
        widget = np.zeros((h, w, 3), dtype=np.uint8)
        cv2.putText(widget, "ROI ERROR", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Resize widget if the crop was partial (e.g. edge of screen) 
    # to maintain the expected UI window size
    if widget.shape[0] != h or widget.shape[1] != w:
        widget = cv2.resize(widget, (w, h))

    # 3. Calculate local hand center relative to the widget
    local_hand_center = None
    if hand_center:
        hx, hy = hand_center
        # Only draw if the hand is actually inside the crop area
        if x1 <= hx <= x2 and y1 <= hy <= y2:
            local_hx = hx - x1  # Relative to the new crop
            local_hy = hy - y1
            local_hand_center = (local_hx, local_hy)

    # 4. Get Color based on Mode
    c = config.COLORS.get(mode, (255, 255, 255))
    
    # 5. Draw Elements
    cv2.rectangle(widget, (0, 0), (w-1, h-1), c, 4)
    cv2.putText(widget, mode, (10, h - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, c, 2)

    # Draw Tracking Dot
    if mode != "PAUSE" and local_hand_center:
        lx, ly = local_hand_center
        cv2.circle(widget, (int(lx), int(ly)), 6, c, -1)
        
    return widget