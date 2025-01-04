import speech_recognition as sr
import queue
from utils.text_to_speech import output_text
import whisper
import tempfile
import os
import torch
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

action_queue = queue.Queue()

print(torch.__version__)
print(torch.cuda.is_available())


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
        recognizer.energy_threshold = 300  # Adjust this value as needed

        while True:
            try:
                audio = recognizer.listen(
                    source, phrase_time_limit=30
                )  # Continuously listen for audio
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".wav"
                ) as temp_audio_file:
                    temp_audio_file.write(audio.get_wav_data())
                    temp_audio_file_path = temp_audio_file.name

                # Transcribe audio using Whisper
                result = model.transcribe(temp_audio_file_path)
                voice_data = result["text"]
                os.remove(temp_audio_file_path)  # Clean up temporary file

                if voice_data:
                    print(f"Detected audio: {voice_data}")
                    # Perform sentiment analysis
                    sentiment = sia.polarity_scores(voice_data)
                    print(f"Sentiment analysis: {sentiment}")
                    action_queue.put((voice_data, sentiment))
            except sr.UnknownValueError:
                print("Sorry, I did not get that")
            except sr.RequestError:
                output_text("Sorry, my speech service is down")
            except Exception as e:
                print(f"Unexpected error: {e}")
