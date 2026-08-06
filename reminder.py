from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from bson.objectid import ObjectId
from database import reminders


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

    for reminder in data:

        ist_time = reminder["time"].astimezone(
            ZoneInfo("Asia/Kolkata")
        )

        result.append(
            f'{reminder["message"]} - {ist_time.strftime("%d-%m-%Y %I:%M %p")}'
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

def remove_reminder(reminder_id):

    try:

        result = reminders.delete_one({
            "_id": ObjectId(reminder_id)
        })

        return result.deleted_count > 0

    except Exception:
        return False