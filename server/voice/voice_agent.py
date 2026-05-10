import pyttsx3
import threading

def _speak_text(text: str):
    try:
        engine = pyttsx3.init()

        # Adjust properties for a "little deep but comforting" voice
        voices = engine.getProperty('voices')

        # Try to find a male voice (often deeper).
        # Fallback to the first voice if no specific male voice is found.
        chosen_voice = voices[0].id
        for voice in voices:
            if "male" in voice.name.lower() or "david" in voice.name.lower() or "zira" not in voice.name.lower():
                chosen_voice = voice.id
                break

        engine.setProperty('voice', chosen_voice)

        # Lower pitch slightly if possible (pyttsx3 doesn't have direct pitch control on all platforms,
        # but lowering rate sometimes gives a smoother, deeper feel).
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 20)  # Slightly slower for comforting feel

        # Lower volume slightly for comforting feel
        engine.setProperty('volume', 0.9)

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")

def speak(text: str):
    """
    Speaks the given text in a separate thread so it doesn't block the async event loop.
    """
    thread = threading.Thread(target=_speak_text, args=(text,))
    thread.daemon = True
    thread.start()
