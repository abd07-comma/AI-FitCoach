import cv2
import mediapipe as mp
from utils.angles import calculate_angle, get_coords
from voice.feedback import speak

mp_pose = mp.solutions.pose


class SquatCounter:
    def __init__(self):
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.cooldown = 0

    def process(self, landmarks):
        # Get body landmark coordinates
        hip = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_HIP)
        knee = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_KNEE)
        ankle = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
        shoulder = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_SHOULDER)

        # Calculate joint angles
        knee_angle = calculate_angle(hip, knee, ankle)
        back_angle = calculate_angle(shoulder, hip, knee)

        # Check if knee is tracking over the toe
        knee_x = knee[0]
        ankle_x = ankle[0]
        toe_over = knee_x - ankle_x  # positive = knee past ankle

        # Measure stance width between both feet
        left_ankle = get_coords(landmarks, mp_pose.PoseLandmark.LEFT_ANKLE)
        right_ankle = get_coords(landmarks, mp_pose.PoseLandmark.RIGHT_ANKLE)
        stance_width = abs(left_ankle[0] - right_ankle[0])

        self.cooldown -= 1

        # Rep counting logic
        if knee_angle > 160:
            self.stage = "up"

        if knee_angle < 90 and self.stage == "up":
            self.stage = "down"
            self.counter += 1
            self.feedback = "Perfect squat!"
            speak("Perfect squat!")

        # Form feedback
        if self.cooldown <= 0:

            # Not squatting deep enough
            if self.stage == "down" and knee_angle > 110:
                self.feedback = "Squat deeper!"
                speak("Squat deeper! Go lower!")
                self.cooldown = 45

            # Leaning too far forward
            elif back_angle < 130:
                self.feedback = "Keep your chest up!"
                speak("Keep your chest up! Lean back!")
                self.cooldown = 45

            # Too upright — needs slight forward lean
            elif back_angle > 175:
                self.feedback = "Lean forward slightly!"
                speak("Lean forward slightly!")
                self.cooldown = 45

            # Knee is tracking past the toe
            elif toe_over > 0.15:
                self.feedback = "Knees behind toes!"
                speak("Keep your knees behind your toes!")
                self.cooldown = 45

            # Stance too narrow
            elif stance_width < 0.1:
                self.feedback = "Wider stance!"
                speak("Widen your stance for better balance!")
                self.cooldown = 45

            # Not fully standing up at the top
            elif self.stage == "up" and knee_angle < 160:
                self.feedback = "Stand up fully!"
                speak("Stand up fully! Lock your knees!")
                self.cooldown = 45

            # Milestone every 5 reps
            elif self.counter > 0 and self.counter % 5 == 0:
                self.feedback = f"{self.counter} squats! Great!"
                speak(f"Amazing! {self.counter} squats done!")
                self.cooldown = 90

        return knee_angle, back_angle

    def draw_ui(self, image):
        h, w = image.shape[:2]

        # Semi-transparent panel on the left
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0), (220, 180),
                      (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)

        # Exercise title
        cv2.putText(image, 'SQUATS',
                    (15, 35),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.8, (0, 255, 100), 2)

        # Divider line
        cv2.line(image, (15, 45), (205, 45),
                 (0, 255, 100), 1)

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
            cv2.line(image, (0, h - 70), (w, h - 70),
                     (0, 255, 100), 2)
            cv2.putText(image, self.feedback,
                        (20, h - 25),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.9, (0, 255, 100), 2)

        # App name — top right corner
        cv2.rectangle(image, (w - 160, 0), (w, 50),
                      (20, 20, 20), -1)
        cv2.putText(image, 'AI FitCoach',
                    (w - 155, 32),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.6, (0, 255, 100), 1)

        return image