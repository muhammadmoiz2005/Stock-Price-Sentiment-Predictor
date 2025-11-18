import csv, os
from datetime import datetime

LOG_FILE = os.path.join('logs', 'system_logs.csv')
os.makedirs('logs', exist_ok=True)
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','event_type','message'])

def log_event(event_type: str, message: str):
    ts = datetime.utcnow().isoformat()
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([ts, event_type, message])
