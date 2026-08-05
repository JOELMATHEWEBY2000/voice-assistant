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
    Load reminders safely.
    """

    if not os.path.exists(REMINDER_FILE):
        return []

    try:
        with open(REMINDER_FILE, "r") as file:

            content = file.read().strip()

            if not content:
                return []

            return json.loads(content)

    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_reminders(reminders):

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

    reminders = load_reminders()

    if not reminders:
        return []

    result = []

    for i, reminder in enumerate(reminders, start=1):

        status = "Completed" if reminder["completed"] else "Pending"

        result.append(
            f"{i}. {reminder['message']} - {reminder['time']} ({status})"
        )

    return result

def due_reminders():

    reminders = load_reminders()

    now = datetime.now()

    due = []

    changed = False

    for reminder in reminders:

        if reminder["completed"]:
            continue

        reminder_time = datetime.strptime(
            reminder["time"],
            "%Y-%m-%d %H:%M:%S"
        )

        if now >= reminder_time:

            due.append(reminder["message"])

            reminder["completed"] = True

            changed = True

    if changed:
        save_reminders(reminders)

    return due



def remove_reminder(index):

    reminders = load_reminders()

    pending = [r for r in reminders if not r["completed"]]

    if index < 1 or index > len(pending):
        return False

    reminder_to_remove = pending[index - 1]

    reminders.remove(reminder_to_remove)

    save_reminders(reminders)

    return True