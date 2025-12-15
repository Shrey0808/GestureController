import cv2
import mediapipe as mp

# ==============================================================================
#                           HAND DETECTOR MODULE
# ==============================================================================

class HandDetector:
    """
    A wrapper class for MediaPipe Hands to simplify hand detection and landmark extraction.
    
    Attributes:
        mode (bool): Static image mode (False for video stream).
        max_hands (int): Maximum number of hands to detect.
        detection_con (float): Minimum confidence value (0-1) for detection to be considered successful.
        track_con (float): Minimum confidence value (0-1) for tracking to continue.
    """
    
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5):
        """
        Initializes the MediaPipe Hands solution.
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con
        
        # Initialize MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Landmark IDs for finger tips (Thumb, Index, Middle, Ring, Pinky)
        # Reference: 
        self.tip_ids = [4, 8, 12, 16, 20]
        self.lm_list = []
        self.results = None

        print("[MODULE] HandDetector Initialized.")

    def find_hands(self, img, draw=True):
        """
        Processes the image to detect hands and optionally draws landmarks.
        
        Args:
            img: The input image (BGR format from OpenCV).
            draw (bool): Whether to draw the hand skeleton on the image.
            
        Returns:
            img: The image with landmarks drawn (if draw=True).
        """
        # MediaPipe requires RGB images
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw connections (skeleton) between landmarks
                    self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
        
        return img

    def find_position(self, img, draw=True):
        """
        Extracts the list of landmark coordinates.
        
        Args:
            img: The input image (needed for scaling normalized coordinates).
            draw (bool): Whether to draw circles on the detected landmarks.
            
        Returns:
            list: A list of [id, x, y] for all 21 hand landmarks. 
                  Returns empty list if no hand is detected.
        """
        self.lm_list = []
        
        # Ensure results exist and landmarks were found
        if self.results and self.results.multi_hand_landmarks:
            # We only process the first detected hand for this controller
            my_hand = self.results.multi_hand_landmarks[0]
            
            h, w, c = img.shape
            
            for id, lm in enumerate(my_hand.landmark):
                # Convert normalized (0-1) coordinates to pixel coordinates
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lm_list.append([id, cx, cy])
                
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        
        return self.lm_list

    def fingers_up(self):
        """
        Determines which fingers are currently extended (up).
        
        Returns:
            list: A list of 5 integers (0 or 1) representing the state of each finger.
                  [Thumb, Index, Middle, Ring, Pinky]
                  1 = Open/Up, 0 = Closed/Down
        """
        fingers = []
        
        # Safety check: Ensure landmarks exist before accessing them
        if len(self.lm_list) == 0:
            return fingers

        # --- 1. Thumb Logic ---
        # The thumb is "up" (open) if the tip (ID 4) is to the RIGHT of the IP joint (ID 3).
        # Note: This logic assumes the hand is facing the camera (palm forward) or right hand.
        # For a more robust solution, handedness (Left/Right) should be checked, 
        # but for a simple controller, x-axis comparison suffices.
        if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # --- 2. Four Fingers Logic (Index, Middle, Ring, Pinky) ---
        # A finger is "up" if the tip (ID 8, 12, 16, 20) is HIGHER (lower Y value) 
        # than the PIP joint (ID 6, 10, 14, 18).
        # Note: In OpenCV, Y coordinates increase downwards (0 is top).
        for id in range(1, 5):
            # tip_ids[id] is the Tip. tip_ids[id]-2 is the PIP joint (Knuckle-ish area).
            if self.lm_list[self.tip_ids[id]][2] < self.lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers