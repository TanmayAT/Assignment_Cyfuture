# dummy_data_push.py
import random
from connector import MongoConnector  # Make sure your connector.py is in same dir

def generate_dummy_complaints(num=100):
    names = ["Amit", "Priya", "Raj", "Neha", "Deepak", "Sneha", "Rohit", "Anjali", "Manish", "Kiran"]
    issues = [
        "Internet not working", "Frequent disconnection", "Wrong billing", "Slow connection",
        "Router malfunction", "App not loading", "SMS not delivered", "Unable to recharge"
    ]

    complaints = []

    for _ in range(num):
        name = random.choice(names)
        phone_number = f"+91-{random.randint(6000000000, 9999999999)}"
        email = f"{name.lower()}{random.randint(100,999)}@example.com"
        complaint_details = random.choice(issues)

        complaints.append((name, phone_number, email, complaint_details))

    return complaints


def push_dummy_complaints():
    mongo = MongoConnector("mongodb+srv://vaidikpandeytt:JJEmTHNTyFgGPnjq@communicationdb.4zlwhdh.mongodb.net/?retryWrites=true&w=majority&appName=Communicationdb")

    dummy_data = generate_dummy_complaints(2000)
    count = 0
    for name, phone, email, detail in dummy_data:
        mongo.create_complaint(name, phone, email, detail)
        count += 1

    print(f"✅ Successfully inserted {count} dummy complaints.")


if __name__ == "__main__":
    push_dummy_complaints()
