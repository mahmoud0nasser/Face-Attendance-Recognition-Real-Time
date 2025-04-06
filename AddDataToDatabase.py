import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-9a1b6-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Mahmoud Nasser",
            "major": "Generative AI",
            "starting_year": 2024,
            "total_attendance": 6,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2024-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emily Blunt",
            "major": "Graphic Designer",
            "starting_year": 2025,
            "total_attendance": 3,
            "standing": "B",
            "year": 4,
            "last_attendance_time": "2025-03-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Business Man",
            "starting_year": 2023,
            "total_attendance": 12,
            "standing": "A",
            "year": 10,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)

# Storage For Images

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

