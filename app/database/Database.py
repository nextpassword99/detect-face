from pymongo import MongoClient
from typing import Dict, Any, Optional
import bson
from datetime import datetime
import numpy as np


class Database:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "faces"):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self._connect()

    def _connect(self):
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]

    def insertDocument(self, collector_name: str, document: Dict[str, Any]) -> str:
        collection = self.db[collector_name]
        result = collection.insert_one(document)

        return str(result.inserted_id)

    def findDocument(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        collection = self.db[collection_name]
        document = collection.find_one(query)

        return document

    def updateDocument(self, collection_name: str, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": new_values})

        return result.modified_count

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
