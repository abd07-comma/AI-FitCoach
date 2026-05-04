import cv2
import mediapipe as mp
from utils.angles import calculate_angle, get_coords
from voice.feedback import speak

mp_pose = mp.solutions.pose


class PullupCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.cooldown = 0

    def process(self, landmarks):
        # Get body landmark coordinates
        shoulder = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        elbow = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
        wrist = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)

        # Calculate elbow angle
        elbow_angle = calculate_angle(shoulder, elbow, wrist)

        self.cooldown -= 1

        # Rep counting logic
        if elbow_angle > 150:
            self.stage = "down"  # arms fully extended at bottom

        if elbow_angle < 60 and self.stage == "down":
            self.stage = "up"  # chin over bar
            self.counter += 1
            self.feedback = "Great pull-up!"
            speak("Great pull-up!")

        # Form feedback
        if self.cooldown <= 0:
            # Not pulling high enough
            if self.stage == "up" and elbow_angle > 70:
                self.feedback = "Pull higher!"
                speak("Pull higher!")
                self.cooldown = 45

            # Not fully extending at the bottom
            elif self.stage == "down" and elbow_angle < 150:
                self.feedback = "Full extension!"
                speak("Full extension at the bottom!")
                self.cooldown = 45

        return elbow_angle

    def draw_ui(self, image):
        h, w = image.shape[:2]

        # Background panel
        cv2.rectangle(image, (0, 0), (250, 120),
                      (0, 0, 0), -1)

        # Exercise title
        cv2.putText(image, 'PULL-UPS',
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0, 255, 0), 2)

        # Rep counter
        cv2.putText(image, str(self.counter),
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2.5, (255, 255, 255), 3)

        # Stage indicator
        cv2.putText(image, f'Stage: {self.stage}',
                    (10, 115),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (200, 200, 200), 1)

        # Feedback panel at the bottom
        if self.feedback:
            cv2.rectangle(image,
                          (0, h - 60), (w, h),
                          (0, 0, 0), -1)
            cv2.putText(image, self.feedback,
                        (10, h - 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 255, 255), 2)

        return image