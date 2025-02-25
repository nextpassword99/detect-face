from app.services.Storage import Storage
import cv2
import numpy as np
from datetime import datetime, timedelta
import face_recognition

class Compare:
    def __init__(self, face_recognition: face_recognition):
        self.face_recognition = face_recognition
        self.storage = Storage()
        self.faces = self.storage.get_all_faces()
        
    
    def _saveFaces(self, frame,  face_locations):
        face_encodings = self.face_recognition.face_encodings(frame, face_locations)

        for face_encoding in zip(face_encodings):
            
            face = self._find_face(face_encoding)

            if face:
                last_saved = face['timestamp']
                now = datetime.now()

                time_difference = now - last_saved
                if time_difference > timedelta(minutes=10):
                    print(
                        f"Rostro identificado: {face['user_id']}, actualizando imagen.")

                    user_data = {
                        "user_id": face['user_id'],
                        "face_encoding": face_encoding.tolist(),
                        "face_image_id": face['user_id'],
                        "timestamp": now
                    }

                    self.storage.update_face(user_data)
                else:
                    print(
                        f"Rostro identificado: {face['user_id']}, pero no han pasado 10 minutos desde la última vez.")
            else:
                user_id = self._save_user()
                
                print(f"Nuevo rostro detectado y guardado con ID: {user_id}")

    def _find_face(self, face_encoding):
        for face in self.faces:
            stored_encoding = np.array(face['face_encoding'])
            result = self.face_recognition.compare_faces(
                [stored_encoding], face_encoding, tolerance=0.4)
            return result[0] or None
    
    def _find():
        pass
    
    def _update_data(self):
        pass
        
    def _save_user(self):
        id = str(np.random.randint(1000, 9999))
        user = {
            'user_id': id,
            'name': 'Desconocido',
        }

        self.storage.save_user(user)

        return id

    def _save_face(self):
        pass