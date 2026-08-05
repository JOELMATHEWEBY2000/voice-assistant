import json
import os
import time
from datetime import datetime, timedelta

REMINDER_FILE = "reminders.json"


def initialize_file():
    """
    Create reminders.json if it doesn't exist.
    """
    if not os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, "w") as file:
            json.dump([], file, indent=4)


initialize_file()


def load_reminders():
    """
    Load reminders from JSON file.
    """
    with open(REMINDER_FILE, "r") as file:
        return json.load(file)


def save_reminders(reminders):
    """
    Save reminders to JSON file.
    """
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)


def add_reminder(minutes, message):
    """
    Add a reminder after specified minutes.
    """

    reminders = load_reminders()

    reminder_time = datetime.now() + timedelta(minutes=minutes)

    reminder = {
        "message": message,
        "time": reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
        "completed": False
    }

    reminders.append(reminder)

    save_reminders(reminders)


def get_reminders():
    """
    Return all pending reminders.
    """

    reminders = load_reminders()

    pending = []

    for reminder in reminders:

        if not reminder["completed"]:
            pending.append(
                f'{reminder["time"]} : {reminder["message"]}'
            )

    return pending


def check_reminders(speak):
    """
    Continuously check reminders and announce them.
    """

    while True:

        reminders = load_reminders()

        updated = False

        current_time = datetime.now()

        for reminder in reminders:

            if reminder["completed"]:
                continue

            reminder_time = datetime.strptime(
                reminder["time"],
                "%Y-%m-%d %H:%M:%S"
            )

            if current_time >= reminder_time:

                speak("Reminder")

                speak(reminder["message"])

                reminder["completed"] = True

                updated = True

        if updated:
            save_reminders(reminders)

        time.sleep(30)

def remove_reminder(index):

    reminders = load_reminders()

    pending = [r for r in reminders if not r["completed"]]

    if index < 1 or index > len(pending):
        return False

    reminder_to_remove = pending[index - 1]

    reminders.remove(reminder_to_remove)

    save_reminders(reminders)

    return True