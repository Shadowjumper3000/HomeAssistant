import os
from dotenv import load_dotenv
import elevenlabs

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVENLABS_APIKEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

os.environ["PATH"] += os.pathsep + FFMPEG_PATH


def output_text(text):
    try:
        audio = elevenlabs.generate(text, voice="Alice", api_key=ELEVEN_LABS_API_KEY)
        elevenlabs.play(audio, use_ffmpeg=False)
    except Exception as e:
        print(f"Error in output_text: {e}")
