from flask import Flask, render_template, request, jsonify
from weather import get_weather
from news import get_news
from reminder import (
    add_reminder,
    get_reminders,
    remove_reminder,
)
from config import validate_keys

import datetime
import re

app = Flask(__name__)


# --------------------------
# Home Page
# --------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------
# Main Command API
# --------------------------

@app.route("/command", methods=["POST"])
def command():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "response": "No command received."
        }), 400

    text = data.get("command", "").lower().strip()

    if text == "":
        return jsonify({
            "success": False,
            "response": "Empty command."
        })

    response = process_command(text)

    return jsonify({
        "success": True,
        "command": text,
        "response": response
    })


# --------------------------
# Process Commands
# --------------------------

def process_command(command):

    # ---------------- Weather ----------------

    if "weather" in command:

        city = extract_city(command)

        if city == "":
            return "Please say the city name. Example: What is the weather in Kochi?"

        return get_weather(city)

    # ---------------- News ----------------

    elif "news" in command:

        headlines = get_news()

        if len(headlines) == 0:
            return "Unable to fetch news."

        return "\n".join(headlines)

    # ---------------- Time ----------------

    elif "time" in command:

        return datetime.datetime.now().strftime(
            "Current time is %I:%M %p"
        )

    # ---------------- Date ----------------

    elif "date" in command:

        return datetime.datetime.now().strftime(
            "Today is %d %B %Y"
        )

    # ---------------- Google ----------------

    elif "google" in command:

        return {
            "message": "Opening Google",
            "action": "open_url",
            "url": "https://www.google.com"
    }

    # ---------------- YouTube ----------------

    elif "youtube" in command:

            return {
                "message": "Opening YouTube",
                "action": "open_url",
                "url": "https://www.youtube.com"
    }

    # ---------------- Gmail ----------------

    elif "gmail" in command:

            return {
                "message": "Opening Gmail",
                "action": "open_url",
                "url": "https://mail.google.com"
    }

    # ---------------- Reminder ----------------

    elif "remind" in command:

        result = parse_reminder(command)

        if result is None:
            return (
                "Example: Remind me to drink water in 10 minutes."
            )

        minutes, message = result

        add_reminder(minutes, message)

        return f"Reminder set for {minutes} minutes."

    # ---------------- Show Reminders ----------------

    elif "show reminders" in command:

        reminders = get_reminders()

        if len(reminders) == 0:
            return "No reminders."

        return "\n".join(reminders)

    # ---------------- Delete Reminder ----------------

    elif "delete reminder" in command:

        number = re.findall(r"\d+", command)

        if len(number) == 0:
            return "Please specify reminder number."

        success = remove_reminder(int(number[0]))

        if success:
            return "Reminder deleted."

        return "Reminder not found."

    # ---------------- Greeting ----------------

    elif "hello" in command or "hi" in command:

        return "Hello! How can I help you today?"

    # ---------------- Exit ----------------

    elif "bye" in command or "exit" in command:

        return "Goodbye! Have a nice day."

    # ---------------- Unknown ----------------

    else:

        return (
            "Sorry, I don't understand that command."
        )


# --------------------------
# Extract City
# --------------------------

def extract_city(command):

    match = re.search(r"weather in (.+)", command)

    if match:
        return match.group(1).strip()

    return ""


# --------------------------
# Parse Reminder
# Example:
# remind me to drink water in 5 minutes
# --------------------------

def parse_reminder(command):

    match = re.search(
        r"remind me to (.+) in (\d+) minute",
        command
    )

    if not match:

        match = re.search(
            r"remind me to (.+) in (\d+) minutes",
            command
        )

    if match:

        message = match.group(1)

        minutes = int(match.group(2))

        return minutes, message

    return None


# --------------------------
# Health Check
# --------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "running"
    })


# --------------------------
# Application Entry
# --------------------------

if __name__ == "__main__":

    validate_keys()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )