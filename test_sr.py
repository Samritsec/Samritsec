import speech_recognition as sr
import pyaudio

def test():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            # Use short timeout just to verify microphone connection
            audio = recognizer.listen(source, timeout=1, phrase_time_limit=2)
            print("Done listening")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test()
