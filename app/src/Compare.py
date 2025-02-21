from app.services.Storage import Storage
import cv2
import numpy as np
from datetime import datetime, timedelta
import face_recognition

class Compare:
    def __init__(self, face_recognition: face_recognition):
        self.face_recognition = face_recognition
        self.storage = Storage()
        self.users = self.storage.get_all_users()
        
    
    def _saveFaces(self, frame,  face_locations):
        face_encodings = self.face_recognition.face_encodings(frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            matches = []

            for user in self.users:
                stored_encoding = np.array(user['face_encoding'])
                result = self.face_recognition.compare_faces(
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

                    self.storage.update_face(user_data)
                else:
                    print(
                        f"Rostro identificado: {user['user_id']}, pero no han pasado 10 minutos desde la última vez.")
            else:
                user_id = str(np.random.randint(1000, 9999))
                _, buffer = cv2.imencode('.jpg', frame)
                face_image_binary = buffer.tobytes()

                self.storage.save_face(user_id, face_encoding, face_image_binary)
                print(f"Nuevo rostro detectado y guardado con ID: {user_id}")
