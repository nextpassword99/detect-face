from pymongo import MongoClient
from typing import Dict, Any, Optional


class Database:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "pictures"):
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

