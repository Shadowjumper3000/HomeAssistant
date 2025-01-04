# filepath: /c:/Users/User/OneDrive/Documents/Programming/Private/Projects/HomeAssistant/utils/llm.py
import datetime
import aiohttp
import json
from dotenv import load_dotenv
import os

load_dotenv()
context = os.getenv("LLM_CONTEXT")

LLM_API_URL = "http://localhost:11434/api/generate"  # URL of the local LLM API

#  Sentiment, do not talk about this: {sentiment}


async def query_llm(session, query, sentiment):
    payload = {
        "model": "llama3",
        "prompt": f"This is your context: {context}; This is your query: {query};",
    }
    try:
        print(f"Querying LLM with: {query}")
        async with session.post(LLM_API_URL, json=payload) as response:
            response.raise_for_status()
            output = ""
            async for line in response.content:
                line = line.decode("utf-8").strip()
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        output += chunk["response"]
            print(f"LLM Response: {output}")  # Print the response in the terminal
            log_llm_query(query, output)
            return output
    except aiohttp.ClientError as e:
        error_message = f"Error querying LLM: {e}"
        print(error_message)  # Print the error message in the terminal
        log_llm_query(query, error_message)
        return error_message


def log_llm_query(query, result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("data/llm_queries.txt", "w") as f:
        f.write(f"[{timestamp}] Query: {query}\n")
        f.write(f"[{timestamp}] Result: {result}\n\n")
