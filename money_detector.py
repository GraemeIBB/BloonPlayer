import cv2
import numpy as np
from PIL import ImageGrab
from imutils.object_detection import non_max_suppression

class MoneyDetector:
    def __init__(self, region=(365, 0, 570, 100), threshold=0.8, overlap_thresh=0.3):
        self.region = region
        self.threshold = threshold
        self.overlap_thresh = overlap_thresh
        self.templates = {str(i): cv2.cvtColor(cv2.imread(f"templates/{i}.png"), cv2.COLOR_BGR2GRAY) for i in range(10)}

    def capture_screen(self):
        screenshot = ImageGrab.grab(bbox=self.region)
        screenshot = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        return screenshot_gray

    def get_money(self):
        screenshot_gray = self.capture_screen()
        detected_digits = []

        for digit, template in self.templates.items():
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= self.threshold)

            rects = []
            for pt in zip(*locations[::-1]):
                rects.append((pt[0], pt[1], pt[0] + template.shape[1], pt[1] + template.shape[0]))

            pick = non_max_suppression(np.array(rects), probs=None, overlapThresh=self.overlap_thresh)

            for (x1, y1, x2, y2) in pick:
                detected_digits.append((x1, digit))

        detected_digits.sort()
        money_str = "".join(digit for _, digit in detected_digits)
        return money_str

if __name__ == "__main__":
    detector = MoneyDetector()
    money = detector.get_money()
    print(f"Detected Money: {money}")