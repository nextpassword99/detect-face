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
        
    def _saveFaces(self, frame, face_locations):
        face_encodings = self.face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            face = self._find_face(face_encoding)
            if face is None:
                user_id = self._save_user()
                print('Nuevo rostro')
            else:
                user_id = face['user_id']
                print('Rostro reconocido')

            self.storage.save_image(user_id, face_encoding, frame)
            self.faces = self.storage.get_all_faces()

    def _find_face(self, face_encoding):
        for face in self.faces:
            stored_encoding = np.array(face['face_encoding'])
            result = self.face_recognition.compare_faces([stored_encoding], face_encoding, tolerance=0.4)

            if result[0]:
                return face
        return None
    
    def _save_user(self):
        id = str(np.random.randint(1000, 9999))
        user = {
            'user_id': id,
            'name': 'Desconocido',
        }

        self.storage.save_user(user)

        return id
