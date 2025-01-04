import speech_recognition as sr
import queue
from utils.text_to_speech import output_text, stop_audio

action_queue = queue.Queue()


def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(
            source, duration=1
        )  # Adjust for ambient noise
        while True:
            try:
                audio = recognizer.listen(source)  # Continuously listen for audio
                voice_data = recognizer.recognize_google(audio)
                if voice_data:
                    print(f"Detected audio: {voice_data}")
                    stop_audio()  # Stop any ongoing audio playback
                    action_queue.put(voice_data)
                    return voice_data
            except sr.UnknownValueError:
                output_text("Sorry, I did not get that")
            except sr.RequestError:
                output_text("Sorry, my speech service is down")
            except Exception as e:
                print(f"Unexpected error: {e}")
