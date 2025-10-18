import requests
import os
import time
from datetime import datetime

SERVER_URL = "http://127.0.0.1:5000/upload"
FILE_PATH = "log.txt"

def send_file(path):
    if not os.path.exists(path):
        print("File not found", path)
        return False
    with open(path, "rb") as f:
        files = {"file": (os.path.basename(path), f)}
        try:
            resp = requests.post(SERVER_URL, files=files, timeout=10)
            print("Server", resp.status_code, resp.text)
            return resp.status_code == 200
        except Exception as e:
            print("Error", e)
            return False

if __name__ == "__main__":
    success = send_file(FILE_PATH)
    if not success:
        retries = 5
        for i in range(retries):
            print(f"Trying again {i+1}/{retries}...")
            time.sleep(5)
            if send_file(FILE_PATH):
                break
    else:
        print("Success", datetime.now().isoformat())

