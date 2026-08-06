import json
import os
import time
from datetime import datetime, timedelta
from database import reminders
from bson.objectid import ObjectId

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

    reminder_time = datetime.now() + timedelta(minutes=minutes)

    reminders.insert_one({

        "message": message,

        "time": reminder_time,

        "completed": False

    })



def get_reminders():

    data = reminders.find({

        "completed": False

    }).sort("time")

    result = []

    for reminder in data:

        result.append(

            f'{reminder["message"]} - {reminder["time"].strftime("%d-%m-%Y %H:%M")}'

        )

    return result

def due_reminders():

    now = datetime.now()

    data = reminders.find({

        "completed": False,

        "time": {"$lte": now}

    })

    due = []

    for reminder in data:

        due.append(reminder["message"])

        reminders.update_one(

            {"_id": reminder["_id"]},

            {"$set": {"completed": True}}

        )

    return due


def remove_reminder(reminder_id):

    result = reminders.delete_one({

        "_id": ObjectId(reminder_id)

    })

    return result.deleted_count > 0