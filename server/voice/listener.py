import speech_recognition as sr
import threading

def _listen_worker(callback):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("NOVA is listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            try:
                # Using Google Web Speech API for now (requires internet, but is free and doesn't need API keys)
                text = recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                callback(text)
            except sr.UnknownValueError:
                print("Could not understand audio.")
                callback("...[Indecipherable]...")
            except sr.RequestError as e:
                print(f"Speech recognition error: {e}")
                callback("...[Error connecting to speech service]...")
    except Exception as e:
        print(f"Microphone error: {e}")
        callback("...[Microphone Error]...")

def listen_and_transcribe(callback):
    """
    Listens to the microphone in a separate thread and passes the
    transcribed text to the callback function.
    """
    thread = threading.Thread(target=_listen_worker, args=(callback,))
    thread.daemon = True
    thread.start()
