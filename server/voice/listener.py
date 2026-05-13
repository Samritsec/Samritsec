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
                # Using local Whisper model for offline speech recognition
                print("Processing audio with local Whisper model...")
                text = recognizer.recognize_whisper(audio, model="base")
                print(f"Recognized: {text}")
                callback(text)
            except sr.UnknownValueError:
                print("Could not understand audio.")
                callback("...[Indecipherable]...")
            except sr.RequestError as e:
                print(f"Speech recognition request error: {e}")
                callback("...[Error connecting to speech service]...")
            except Exception as e:
                print(f"Speech recognition error: {e}")
                callback(f"...[Speech Recognition Error: {str(e)[:50]}]...")
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
