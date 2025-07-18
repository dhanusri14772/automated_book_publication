from agents import voice

if __name__ == "__main__":
    print("🎙️ Testing voice module...")

    voice.speak("Hello! Please say yes or no.")
    result = voice.listen_for_yes_no()
    print(f"🧠 Detected response: {result}")
