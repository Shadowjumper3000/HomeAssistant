import speech_recognition as sr
import queue
from tts.tts import output_text
import whisper
import os
import torch
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import logging

load_dotenv()

nltk.download("vader_lexicon")

action_queue = queue.Queue()

print(torch.__version__)
print(torch.cuda.is_available())

input_audio_dir = os.getenv("INPUT_AUDIO_DIR", ".audio_data/input")
os.makedirs(input_audio_dir, exist_ok=True)

logging.basicConfig(level=logging.DEBUG)

KEYWORD = "Friday"


def record_audio():
    if whisper is None:
        print(
            "Whisper library is not available. Please install it using 'pip install openai-whisper'."
        )
        return

    model = whisper.load_model("base")
    recognizer = sr.Recognizer()
    sia = SentimentIntensityAnalyzer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(
            source, duration=1
        )  # Adjust for ambient noise

        # Set the energy threshold lower to increase sensitivity
        recognizer.energy_threshold = 700  # Adjust this value as needed

        while True:
            try:
                audio = recognizer.listen(
                    source, phrase_time_limit=30
                )  # Continuously listen for audio
                audio_file_path = os.path.join(input_audio_dir, "input.wav")
                with open(audio_file_path, "wb") as audio_file:
                    audio_file.write(audio.get_wav_data())

                # Transcribe audio using Whisper
                result = model.transcribe(audio_file_path)
                voice_data = result["text"]

                if voice_data:
                    print(f"Detected audio: {voice_data}")
                    # Check if the sentence starts with the keyword
                    if voice_data.lower().startswith(KEYWORD.lower()):
                        print(
                            f"Keyword '{KEYWORD}' detected at the beginning of the sentence."
                        )
                        # Perform sentiment analysis
                        sentiment = sia.polarity_scores(voice_data)
                        print(f"Sentiment analysis: {sentiment}")
                        action_queue.put((voice_data, sentiment))
                    else:
                        print(
                            f"Keyword '{KEYWORD}' not detected at the beginning of the sentence. Ignoring."
                        )
            except sr.UnknownValueError:
                print("Sorry, I did not get that")
            except sr.RequestError:
                output_text("Sorry, my speech service is down")
            except Exception as e:
                print(f"Unexpected error: {e}")
