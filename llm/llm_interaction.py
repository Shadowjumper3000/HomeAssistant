import json
import os
import aiohttp
import asyncio
import threading
import logging
from dotenv import load_dotenv

load_dotenv()

LLM_CONTEXT = os.getenv("LLM_CONTEXT")
LLM_FILE = os.getenv("LLM_FILE")
LLM_API_URL = os.getenv("LLM_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
llm_queries_dir = os.getenv("LLM_QUERIES_DIR", ".llm_queries")
tts_input_dir = os.getenv("TTS_INPUT_DIR", ".tts_text")
os.makedirs(llm_queries_dir, exist_ok=True)
os.makedirs(tts_input_dir, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)


async def query_llm(session, query, sentiment):
    payload = {
        "model": LLM_MODEL,
        "prompt": f"LLM Context: {LLM_CONTEXT}; User query: {query};",
    }
    try:
        logging.debug(f"Querying LLM with: {query}")
        async with session.post(LLM_API_URL, json=payload) as response:
            response.raise_for_status()
            output = ""
            async for line in response.content:
                line = line.decode("utf-8").strip()
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        output += chunk["response"]
            logging.debug(f"LLM Response: {output}")
            return output
    except aiohttp.ClientError as e:
        error_message = f"Error querying LLM: {e}"
        logging.error(error_message)
        return error_message


async def process_llm_queries():
    async with aiohttp.ClientSession() as session:
        while True:
            for llm_file in os.listdir(llm_queries_dir):
                if llm_file.endswith(".txt"):
                    llm_path = os.path.join(llm_queries_dir, llm_file)
                    if os.path.isfile(llm_path):
                        try:
                            logging.debug(f"Processing LLM query file: {llm_path}")
                            # Lock the file by renaming it
                            locked_llm_path = llm_path + ".lock"
                            os.rename(llm_path, locked_llm_path)
                            logging.debug(f"Locked LLM query file: {locked_llm_path}")

                            # Read the query from the file
                            with open(locked_llm_path, "r") as file:
                                query = file.read()

                            # Perform sentiment analysis if needed
                            sentiment = {}  # Add sentiment analysis if needed

                            # Query the LLM
                            response = await query_llm(session, query, sentiment)

                            logging.debug(
                                f"Attempting to write to file: {locked_llm_path}"
                            )
                            # Save the response to the locked file
                            with open(locked_llm_path, "w") as tts_text_file:
                                tts_text_file.write(response)

                            # Unlock the file by renaming it back
                            unlocked_llm_path = locked_llm_path.replace(".lock", "")
                            os.rename(locked_llm_path, unlocked_llm_path)
                            logging.debug(
                                f"Unlocked LLM query file: {unlocked_llm_path}"
                            )

                            # Move the file to the TTS directory
                            tts_text_path = os.path.join(tts_input_dir, llm_file)
                            os.rename(unlocked_llm_path, tts_text_path)
                            logging.debug(
                                f"Moved LLM response to TTS directory: {tts_text_path}"
                            )

                        except Exception as e:
                            logging.error(f"Error processing LLM query {llm_path}: {e}")
            await asyncio.sleep(1)  # Add a small delay to avoid busy-waiting


def start_llm_thread():
    llm_thread = threading.Thread(target=lambda: asyncio.run(process_llm_queries()))
    llm_thread.start()
    return llm_thread
