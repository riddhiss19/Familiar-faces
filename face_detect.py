import face_recognition
import cv2
import time
import os


def recognize_faces():
    # Load saved face images
    saved_face_encodings = []
    saved_face_names = []

    for file in os.listdir("uploads"):
        image = face_recognition.load_image_file(f"uploads/{file}")
        encoding = face_recognition.face_encodings(image)[0]

        name = os.path.splitext(file)[0]
        saved_face_encodings.append(encoding)
        saved_face_names.append(name)

    # Start video capture
    video_capture = cv2.VideoCapture(0)

    times = 0
    names = ""
    while True:
        ret, frame = video_capture.read()

        # Detect faces in live camera feed
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        no_face_timer = time.time()
        for face_encoding in face_encodings:
            # Match with saved faces
            matches = face_recognition.compare_faces(
                saved_face_encodings, face_encoding
            )
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = saved_face_names[first_match_index]
                times += 1

                if times >= 8:
                    break
                    
            # Draw label with name
            (top, right, bottom, left) = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            cv2.putText(
                frame,
                name,
                (left + 6, bottom - 6),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                1,
            )

        # Display result
        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) == ord("q"):
            break
        elif time.time() - no_face_timer > 10:
            # No face for 10 seconds, break out
            return False

    video_capture.release()
    cv2.destroyAllWindows()
    return name
