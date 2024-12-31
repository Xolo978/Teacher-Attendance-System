from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)

db = client["teacher_attendance"]
attendance = db["attendance"]
teachers = db["teachers"]
students = db["students"]

if __name__ == "__main__":
    print("Connected to the database",client.server_info())