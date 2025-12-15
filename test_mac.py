import cv2
import pyautogui

print("1. Testing Mouse Control...")
try:
    # This should jiggle your mouse slightly
    pyautogui.moveRel(50, 0)
    pyautogui.moveRel(-50, 0)
    print("   -> Mouse moved! Permission Granted.")
except Exception as e:
    print("   -> ERROR: Mouse blocked. Check System Settings > Accessibility.")

print("2. Testing M4 Camera...")
cap = cv2.VideoCapture(0) # Try 1 if 0 fails
if cap.isOpened():
    print("   -> Camera Found! Press 'q' to close the window.")
    while True:
        success, frame = cap.read()
        if success:
            cv2.imshow("M4 Camera Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("   -> ERROR: Could not open camera. Check Privacy & Security > Camera.")