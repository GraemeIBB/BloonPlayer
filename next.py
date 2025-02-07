import cv2
import numpy as np
from PIL import ImageGrab
from imutils.object_detection import non_max_suppression

# Define region for the money display (adjust for your screen)
MONEY_REGION = (365, 0, 570, 100)  # (x1, y1, x2, y2)

# Load number templates (0-9) and convert to grayscale
templates = {str(i): cv2.cvtColor(cv2.imread(f"templates/{i}.png"), cv2.COLOR_BGR2GRAY) for i in range(10)}

def get_money():
    # Capture the game screen
    screenshot = ImageGrab.grab(bbox=MONEY_REGION)
    screenshot = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    detected_digits = []

    for digit, template in templates.items():
        # Perform template matching
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust as needed
        locations = np.where(result >= threshold)

        rects = []
        for pt in zip(*locations[::-1]):  # Get coordinates
            rects.append((pt[0], pt[1], pt[0] + template.shape[1], pt[1] + template.shape[0]))

        # Apply non-maximum suppression to filter out overlapping detections
        pick = non_max_suppression(np.array(rects), probs=None, overlapThresh=0.3)

        for (x1, y1, x2, y2) in pick:
            detected_digits.append((x1, digit))  # Store (x_position, digit)

    # Sort digits from left to right
    detected_digits.sort()

    # Extract just the numbers
    money_str = "".join(digit for _, digit in detected_digits)
    
    return money_str

# Run and print the detected money
money = get_money()
print(f"Detected Money: {money}")
