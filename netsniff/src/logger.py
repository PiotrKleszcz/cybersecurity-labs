import json
import os
from datetime import datetime
from scapy.all import wrpcap

LOG_DIR = "logs"
CAPTURE_DIR = "captures"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CAPTURE_DIR, exist_ok=True)

def save_json(records: list, filename: str = None):
    filename = filename or f"{LOG_DIR}/capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w") as f:
        json.dump(records, f, indent=2)
    print(f"[+] Saved JSON: {filename}")
    return filename

def save_pcap(packets: list, filename: str = None):
    filename = filename or f"{CAPTURE_DIR}/capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pcap"
    wrpcap(filename, packets)
    print(f"[+] Saved PCAP: {filename}")
    return filename
