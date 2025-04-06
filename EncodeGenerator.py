import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import cv2
import face_recognition
import os
import pickle

load_dotenv()  # load environment variables from .env

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-9a1b6-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Importing The Student Images
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIDs = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    student_ID = os.path.splitext(path)[0]
    studentIDs.append(student_ID)
    # print(path)
    # print(os.path.splitext(path)[0])

    img_path = os.path.join(folderPath, path)
    img = cv2.imread(img_path)

    if img is None:
        print(f"Skipping {path} due to load error.")
        continue

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(img_path, public_id=f"students/{student_ID}")
    print(f"Uploaded {student_ID}: {upload_result['secure_url']}")

    # Optional: Save Cloudinary URL to Firebase Realtime DB
    db.reference(f"Students/{student_ID}").update({
        "image_url": upload_result['secure_url']
    })

# print(len(imgList))

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDs = [encodeListKnown, studentIDs]
# print(encodeListKnown)
print("Encoding Complete")

file = open("Artifacts/EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIDs, file)
file.close()
print("File Saved")
