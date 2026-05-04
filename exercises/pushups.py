import cv2
import mediapipe as mp
from utils.angles import calculate_angle, get_coords
from voice.feedback import speak

mp_pose = mp.solutions.pose


class PushupCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.cooldown = 0
        self.min_angle = 180  # tracks minimum elbow angle per rep

    def process(self, landmarks):
        # Get body landmark coordinates
        shoulder = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)
        elbow = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ELBOW)
        wrist = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_WRIST)
        hip = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        knee = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        ankle = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)

        # Calculate joint angles
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        body_angle = calculate_angle(shoulder, hip, knee)

        # Check if body is in horizontal push-up position
        shoulder_y = shoulder[1]
        ankle_y = ankle[1]
        is_horizontal = abs(shoulder_y - ankle_y) < 0.3

        self.cooldown -= 1

        if is_horizontal:

            # Track minimum elbow angle while going down
            if self.stage == "going_down":
                self.min_angle = min(self.min_angle, elbow_angle)

            # Start of downward movement
            if elbow_angle < 155 and self.stage == "up":
                self.stage = "going_down"
                self.min_angle = elbow_angle

            # Reached the bottom of the push-up
            if elbow_angle < 90 and self.stage == "going_down":
                self.stage = "down"
                self.counter += 1
                self.feedback = "Great rep!"
                speak("Great rep!")

            # Returned to the top — check rep depth
            if elbow_angle > 155 and self.stage in ["down", "going_down"]:
                if self.min_angle > 95:
                    # Did not go low enough
                    self.feedback = "Go lower next time!"
                    speak("Go lower next time!")
                    self.cooldown = 60
                self.stage = "up"
                self.min_angle = 180  # reset for next rep

            # Initial state — set stage when arms are extended
            if self.stage is None and elbow_angle > 155:
                self.stage = "up"
                self.min_angle = 180

            # Form feedback
            if self.cooldown <= 0:
                if body_angle < 140:
                    self.feedback = "Keep your back straight!"
                    speak("Keep your back straight!")
                    self.cooldown = 60

                elif body_angle > 210:
                    self.feedback = "Lower your hips!"
                    speak("Lower your hips!")
                    self.cooldown = 60

                elif self.counter > 0 and self.counter % 5 == 0:
                    self.feedback = f"{self.counter} reps!"
                    speak(f"Great job! {self.counter} reps!")
                    self.cooldown = 90

        else:
            # Not in push-up position — reset state
            self.stage = None
            self.min_angle = 180
            self.feedback = "Get in pushup position!"
            if self.cooldown <= 0:
                speak("Get in pushup position!")
                self.cooldown = 60

        return elbow_angle, body_angle

    def draw_ui(self, image):
        h, w = image.shape[:2]

        # Semi-transparent panel on the left
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0), (220, 180),
                      (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)

        # Exercise title
        cv2.putText(image, 'PUSH-UPS',
                    (15, 35),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.8, (0, 200, 255), 2)

        # Divider line
        cv2.line(image, (15, 45), (205, 45),
                 (0, 200, 255), 1)

        # Large rep counter
        cv2.putText(image, str(self.counter),
                    (60, 130),
                    cv2.FONT_HERSHEY_DUPLEX,
                    3.5, (255, 255, 255), 4)

        # Stage indicator with color
        stage_color = (0, 255, 0) if self.stage == "up" else (0, 165, 255)
        cv2.putText(image, f'Stage: {self.stage}',
                    (15, 165),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, stage_color, 2)

        # Feedback panel at the bottom
        if self.feedback:
            overlay2 = image.copy()
            cv2.rectangle(overlay2,
                          (0, h - 70), (w, h),
                          (20, 20, 20), -1)
            cv2.addWeighted(overlay2, 0.7, image, 0.3, 0, image)

            # Colored top border for feedback panel
            cv2.line(image, (0, h - 70), (w, h - 70),
                     (0, 200, 255), 2)

            # Feedback text
            cv2.putText(image, self.feedback,
                        (20, h - 25),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.9, (0, 255, 255), 2)

        # App name — top right corner
        cv2.rectangle(image, (w - 160, 0), (w, 50),
                      (20, 20, 20), -1)
        cv2.putText(image, 'AI FitCoach',
                    (w - 155, 32),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.6, (0, 200, 255), 1)

        return image