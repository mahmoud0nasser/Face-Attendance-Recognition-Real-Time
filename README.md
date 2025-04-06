```markdown
# 🎓 Face Recognition Attendance System

This is a Face Recognition-based Attendance System built with Python, OpenCV, and `face_recognition`, integrated with Firebase and Cloudinary for real-time database and image storage.

## 🚀 Features

- Real-time face recognition via webcam  
- Automatically logs student attendance  
- Syncs student data with Firebase Realtime Database  
- Uploads and retrieves images from **Cloudinary** and **Firebase Storage**  
- Beautiful GUI display using `cvzone` and custom templates  
- Prevents duplicate attendance entries within a short time window  

---

## 🛠️ Technologies Used

- Python  
- OpenCV  
- face_recognition  
- Firebase Admin SDK  
- Cloudinary  
- cvzone  
- NumPy  
- Pickle  

---

## 📂 Project Structure

```
.
├── AddDatatoDatabase.py         # Script to upload students data to Firebase
├── EncodeGenerator.py           # Generates face encodings and uploads images to Cloudinary & Firebase
├── Artificats/
│   ├── EncodeFile.p             # Pickled file containing encodings and student IDs
├── AttendanceSystem.py          # Main application file for real-time recognition
├── serviceAccountKey.json       # Firebase Admin SDK credentials
├── config.json                  # Cloudinary Storage
├── Images/                      # Folder containing employee images
├── Resources/
│   ├── background.png           # Main UI template background
│   └── Modes/                   # Contains various UI screens/modes (e.g., loading, success)
└── README.md                    # You are here
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

> Or install them individually:

```bash
pip install opencv-python face_recognition firebase-admin numpy cvzone cloudinary
```

---

## 🔐 Firebase Configuration

1. Create a Firebase project from the [Firebase Console](https://console.firebase.google.com).
2. Set up:
   - **Realtime Database**
   - **Firebase Storage**
3. Go to Project Settings → Service accounts → Generate new private key  
4. Save the JSON as `serviceAccountKey.json` in the project root  
5. Replace placeholders in Python files:
   - `databaseURL`: your Realtime Database URL  
   - `storageBucket`: your Firebase storage bucket link (e.g. `your-project-id.appspot.com`)  

---

## 🌥️ Cloudinary Integration (Optional)

Used optionally to store/retrieve student images.

1. Sign up at [https://cloudinary.com](https://cloudinary.com)  
2. Get your `CLOUD_NAME`, `API_KEY`, and `API_SECRET`  
3. Add a `.env` file or hardcode (not recommended for production):

```bash
CLOUD_NAME=your_cloud_name
API_KEY=your_api_key
API_SECRET=your_api_secret
```

> Update the code in `EncodeGenerator.py` to upload images to Cloudinary if needed:

```python
import cloudinary
import cloudinary.uploader

cloudinary.config(
  cloud_name = "your_cloud_name",
  api_key = "your_api_key",
  api_secret = "your_api_secret"
)

response = cloudinary.uploader.upload(fileName, public_id=path)
```

---

## 📸 Adding Student Images

Place your student images in the `Images/` folder with the filename as the student ID (e.g. `321654.jpg`).

---

## 🧪 Running the Project

1. **Add Employee Data to Firebase**

```bash
python AddDatatoDatabase.py
```

2. **Generate Encodings**

```bash
python EncodeGenerator.py
```

3. **Start the Attendance App**

```bash
python AttendanceSystem.py
```
4. **Start the home app**

```bash
python home.py
```

---

## 📦 Output

- Attendance marked in Firebase Realtime Database under `/Students`
- Student details with image shown on GUI
- Images can also be stored in Cloudinary for backup or CDN-based usage

---

## 🧑‍🎓 Sample Student Data Format in Firebase

```json
{
  "321654": {
    "name": "Mahmoud Nasser",
    "major": "Generative AI",
    "starting_year": 2024,
    "total_attendance": 7,
    "standing": "G",
    "year": 4,
    "last_attendance_time": "2022-12-11 00:54:34"
  }
}
```

---

## ✅ To-Do & Improvements

- [ ] Add support for multiple cameras  
- [ ] Add user-friendly GUI to manage student data  
- [ ] Cloudinary-based image fallback when Firebase image fails  
- [ ] Dockerize the project for easier deployment  

---

## 🙏 Credits

- Firebase & Cloudinary platforms  

---

## 📄 License

This project is licensed under the MIT License. Feel free to fork and build upon it!
```
