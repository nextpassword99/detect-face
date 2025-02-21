from app.database.Database import Database
from typing import Dict, Any, Optional
import bson
from datetime import datetime
import numpy as np

class Storage (Database):
    def save_face(self, user_id: str, face_encoding: list, face_image_binary: bytes) -> str:
        face_encoding_list = face_encoding.tolist() if isinstance(
            face_encoding, np.ndarray) else face_encoding

        face_document = {
            "user_id": user_id,
            "face_encoding": face_encoding_list,
            "face_image": bson.Binary(face_image_binary),
            "timestamp": datetime.now()
        }

        return self.insertDocument("faces", face_document)
    
    def get_user_by_face_encoding(self, face_encoding: list) -> Optional[Dict[str, Any]]:
        return self.findDocument("faces", {"face_encoding": face_encoding})

    def get_all_users(self):
        return list(self.db["faces"].find())
