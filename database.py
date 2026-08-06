from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client["voiceassistant"]

reminders = db["reminders"]