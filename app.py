from flask import Flask, render_template, request, jsonify
from weather import get_weather
from news import get_news
from reminder import (
    add_reminder,
    get_reminders,
    remove_reminder,
    due_reminders,
)
from config import validate_keys

from datetime import datetime
from zoneinfo import ZoneInfo
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
            return "Please say the city name. Example: What is the weather today?"

        return get_weather(city)

    # ---------------- News ----------------

    elif "news" in command:

        headlines = get_news()

        if len(headlines) == 0:
            return "Unable to fetch news."

        return "\n".join(headlines)

    # ---------------- Time ----------------

    elif "time" in command:
        current_time = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%I:%M %p")
        return f"Current time is {current_time}"

    # ---------------- Date ----------------

    elif "date" in command:
        today = datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime("%d %B %Y")
        return f"Today is {today}"

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

# ---------------- Show Reminders ----------------
    elif "show reminders" in command or "list reminders" in command:
        reminder_list = get_reminders()
        print("MongoDB Reminders:", reminder_list)
        if not reminder_list:
            return "No reminders found."
        return "\n".join(reminder_list)


# ---------------- Add Reminder ----------------

    elif "remind me" in command or "set reminder" in command:
        result = parse_reminder(command)
        if result is None:
            return "Example: Remind me to study in 10 minutes."
        minutes, message = result
        add_reminder(minutes, message)
        return f"Reminder set for {minutes} minutes."


# ---------------- Delete Reminder ----------------
    
    elif "delete reminder" in command:
        number = re.findall(r"\d+", command)
        if not number:
            return "Please say the reminder number."
        success = remove_reminder(int(number[0]))
        if success:
            return f"Reminder {number[0]} deleted."
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

import re

def parse_reminder(command):

    command = command.lower().strip()

    patterns = [

        # Remind me to drink water in 10 minutes
        r"remind me to (.+) in (\d+) minute[s]?",

        # Set reminder to study in 20 minutes
        r"set reminder to (.+) in (\d+) minute[s]?",

        # Reminder to call mom in 15 minutes
        r"reminder to (.+) in (\d+) minute[s]?"
    ]

    for pattern in patterns:

        match = re.search(pattern, command)

        if match:

            message = match.group(1).strip()
            minutes = int(match.group(2))

            return minutes, message

    # Support: "Set reminder for 20 minutes"
    match = re.search(
        r"set reminder for (\d+) minute[s]?",
        command
    )

    if match:

        minutes = int(match.group(1))

        return minutes, "Reminder"

    return None


# --------------------------
# Health Check
# --------------------------

@app.route("/health")
def health():

    return jsonify({
        "status": "running"
    })


@app.route("/check-reminders")
def check_due():

    reminders = due_reminders()

    return jsonify({
        "reminders": reminders
    })

@app.route("/debug-reminders")
def debug_reminders():
    from reminder import load_reminders
    return jsonify(load_reminders())


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