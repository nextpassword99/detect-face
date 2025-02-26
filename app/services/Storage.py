from app.database.Database import Database
from typing import Dict, Any, Optional
import bson
from datetime import datetime
import numpy as np
import cv2

class Storage (Database):
    def save_face(self, user_id: str, face_encoding: list, frame) -> str:
        face_encoding_list = face_encoding.tolist() if isinstance(
            face_encoding, np.ndarray) else face_encoding

        face_document = {
            "user_id": user_id,
            "face_encoding": face_encoding_list,
            "timestamp": datetime.now()
        }

        return self.insertDocument("faces", face_document)
    
    def get_user_by_face_encoding(self, face_encoding: list) -> Optional[Dict[str, Any]]:
        return self.findDocument("faces", {"face_encoding": face_encoding})

    def get_all_users(self):
        return list(self.db["users"].find())

    def get_all_faces(self):
        return list(self.db["faces"].find())

    def update_face(self, user_data):
        user_id = user_data['user_id']
        
        user = self.findDocument('users', {'user_id': user_id})

        if user:
            updated_data = {
                'face_encoding': user_data['face_encoding'],
                'face_image_id': user_data['face_image_id'],
                'timestamp': user_data['timestamp']
            }
            updated_count = self.updateDocument('users', {'user_id': user_id}, updated_data)
            
            if updated_count > 0:
                print(f"Datos del rostro para el usuario {user_id} actualizados exitosamente.")
            else:
                print(f"No se actualizó el usuario {user_id}.")
        else:
            print(f"Usuario {user_id} no encontrado para actualizar.")
            
    def save_image(self, user_id, face_encoding, frame):
        self.insertDocument('faces', {
            'user_id': user_id,
            'face_encoding': face_encoding.tolist(),
            'face_image': self._image_to_binary(frame),
            'timestamp': datetime.now(),
        })

    def save_user(self, user):
        self.insertDocument('users', user)
    
    def _image_to_binary(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        face_bytes = buffer.tobytes()
        return bson.Binary(face_bytes)