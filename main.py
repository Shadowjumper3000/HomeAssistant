import threading
import queue
import datetime
import asyncio
import aiohttp
from audio_recording.recording import record_audio, action_queue
from tts.tts import output_text
from llm.llm_interaction import query_llm
from dotenv import load_dotenv
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

load_dotenv()

stop_event = threading.Event()
debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")


async def respond():
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            try:
                voice_data, sentiment = action_queue.get(timeout=1)
                if debug:
                    voice_data = "Test message"
                if "current time" in voice_data:
                    time = datetime.datetime.now().strftime("%I:%M %p")
                    output_text(time)
                elif "current date" in voice_data:
                    date = datetime.datetime.now().strftime("%B %d, %Y")
                    output_text(date)
                elif "exit" in voice_data:
                    output_text("Goodbye!")
                    stop_event.set()
                elif "stop" in voice_data:
                    pass
                else:
                    response = await query_llm(
                        session, voice_data, sentiment
                    )  # Query local LLM
                    output_text(response)
                action_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")


def continuously_record_microphone():
    record_audio()


recording_thread = threading.Thread(target=continuously_record_microphone)
responding_thread = threading.Thread(target=lambda: asyncio.run(respond()))

recording_thread.start()
responding_thread.start()

try:
    recording_thread.join()
    responding_thread.join()
except KeyboardInterrupt:
    print("Interrupted! Stopping threads...")
    stop_event.set()
    recording_thread.join()
    responding_thread.join()
    print("Threads stopped. Exiting program.")
