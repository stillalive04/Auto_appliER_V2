# Simple in-memory database for testing
# Replace with actual MongoDB connection in production

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class InMemoryCollection:
    def __init__(self):
        self.data = []
        self.counter = 1
    
    def insert_one(self, document: Dict[str, Any]):
        document['_id'] = str(self.counter)
        document['created_at'] = datetime.now()
        self.data.append(document)
        self.counter += 1
        return type('InsertResult', (), {'inserted_id': document['_id']})()
    
    def find_one(self, query: Optional[Dict[str, Any]] = None):
        if query is None:
            return self.data[0] if self.data else None
        
        for doc in self.data:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                return doc
        return None
    
    def find(self, query: Optional[Dict[str, Any]] = None):
        if query is None:
            return self.data
        
        results = []
        for doc in self.data:
            match = True
            for key, value in query.items():
                if key not in doc or doc[key] != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return type('Cursor', (), {'sort': lambda *args: results})()

class InMemoryDB:
    def __init__(self):
        self.applications = InMemoryCollection()

# Initialize collections
users = InMemoryCollection()
resumes = InMemoryCollection()
preferences = InMemoryCollection()
db = InMemoryDB() 