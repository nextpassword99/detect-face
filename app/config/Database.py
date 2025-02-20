from pymongo import MongoClient
from typing import Dict, Any, Optional


class Database:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "pictures"):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self._connect()
