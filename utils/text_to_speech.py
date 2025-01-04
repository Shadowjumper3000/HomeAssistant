import pyttsx3


def output_text(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        with open("data/output.txt", "w") as f:
            f.write(text + "\n")
    except Exception as e:
        print(f"Error in output_text: {e}")
