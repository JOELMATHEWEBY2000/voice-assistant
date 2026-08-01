import speech_recognition as sr
import pyttsx3

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Voice settings
engine.setProperty("rate", 170)      # Speed
engine.setProperty("volume", 1.0)    # Volume

# Select voice (0 = Male, 1 = Female if available)
voices = engine.getProperty("voices")

if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)


def speak(text):
    """
    Convert text to speech.
    """
    print(f"Assistant: {text}")

    engine.say(text)
    engine.runAndWait()


def listen():
    """
    Listen through microphone and convert speech to text.
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=8
        )

    try:

        command = recognizer.recognize_google(audio)

        print(f"You: {command}")

        return command.lower()

    except sr.UnknownValueError:

        speak("Sorry, I didn't understand.")

        return ""

    except sr.RequestError:

        speak("Speech service is unavailable.")

        return ""

    except Exception as e:

        print(e)

        speak("Something went wrong.")

        return ""


def test_voice():

    speak("Hello. Voice Assistant is working properly.")


if __name__ == "__main__":

    test_voice()

    while True:

        command = listen()

        if command == "exit":
            speak("Goodbye")
            break

        speak(f"You said {command}")