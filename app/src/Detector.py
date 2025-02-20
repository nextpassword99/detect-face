from app.config.Database import Database
from datetime import datetime, timedelta
import face_recognition
import cv2
import numpy as np


class Detector:
    def __init__(self):
        self._initializeCamera()
        self.db = Database()
        self.users = self.db.get_all_users()

        while True:
            frame = self._captureFrame()
            if frame is not None:
                face_locations = self._faceLocations(frame)
                self._displayVideo(frame, face_locations)
                self._saveFaces(frame, face_locations)
            else:
                print('No frame')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self._releaseResources()

    def _initializeCamera(self):
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Error: No se pudo abrir la cámara.")
            exit(1)

    def _captureFrame(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return None
        return frame

    def _faceLocations(self, frame):
        frame = frame[:, :, ::-1]
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return face_recognition.face_locations(frame)

    def _displayVideo(self, frame, face_locations):
        for top, right, bottom, left in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

    def _releaseResources(self):
        if self.video_capture is not None:
            self.video_capture.release()
        cv2.destroyAllWindows()

    def _saveFaces(self, frame, face_locations):
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            matches = []

            for user in self.users:
                stored_encoding = np.array(user['face_encoding'])
                result = face_recognition.compare_faces(
                    [stored_encoding], face_encoding, tolerance=0.4)
                if result[0]:
                    matches.append(user)

            if matches:
                user = matches[0]
                last_saved = user['timestamp']
                now = datetime.now()

                time_difference = now - last_saved
                if time_difference > timedelta(minutes=10):
                    print(
                        f"Rostro identificado: {user['user_id']}, actualizando imagen.")

                    _, buffer = cv2.imencode('.jpg', frame)
                    face_image_binary = buffer.tobytes()

                    user_data = {
                        "user_id": user['user_id'],
                        "face_encoding": face_encoding.tolist(),
                        "face_image_id": user['user_id'],
                        "timestamp": now
                    }

                    self.db.update_face(user_data)
                else:
                    print(
                        f"Rostro identificado: {user['user_id']}, pero no han pasado 10 minutos desde la última vez.")
            else:
                user_id = str(np.random.randint(1000, 9999))
                _, buffer = cv2.imencode('.jpg', frame)
                face_image_binary = buffer.tobytes()

                self.db.save_face(user_id, face_encoding, face_image_binary)
                print(f"Nuevo rostro detectado y guardado con ID: {user_id}")
