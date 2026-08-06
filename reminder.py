from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from bson.objectid import ObjectId
from database import reminders
from zoneinfo import ZoneInfo


# --------------------------
# Add Reminder
# --------------------------

def add_reminder(minutes, message):

    reminder_time = (
        datetime.now(timezone.utc)
        + timedelta(minutes=minutes)
    )

    reminders.insert_one({
        "message": message,
        "time": reminder_time,
        "completed": False
    })


# --------------------------
# Get Pending Reminders
# --------------------------

def get_reminders():

    data = reminders.find({
        "completed": False
    }).sort("time", 1)

    result = []

    for i, reminder in enumerate(data, start=1):

        ist_time = reminder["time"].astimezone(
            ZoneInfo("Asia/Kolkata")
        )

        result.append(
            f"{i}. {reminder['message']} - "
            f"{ist_time.strftime('%d-%m-%Y %I:%M %p')}"
        )

    return result


# --------------------------
# Check Due Reminders
# --------------------------

def due_reminders():

    now = datetime.now(timezone.utc)

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


# --------------------------
# Remove Reminder
# --------------------------

def remove_reminder(index):

    data = list(
        reminders.find({
            "completed": False
        }).sort("time", 1)
    )

    if index < 1 or index > len(data):
        return False

    reminder = data[index - 1]

    result = reminders.delete_one({
        "_id": reminder["_id"]
    })

    return result.deleted_count > 0