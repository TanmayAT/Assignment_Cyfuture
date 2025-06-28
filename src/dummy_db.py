import random
import uuid
import datetime
import json

def get_dummy_data(num_records=10):
    """
    Generate datapoints for the updates checking and complaints progress report and tracking
    """
    statuses = ['Open', 'In Progress', 'Resolved', 'Closed', 'Escalated']
    complaint_types = ['Network Issue', 'Billing Error', 'Slow Internet', 'Connection Drop', 'Hardware Fault']
    departments = ['Technical', 'Customer Service', 'Billing', 'Field Team']
    
    dummy_data = []

    for _ in range(num_records):
        record = {
            "complaint_id": str(uuid.uuid4()),
            "mobile_number": f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "name": f"User_{random.randint(1, 100)}",
            "user_id": f"user_{random.randint(1000, 9999)}",
            "complaint_type": random.choice(complaint_types),
            "status": random.choice(statuses),
            "department": random.choice(departments),
            "progress_percent": round(random.uniform(0, 100), 2),
            "last_updated": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat(),
        }
        dummy_data.append(record)

    return dummy_data

# Example usage:
if __name__ == "__main__":
    data = get_dummy_data(2000)
    print(json.dumps(data, indent=2))
