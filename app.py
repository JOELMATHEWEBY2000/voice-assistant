from flask import Flask, render_template, request, jsonify
from assistant import speak, listen
from weather import get_weather
from news import get_news
from reminder import (
    add_reminder,
    get_reminders,
    check_reminders
)
from config import validate_keys
import datetime
import webbrowser
import threading

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/voice", methods=["POST"])
def voice():

    command = listen()

    if not command:
        return jsonify({
            "command": "",
            "response": "Sorry, I couldn't understand."
        })

    response = process_command(command)

    return jsonify({
        "command": command,
        "response": response
    })


def process_command(command):

    command = command.lower()

    # Weather
    if "weather" in command:

        speak("Please tell me the city name.")

        city = listen()

        if not city:
            return "City not recognized."

        result = get_weather(city)

        speak(result)

        return result

    # News
    elif "news" in command:

        headlines = get_news()

        if len(headlines) == 0:
            return "Unable to fetch news."

        speak("Today's top headlines are")

        for news in headlines:
            speak(news)

        return "\n".join(headlines)

    # Time
    elif "time" in command:

        current = datetime.datetime.now().strftime("%I:%M %p")

        text = f"The current time is {current}"

        speak(text)

        return text

    # Date
    elif "date" in command:

        today = datetime.datetime.now().strftime("%d %B %Y")

        text = f"Today is {today}"

        speak(text)

        return text

    # Google
    elif "google" in command:

        webbrowser.open("https://www.google.com")

        speak("Opening Google")

        return "Opening Google"

    # YouTube
    elif "youtube" in command:

        webbrowser.open("https://www.youtube.com")

        speak("Opening YouTube")

        return "Opening YouTube"

    # Gmail
    elif "gmail" in command:

        webbrowser.open("https://mail.google.com")

        speak("Opening Gmail")

        return "Opening Gmail"

    # Reminder
    elif "reminder" in command:

        speak("How many minutes?")

        minutes = listen()

        try:

            minutes = int(minutes)

        except:

            return "Invalid number."

        speak("What should I remind you?")

        message = listen()

        if not message:
            return "Reminder message not recognized."

        threading.Thread(
            target=add_reminder,
            args=(minutes, message)
        ).start()

        speak("Reminder has been added.")

        return "Reminder has been set."

    # Show reminders
    elif "show reminders" in command:

        reminders = get_reminders()

        if len(reminders) == 0:
            return "No reminders."

        text = "\n".join(reminders)

        speak("Here are your reminders")

        return text

    # Exit
    elif "exit" in command or "quit" in command:

        speak("Goodbye")

        return "Goodbye"

    else:

        speak("Sorry, I don't know that command.")

        return "Unknown command."


if __name__ == "__main__":
    speak("Welcome. I am your Voice Assistant.")

    validate_keys()

    threading.Thread(
    target=check_reminders,
    args=(speak,),
    daemon=True
).start()
    
    app.run(host="0.0.0.0", port=5000)