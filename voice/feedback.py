import threading
import os
from gtts import gTTS
import playsound

is_speaking = False

# All phrases used across exercises — preloaded at startup
PHRASES = [
    "Great rep!", "Go lower!", "Keep your back straight!",
    "Lower your hips!", "Lock your arms at the top!",
    "Get in pushup position!", "Great job!",
    "Perfect squat!", "Squat deeper! Go lower!",
    "Keep your chest up! Lean back!",
    "Lean forward slightly!",
    "Keep your knees behind your toes!",
    "Widen your stance for better balance!",
    "Stand up fully! Lock your knees!",
    "Great pull-up!", "Pull higher!",
    "Full extension at the bottom!",
    "5 reps! Keep going!", "10 reps! Keep going!",
    "Amazing! 5 squats done!", "Amazing! 10 squats done!"
]


def preload_audio():
    """Generate and cache all audio files at startup to avoid delays during exercise."""
    os.makedirs("audio_cache", exist_ok=True)
    print("Loading voice feedback...")
    for phrase in PHRASES:
        filename = f"audio_cache/{phrase[:30].replace(' ', '_').replace('!', '')}.mp3"
        if not os.path.exists(filename):
            try:
                tts = gTTS(text=phrase, lang='en', slow=False)
                tts.save(filename)
            except Exception as e:
                print(f"Could not preload: {phrase} — {e}")
    print("Voice feedback ready!")


def get_audio_file(text):
    """Return path to cached audio file, generating it on-the-fly if not found."""
    filename = f"audio_cache/{text[:30].replace(' ', '_').replace('!', '')}.mp3"
    if os.path.exists(filename):
        return filename
    # Generate on demand if not in cache
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(filename)
        return filename
    except:
        return None


def speak(text):
    """Play voice feedback in a separate thread to avoid blocking the video loop."""
    global is_speaking

    if is_speaking:
        return

    def run():
        global is_speaking
        is_speaking = True
        try:
            audio_file = get_audio_file(text)
            if audio_file:
                playsound.playsound(audio_file)
        except Exception as e:
            print(f"Voice error: {e}")
        is_speaking = False

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()