import threading
import aiohttp
import asyncio
from flask import Flask, request, jsonify, send_file
from audio_recording.recording import record_audio
from audio_processing.processing import start_processing_thread, process_audio_file
from llm.llm_interaction import start_llm_thread
from tts.tts import start_tts_thread
from dotenv import load_dotenv
import os
import warnings
import logging
from functools import wraps

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

load_dotenv()

app = Flask(__name__)
stop_event = threading.Event()
debug = os.getenv("DEBUG", "False").lower() in ("true", "1")
server_mode = os.getenv("SERVER_STATUS", "False").lower() in ("true", "1")
input_audio_dir = os.getenv("INPUT_AUDIO_DIR", ".audio_data/input")
llm_queries_dir = os.getenv("LLM_QUERIES_DIR", ".llm_queries")
tts_input_dir = os.getenv("TTS_INPUT_DIR", ".tts_text")
output_audio_dir = os.getenv("OUTPUT_AUDIO_DIR", ".audio_data/output")
auth_token = os.getenv("AUTH_TOKEN")

# Ensure directories exist
os.makedirs(input_audio_dir, exist_ok=True)
os.makedirs(llm_queries_dir, exist_ok=True)
os.makedirs(tts_input_dir, exist_ok=True)
os.makedirs(output_audio_dir, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)


def check_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token != auth_token:
            logging.error("Unauthorized access attempt")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/process_audio", methods=["POST"])
@check_auth
def process_audio():
    if "audio" not in request.files:
        logging.error("No audio file provided in the request")
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_path = os.path.join(input_audio_dir, audio_file.filename)
    audio_file.save(audio_path)
    logging.info(f"Audio file saved to {audio_path}")

    async def process_audio_async():
        async with aiohttp.ClientSession() as session:
            try:
                voice_data = await process_audio_file(session, audio_path)
                llm_query_path = os.path.join(
                    llm_queries_dir,
                    os.path.basename(audio_path).replace(".wav", ".txt"),
                )
                with open(llm_query_path, "w") as llm_query_file:
                    llm_query_file.write(voice_data)
                logging.info(f"Transcribed text saved to {llm_query_path}")
                return jsonify({"response": voice_data}), 200
            except Exception as e:
                logging.error(f"Error processing audio file: {e}")
                return jsonify({"error": str(e)}), 500

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(process_audio_async())


@app.route("/get_audio/<filename>", methods=["GET"])
@check_auth
def get_audio(filename):
    audio_path = os.path.join(output_audio_dir, filename)
    if os.path.exists(audio_path):
        logging.info(f"Sending audio file: {audio_path}")
        return send_file(audio_path, as_attachment=True)
    else:
        logging.error(f"File not found: {audio_path}")
        return jsonify({"error": "File not found"}), 404


def continuously_record_microphone():
    record_audio()


if __name__ == "__main__":
    if not server_mode:
        recording_thread = threading.Thread(target=continuously_record_microphone)
        recording_thread.start()

    processing_thread = start_processing_thread()
    llm_thread = start_llm_thread()
    tts_thread = start_tts_thread()

    if server_mode:
        app.run(host="0.0.0.0", port=int(os.getenv("SERVER_PORT", 5000)))

    try:
        if not server_mode:
            recording_thread.join()
        processing_thread.join()
        llm_thread.join()
        tts_thread.join()
    except KeyboardInterrupt:
        logging.info("Interrupted! Stopping threads...")
        stop_event.set()
        if not server_mode:
            recording_thread.join()
        processing_thread.join()
        llm_thread.join()
        tts_thread.join()
        logging.info("Threads stopped. Exiting program.")
