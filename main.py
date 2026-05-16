import cv2
import csv
import os
from datetime import datetime

# ==========================================
# ENTER STUDENT NAME
# ==========================================

student_name = input("Enter Student Name: ")

# ==========================================
# CREATE DAILY CSV FILE
# ==========================================

today_date = datetime.now().strftime("%Y-%m-%d")

csv_filename = f"attendance_{today_date}.csv"

if not os.path.exists(csv_filename):

    with open(csv_filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Name", "Date", "Time"])

# ==========================================
# CHECK DUPLICATE ATTENDANCE
# ==========================================

attendance_marked = False

with open(csv_filename, "r") as file:

    reader = csv.reader(file)

    next(reader)

    for row in reader:

        if row[0] == student_name:

            attendance_marked = True

            break

# ==========================================
# CREATE CAPTURES FOLDER
# ==========================================

if not os.path.exists("captures"):

    os.makedirs("captures")

# ==========================================
# LOAD FACE DETECTOR
# ==========================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ==========================================
# OPEN CAMERA
# ==========================================

camera = cv2.VideoCapture(0)

attendance_count = 0

status_message = "System Ready"

status_color = (0, 255, 0)

print("\nSMART AI ATTENDANCE SYSTEM")
print("Press A to mark attendance")
print("Press Q to quit")

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, frame = camera.read()

    if not success:

        print("Camera Error")

        break

    # Flip camera for mirror view
    frame = cv2.flip(frame, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # ==========================================
    # FACE DETECTION RECTANGLES
    # ==========================================

    for (x, y, w, h) in faces:

        # Face rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            3
        )

        # Name background
        cv2.rectangle(
            frame,
            (x, y - 35),
            (x + w, y),
            (0, 255, 0),
            -1
        )

        # Student name
        cv2.putText(
            frame,
            student_name,
            (x + 10, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 0),
            2
        )

    # ==========================================
    # HEADER SECTION
    # ==========================================

    cv2.rectangle(
        frame,
        (0, 0),
        (800, 80),
        (30, 30, 30),
        -1
    )

    cv2.putText(
        frame,
        "SMART AI ATTENDANCE SYSTEM",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        3
    )

    cv2.putText(
        frame,
        "Powered by OpenCV",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==========================================
    # SIDE INFORMATION PANEL
    # ==========================================

    cv2.rectangle(
        frame,
        (0, 80),
        (350, 280),
        (50, 50, 50),
        -1
    )

    # Student Name
    cv2.putText(
        frame,
        f"Student: {student_name}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    # Attendance Count
    cv2.putText(
        frame,
        f"Attendance Count: {attendance_count}",
        (20, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Face Count
    cv2.putText(
        frame,
        f"Faces Detected: {len(faces)}",
        (20, 230),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # Current Date and Time
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cv2.putText(
        frame,
        current_time,
        (20, 270),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==========================================
    # STATUS BOX
    # ==========================================

    cv2.rectangle(
        frame,
        (0, 280),
        (800, 340),
        (40, 40, 40),
        -1
    )

    cv2.putText(
        frame,
        f"STATUS: {status_message}",
        (20, 320),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        status_color,
        2
    )

    # ==========================================
    # INSTRUCTION PANEL
    # ==========================================

    cv2.rectangle(
        frame,
        (0, 340),
        (800, 430),
        (20, 20, 20),
        -1
    )

    cv2.putText(
        frame,
        "Press A to Mark Attendance",
        (20, 380),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Quit",
        (20, 415),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    # ==========================================
    # SHOW WINDOW
    # ==========================================

    cv2.imshow("AI Attendance System", frame)

    # Keyboard handling
    key = cv2.waitKey(1) & 0xFF

    # ==========================================
    # MARK ATTENDANCE
    # ==========================================

    if key == ord('a'):

        if attendance_marked:

            status_message = "Attendance Already Marked"

            status_color = (0, 0, 255)

            print("Attendance Already Marked")

        else:

            now = datetime.now()

            date = now.strftime("%Y-%m-%d")

            time = now.strftime("%H:%M:%S")

            # Save attendance to CSV
            with open(csv_filename, "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([student_name, date, time])

            # Save image to captures folder
            image_name = os.path.join(
                "captures",
                f"{student_name}_{time.replace(':', '-')}.jpg"
            )

            saved = cv2.imwrite(image_name, frame)

            if saved:

                attendance_count += 1

                attendance_marked = True

                status_message = "Attendance Marked Successfully"

                status_color = (0, 255, 0)

                print("Attendance Marked Successfully")

                print(f"Image Saved: {image_name}")

            else:

                status_message = "Image Saving Failed"

                status_color = (0, 0, 255)

                print("Image Saving Failed")

    # ==========================================
    # QUIT PROGRAM
    # ==========================================

    elif key == ord('q'):

        print("Program Closed")

        break

# ==========================================
# CLOSE EVERYTHING
# ==========================================

camera.release()

cv2.destroyAllWindows()