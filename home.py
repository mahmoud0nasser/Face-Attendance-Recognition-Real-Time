import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import shutil
import subprocess
import cloudinary
import cloudinary.uploader
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Firebase Init
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-9a1b6-default-rtdb.firebaseio.com/"
})
ref = db.reference('Students')

# Cloudinary Config
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# Root Window
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("500x550")
root.config(bg="#f0f0f5")

# Main Frames
home_frame = tk.Frame(root, bg="#f0f0f5")
add_frame = tk.Frame(root, bg="#f0f0f5")
show_frame = tk.Frame(root, bg="#f0f0f5")

for frame in (home_frame, add_frame, show_frame):
    frame.place(relwidth=1, relheight=1)

def show_frame_func(frame):
    frame.tkraise()

# ---------------------- HOME FRAME -----------------------
def build_home():
    for widget in home_frame.winfo_children():
        widget.destroy()

    tk.Label(home_frame, text="👨‍💼 Face Recognition Attendance System", font=("Helvetica", 18, "bold"), bg="#f0f0f5", fg="#673ab7").pack(pady=30)

    tk.Button(home_frame, text="➕ Add New Employee", font=("Helvetica", 12),
              width=25, height=2, bg="#9c27b0", fg="white", relief="flat",
              command=lambda: show_frame_func(add_frame)).pack(pady=10, padx=15)

    tk.Button(home_frame, text="🕵️‍♂️ Start Attendance", font=("Helvetica", 12),
              width=25, height=2, bg="#2196f3", fg="white", relief="flat",
              command=start_attendance).pack(pady=10, padx=15)

    tk.Button(home_frame, text="👀 Show All Employees", font=("Helvetica", 12),
              width=25, height=2, bg="#3f51b5", fg="white", relief="flat",
              command=lambda: [build_show_all(), show_frame_func(show_frame)]).pack(pady=10, padx=15)

# ---------------------- ADD EMPLOYEE FRAME -----------------------
def build_add_employee():
    for widget in add_frame.winfo_children():
        widget.destroy()

    tk.Label(add_frame, text="Add New Employee", font=("Helvetica", 18, "bold"), bg="#f0f0f5", fg="#673ab7").pack(pady=10)

    fields = {}
    labels = ["Name", "Student ID", "Major", "Year", "Standing", "Starting Year"]
    for label in labels:
        tk.Label(add_frame, text=label, bg="#f0f0f5", font=("Helvetica", 12), fg="#333333").pack()
        entry = tk.Entry(add_frame, font=("Helvetica", 12))
        entry.pack(pady=5, padx=20)
        fields[label.lower().replace(" ", "_")] = entry

    image_path = tk.StringVar()

    def browse_image():
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        image_path.set(path)

    def submit_data():
        name = fields['name'].get()
        student_id = fields['student_id'].get()
        if not all([name, student_id, image_path.get()]):
            messagebox.showwarning("Missing Data", "Please fill all fields and select an image.")
            return

        upload_result = cloudinary.uploader.upload(image_path.get(), public_id=f"students/{student_id}")
        image_url = upload_result['secure_url']

        if not os.path.exists("Images"):
            os.makedirs("Images")

        shutil.copy(image_path.get(), f"Images/{student_id}.jpg")

        student_data = {
            "name": name,
            "major": fields['major'].get(),
            "starting_year": fields['starting_year'].get(),
            "total_attendance": 0,
            "standing": fields['standing'].get(),
            "year": fields['year'].get(),
            "last_attendance_time": "2000-01-01 00:00:00",
            "image_url": image_url
        }

        ref.child(student_id).set(student_data)
        messagebox.showinfo("Success", f"{name} added successfully!")
        subprocess.run(["python", "encodeGenerator.py"])
        show_frame_func(home_frame)

    tk.Button(add_frame, text="📁 Select Image", command=browse_image, bg="#9c27b0", fg="white", relief="flat").pack(pady=10)
    tk.Label(add_frame, textvariable=image_path, bg="#f0f0f5", font=("Helvetica", 12), fg="#333333").pack(pady=5)

    tk.Button(add_frame, text="✅ Submit", command=submit_data, bg="#4caf50", fg="white", relief="flat", font=("Helvetica", 12)).pack(pady=10)
    tk.Button(add_frame, text="⬅️ Back to Home", command=lambda: show_frame_func(home_frame), bg="#f44336", fg="white", relief="flat", font=("Helvetica", 12)).pack(pady=10)

# ---------------------- SHOW EMPLOYEES FRAME -----------------------
def build_show_all():
    for widget in show_frame.winfo_children():
        widget.destroy()

    # Title Label
    tk.Label(show_frame, text="All Employees", font=("Helvetica", 20, "bold"), bg="#f0f0f5", fg="#673ab7").pack(pady=30)

    # Treeview Frame for better alignment
    tree_frame = tk.Frame(show_frame, bg="#f0f0f5")
    tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Adding Scrollbars
    tree_scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
    tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")

    tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Major", "Year"), show="headings", style="Treeview.Heading", yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

    # Configure scrollbars
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)

    # Scrollbars placement
    tree_scroll_y.pack(side=tk.RIGHT, fill="y")
    tree_scroll_x.pack(side=tk.BOTTOM, fill="x")

    # Treeview headings
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Major", text="Major")
    tree.heading("Year", text="Year")

    # Set column widths
    tree.column("ID", width=120, anchor="center")
    tree.column("Name", width=200, anchor="w")
    tree.column("Major", width=150, anchor="w")
    tree.column("Year", width=100, anchor="center")

    # Custom style for alternating row colors
    def style_treeview():
        for index, row in enumerate(tree.get_children()):
            if index % 2 == 0:
                tree.tag_configure(f"even_row", background="#673ab7")
                tree.item(row, tags="even_row")
            else:
                tree.tag_configure(f"odd_row", background="#4caf50")
                tree.item(row, tags="odd_row")

    # Insert data
    data = ref.get()
    if data:
        for student_id, info in data.items():
            tree.insert("", tk.END, values=(student_id, info.get("name"), info.get("major"), info.get("year")))
        style_treeview()

    # Treeview Pack
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Back Button
    tk.Button(show_frame, text="⬅️ Back to Home", command=lambda: show_frame_func(home_frame), bg="#673ab7", fg="white", relief="flat", font=("Helvetica", 14, "bold"), width=20, height=2).pack(pady=20)

# ---------------------- START ATTENDANCE -----------------------
def start_attendance():
    subprocess.run(["python", "AttendanceSystem.py"])

# ---------------------- Style for Treeview ----------------------
style = ttk.Style()
style.configure("Treeview",
                background="#ffffff",
                foreground="black",
                rowheight=25,
                fieldbackground="#f0f0f5")

style.configure("Treeview.Heading",
                background="#673ab7",
                foreground="white",
                font=("Helvetica", 14, "bold"))

# ---------------------- Build and Start -----------------------
build_home()
build_add_employee()
show_frame_func(home_frame)

root.mainloop()
