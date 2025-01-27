import os
import threading
import asyncio
from dotenv import load_dotenv
import elevenlabs
import pyttsx3
import logging

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv("ELEVENLABS_APIKEY")
FFMPEG_PATH = os.getenv("FFMPEG_PATH")
TTS_ENGINE = (
    os.getenv("TTS_ENGINE", "pyttsx3").strip().replace('"', "").lower()
)  # Ensure lowercase and strip whitespace
tts_input_dir = os.getenv("TTS_INPUT_DIR", ".tts_text")
output_audio_dir = os.getenv("OUTPUT_AUDIO_DIR", ".audio_data/output")
os.makedirs(tts_input_dir, exist_ok=True)
os.makedirs(output_audio_dir, exist_ok=True)

os.environ["PATH"] += os.pathsep + FFMPEG_PATH

logging.basicConfig(level=logging.DEBUG)

# Log the value of TTS_ENGINE
logging.debug(f"TTS_ENGINE environment variable: '{TTS_ENGINE}'")


def output_text(text, output_path):
    logging.debug(f"Outputting text to audio. Text: {text}, Output Path: {output_path}")
    if TTS_ENGINE == "elevenlabs":
        try:
            audio = elevenlabs.generate(
                text, voice="21m00Tcm4TlvDq8ikWAM", api_key=ELEVEN_LABS_API_KEY
            )
            # Suppress FFmpeg output by redirecting stderr to null
            with open(os.devnull, "w") as devnull:
                elevenlabs.save(audio, output_path, stderr=devnull)
            logging.debug(f"Audio saved to {output_path} using elevenlabs")
        except Exception as e:
            logging.error(
                f"Error in output_text with elevenlabs. Text: {text}, Output Path: {output_path}, Error: {e}"
            )
    elif TTS_ENGINE == "pyttsx3":
        try:
            engine = pyttsx3.init()
            logging.debug("Initialized pyttsx3 engine")
            engine.save_to_file(text, output_path)
            logging.debug("Saving text to audio file using pyttsx3")
            engine.runAndWait()
            logging.debug(f"Audio saved to {output_path} using pyttsx3")
        except Exception as e:
            logging.error(
                f"Error in output_text with pyttsx3. Text: {text}, Output Path: {output_path}, Error: {e}"
            )
    else:
        logging.error(f"Unsupported TTS engine: '{TTS_ENGINE}'")


async def process_tts():
    while True:
        for tts_file in os.listdir(tts_input_dir):
            if tts_file.endswith(".txt"):
                tts_path = os.path.join(tts_input_dir, tts_file)
                if os.path.isfile(tts_path):
                    try:
                        logging.debug(f"Processing TTS file: {tts_path}")
                        # Lock the file by renaming it
                        locked_tts_path = tts_path + ".lock"
                        os.rename(tts_path, locked_tts_path)
                        logging.debug(f"Locked TTS file: {locked_tts_path}")

                        # Read the text from the file
                        with open(locked_tts_path, "r") as file:
                            text = file.read()
                        logging.debug(f"Read text from locked TTS file: {text}")

                        # Convert text to audio and save it
                        output_audio_path = os.path.join(
                            output_audio_dir, tts_file.replace(".txt", ".wav")
                        )
                        output_text(text, output_audio_path)

                        # Delete the processed text file
                        os.remove(locked_tts_path)
                        logging.debug(f"Deleted locked TTS file: {locked_tts_path}")
                    except Exception as e:
                        logging.error(
                            f"Error processing TTS file {tts_path}. Error: {e}"
                        )
        await asyncio.sleep(1)  # Add a small delay to avoid busy-waiting


def start_tts_thread():
    logging.debug("Starting TTS thread")
    try:
        # Test pyttsx3 initialization
        if TTS_ENGINE == "pyttsx3":
            engine = pyttsx3.init()
            logging.debug("pyttsx3 engine initialized successfully in start_tts_thread")
            engine.stop()
            logging.debug("pyttsx3 engine stopped successfully in start_tts_thread")
    except Exception as e:
        logging.error(f"Error initializing pyttsx3 engine in start_tts_thread: {e}")

    tts_thread = threading.Thread(target=lambda: asyncio.run(process_tts()))
    tts_thread.start()
    return tts_thread
