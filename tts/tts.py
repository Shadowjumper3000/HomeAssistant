import os
from dotenv import load_dotenv
import elevenlabs
import pyttsx3

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVENLABS_APIKEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")

os.environ["PATH"] += os.pathsep + FFMPEG_PATH


def output_text(text):
    if TTS_ENGINE == "elevenlabs":
        try:
            audio = elevenlabs.generate(
                text, voice="21m00Tcm4TlvDq8ikWAM", api_key=ELEVEN_LABS_API_KEY
            )
            elevenlabs.play(audio, use_ffmpeg=False)
        except Exception as e:
            print(f"Error in output_text: {e}")
    elif TTS_ENGINE == "pyttsx3":
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in output_text: {e}")
    else:
        print(f"Unsupported TTS engine: {TTS_ENGINE}")
