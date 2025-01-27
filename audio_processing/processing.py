import os
import asyncio
import aiohttp
import whisper
import threading
from dotenv import load_dotenv

load_dotenv()

input_audio_dir = os.getenv("INPUT_AUDIO_DIR", ".audio_data/input")
llm_queries_dir = os.getenv("LLM_QUERIES_DIR", ".llm_queries")
os.makedirs(input_audio_dir, exist_ok=True)
os.makedirs(llm_queries_dir, exist_ok=True)


async def process_audio_file(session, audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    voice_data = result["text"]
    return voice_data


async def process_audio():
    async with aiohttp.ClientSession() as session:
        while True:
            for audio_file in os.listdir(input_audio_dir):
                if audio_file.endswith(".wav"):
                    audio_path = os.path.join(input_audio_dir, audio_file)
                    if os.path.isfile(audio_path):
                        try:
                            # Lock the file by renaming it
                            locked_audio_path = audio_path + ".lock"
                            os.rename(audio_path, locked_audio_path)

                            # Process the audio file
                            voice_data = await process_audio_file(
                                session, locked_audio_path
                            )

                            # Save the transcribed text to .llm_queries
                            llm_query_path = os.path.join(
                                llm_queries_dir, audio_file.replace(".wav", ".txt")
                            )
                            with open(llm_query_path, "w") as llm_query_file:
                                llm_query_file.write(voice_data)

                            # Delete the processed audio file
                            os.remove(locked_audio_path)
                        except Exception as e:
                            print(f"Error processing audio file {audio_path}: {e}")
            await asyncio.sleep(1)  # Add a small delay to avoid busy-waiting


def start_processing_thread():
    processing_thread = threading.Thread(target=lambda: asyncio.run(process_audio()))
    processing_thread.start()
    return processing_thread
