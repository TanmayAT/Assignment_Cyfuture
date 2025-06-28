from pymongo import MongoClient
from datetime import datetime
import uuid

class MongoConnector:
    def __init__(self, uri, db_name="complaintsDB"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["complaints"]

    def create_complaint(self, name, phone_number, email, complaint_details):
        complaint_id = str(uuid.uuid4())[:8]
        complaint_doc = {
            "complaint_id": complaint_id,
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "complaint_details": complaint_details,
            "created_at": datetime.utcnow()
        }
        self.collection.insert_one(complaint_doc)
        return {
            "complaint_id": complaint_id,
            "message": "Complaint created successfully"
        }

    def get_complaint_by_id(self, complaint_id):
        result = self.collection.find_one({"complaint_id": complaint_id}, {"_id": 0})
        if not result:
            return {"error": "Complaint ID not found"}
        return result


