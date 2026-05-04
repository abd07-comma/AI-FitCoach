import cv2
import mediapipe as mp
from exercises.pushups import PushupCounter
from exercises.squats import SquatCounter
from exercises.pullups import PullupCounter

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# IP camera URL — replace with your own address
CAMERA_URL = "rtsp://192.168.137.39:8080/h264.sdp"

# Choose exercise: "pushup", "squat", "pullup"
EXERCISE = "pushup"


def main():
    from voice.feedback import preload_audio
    preload_audio()

    # Initialize rep counter based on selected exercise
    exercise = EXERCISE
    if EXERCISE == "pushup":
        counter = PushupCounter()
    elif EXERCISE == "squat":
        counter = SquatCounter()
    else:
        counter = PullupCounter()

    # Connect to camera
    cap = cv2.VideoCapture(CAMERA_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FPS, 15)

    # Fall back to webcam if IP camera is unavailable
    if not cap.isOpened():
        print("IP camera unavailable, switching to webcam...")
        cap = cv2.VideoCapture(0)

    print(f"Exercise: {EXERCISE.upper()}")
    print("Press Q to quit")
    print("Press R to reset counter")
    print("Press 1 - push-ups, 2 - squats, 3 - pull-ups")

    with mp_pose.Pose(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
    ) as pose:

        while cap.isOpened():
            # Flush buffer to get the latest frame
            cap.grab()
            cap.grab()
            ret, frame = cap.read()

            if not ret:
                print("No video signal...")
                break

            # Convert BGR to RGB for MediaPipe
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Run pose estimation
            results = pose.process(image)

            # Convert back to BGR for OpenCV
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Process body landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                counter.process(landmarks)

            except Exception as e:
                # Show message if no person detected
                cv2.putText(image, "No person detected",
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

            # Draw pose skeleton
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style()
            )

            # Render UI overlay
            image = counter.draw_ui(image)

            # Show current exercise name
            cv2.putText(image,
                        f"Exercise: {EXERCISE.upper()}",
                        (image.shape[1] - 300, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (255, 255, 0), 2)

            # Display the frame
            cv2.imshow('AI FitCoach', image)

            # Handle keyboard input
            key = cv2.waitKey(10) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('r'):
                counter.counter = 0
                counter.stage = None
                print("Counter reset!")
            elif key == ord('1'):
                counter = PushupCounter()
                exercise = "pushup"
            elif key == ord('2'):
                counter = SquatCounter()
                exercise = "squat"
            elif key == ord('3'):
                counter = PullupCounter()
                exercise = "pullup"

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()