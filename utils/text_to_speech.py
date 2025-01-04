import os
from dotenv import load_dotenv
import elevenlabs
import pyttsx3

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVENLABS_APIKEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")

os.environ["PATH"] += os.pathsep + FFMPEG_PATH

# ! CURRENTLY USED, comment for testing to preserve API costs !
# def output_text(text):
#     try:
#         audio = elevenlabs.generate(text, voice="21m00Tcm4TlvDq8ikWAM", api_key=ELEVEN_LABS_API_KEY)
#         elevenlabs.play(audio, use_ffmpeg=False)
#     except Exception as e:
#         print(f"Error in output_text: {e}")


# ! DEPRECATED, keep in for future testing !
def output_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in output_text: {e}")
