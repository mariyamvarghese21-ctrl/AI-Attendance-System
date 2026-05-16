import cv2
import csv
import os
from datetime import datetime

# ==============================
# ENTER STUDENT NAME
# ==============================

student_name = input("Enter Student Name: ")

# ==============================
# CREATE DAILY CSV FILE
# ==============================

today_date = datetime.now().strftime("%Y-%m-%d")

csv_filename = f"attendance_{today_date}.csv"

# Create file if not exists
if not os.path.exists(csv_filename):

    with open(csv_filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Name", "Date", "Time"])

# ==============================
# CHECK DUPLICATE ATTENDANCE
# ==============================

attendance_marked = False

with open(csv_filename, "r") as file:

    reader = csv.reader(file)

    next(reader)

    for row in reader:

        if row[0] == student_name:

            attendance_marked = True

            break

# ==============================
# LOAD FACE DETECTION MODEL
# ==============================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# ==============================
# OPEN WEBCAM
# ==============================

camera = cv2.VideoCapture(0)

attendance_count = 0

print("\nSMART AI ATTENDANCE SYSTEM")
print("Press A to mark attendance")
print("Press Q to quit")

# ==============================
# MAIN LOOP
# ==============================

while True:

    success, frame = camera.read()

    if not success:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(50, 50)
    )

    # ==============================
    # DRAW RECTANGLES AROUND FACES
    # ==============================

    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # ==============================
    # DISPLAY TEXT ON SCREEN
    # ==============================

    cv2.putText(
        frame,
        "SMART AI ATTENDANCE SYSTEM",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Student: {student_name}",
        (10, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Attendance Count: {attendance_count}",
        (10, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press A to Mark Attendance",
        (10, 135),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Quit",
        (10, 170),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # ==============================
    # SHOW WEBCAM WINDOW
    # ==============================

    cv2.imshow("AI Attendance System", frame)

    key = cv2.waitKey(1)

    # ==============================
    # MARK ATTENDANCE
    # ==============================

    if key == ord('a'):

        # Duplicate check
        if attendance_marked:

            print("Attendance Already Marked")

        else:

            now = datetime.now()

            date = now.strftime("%Y-%m-%d")

            time = now.strftime("%H:%M:%S")

            # Save attendance
            with open(csv_filename, "a", newline="") as file:

                writer = csv.writer(file)

                writer.writerow([student_name, date, time])

            # Create captures folder if not exists
            if not os.path.exists("captures"):

                os.makedirs("captures")

            # Save image
            image_name = f"captures/{student_name}_{time.replace(':', '-')}.jpg"

            cv2.imwrite(image_name, frame)

            attendance_count += 1

            attendance_marked = True

            print("Attendance Marked Successfully")

    # ==============================
    # QUIT PROGRAM
    # ==============================

    elif key == ord('q'):

        break

# ==============================
# CLOSE EVERYTHING
# ==============================

camera.release()

cv2.destroyAllWindows()