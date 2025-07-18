import speech_recognition as sr
import pyttsx3

def speak(text):
    """Text-to-speech feedback"""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen_for_yes_no(max_retries=3):
    """Listens for a simple yes or no response."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    for attempt in range(max_retries):
        with mic as source:
            print(" Listening for voice input (say 'yes' or 'no')...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            response = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {response}")
            response = response.lower()
            if "yes" in response:
                return "y"
            elif "no" in response:
                return "n"
            else:
                print(" Couldn't detect a clear yes/no.")
        except sr.UnknownValueError:
            print(" Could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")

        print(" Let's try again...")

    print(" Max retries reached. Defaulting to 'n'.")
    return "n"


def listen_for_command(commands=["accept", "edit", "revise", "final"], max_retries=3):
    """Listens for specific commands (e.g., accept/edit)."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    for attempt in range(max_retries):
        with mic as source:
            print(f"🎤 Listening for command ({', '.join(commands)})...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            response = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {response}")
            response = response.lower().strip()

            for cmd in commands:
                if cmd in response:
                    return cmd

            print(" Couldn't detect a valid command.")
        except sr.UnknownValueError:
            print(" Could not understand audio.")
        except sr.RequestError as e:
            print(f" Could not request results: {e}")

        print(" Let's try again...")

    print(" Max retries reached. Defaulting to 'revise'.")
    return "revise"


def listen_free_form(prompt=" Speak now (free-form):", max_retries=2):
    """Captures free-form voice input and returns it as text."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    for attempt in range(max_retries):
        with mic as source:
            print(prompt)
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source)

        try:
            response = recognizer.recognize_google(audio)
            print(f" Recognized: {response}")
            return response
        except sr.UnknownValueError:
            print(" Sorry, I couldn't understand that.")
        except sr.RequestError as e:
            print(f" API error: {e}")

        print(" Trying again...")

    return "Sorry, voice input failed."

if __name__ == "__main__":
    speak("Say something you want me to repeat.")
    user_input = listen_free_form()
    speak(f"You said: {user_input}")
