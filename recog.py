import threading
import queue
import datetime
import asyncio
import aiohttp
from utils.audio import record_audio, action_queue
from utils.text_to_speech import output_text
from utils.llm import query_llm
from utils.web_search import perform_web_search

stop_event = threading.Event()
debug = False  # Set this to True to enable debug mode


async def respond():
    async with aiohttp.ClientSession() as session:
        while not stop_event.is_set():
            try:
                voice_data = action_queue.get(timeout=1)
                if debug:
                    voice_data = "Test message"
                print(f"Detected audio: {voice_data}")
                if "current time" in voice_data:
                    time = datetime.datetime.now().strftime("%I:%M %p")
                    output_text(time)
                elif "current date" in voice_data:
                    date = datetime.datetime.now().strftime("%B %d, %Y")
                    output_text(date)
                elif "search" in voice_data:
                    output_text("What do you want to search for?")
                    search = record_audio()
                    output_text("Searching for " + search)
                    search_result = await perform_web_search(
                        session, search
                    )  # Perform web search
                    output_text(search_result)
                elif "exit" in voice_data:
                    output_text("Goodbye!")
                    stop_event.set()
                else:
                    response = await query_llm(session, voice_data)  # Query local LLM
                    output_text(response)
                action_queue.task_done()
            except queue.Empty:
                continue


def continuously_record_microphone():
    while not stop_event.is_set():
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
