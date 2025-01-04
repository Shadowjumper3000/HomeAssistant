import speech_recognition as sr
import queue
from utils.text_to_speech import output_text

action_queue = queue.Queue()


def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            voice_data = recognizer.recognize_google(audio)
            if voice_data:
                print(f"Detected audio: {voice_data}")
                action_queue.put(voice_data)
        except sr.UnknownValueError:
            output_text("Sorry, I did not get that")
        except sr.RequestError:
            output_text("Sorry, my speech service is down")
