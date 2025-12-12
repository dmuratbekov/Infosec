# System Report API

System Report API is a small educational service written in Python + Flask that collects current system information (CPU, RAM, disk, uptime, users) and returns it in JSON format. The project also stores request history in SQLite and provides a secure endpoint `/logs` for viewing history.

--- 

## Features

### System Information Endpoints
The API exposes real-time machine statistics such as:
- CPU usage (%)
- RAM usage (%)
- Total / available memory
- Disk space usage
- System uptime
- Boot time
- Logged-in users
- Running processes
- Python environment info
- Timestamp in UTC

--- 

## Project Structure
```
system_report_api/
├── app.py                          # Main Flask application
│
├── db/
│ └── system_history.db             # SQLite database
│
├── logs/
│ └── requests.log                  # Log file created automatically
│
├── requirements.txt 
│
└── README.md
```

---

## Logging
Every request is logged into:
```
log/srequests.log
```
including:
- timestamp
- endpoint accessed
- client IP
- HTTP method
- response status

---

## Postman Demonstration

The project is fully compatible with Postman.

You can test:
- /system
- /cpu
- /memory
- /disk
- /health
- /logs

---

## Technologies Used

- Python 3.12
- Flask
- psutil
- logging module
- datetime
- JSON formatting

---

# API Documentation

## GET /
Displays:
```json
{
    "endpoints": [
        "/health",
        "/system",
        "/cpu",
        "/memory",
        "/disk",
        "/logs"
    ],
    "service": "System Report API"
}
```


## GET /system
Returns complete system summary.

Response Example:
```json
{
    "cpu": {
        "logical_cores": 4,
        "usage_percent": 0.0
    },
    "disk": {
        "total": 1081101176832,
        "total_human": "1006.85 GB",
        "usage_percent": 0.3,
        "used": 2655764480,
        "used_human": "2.47 GB"
    },
    "memory": {
        "total": 4057190400,
        "total_human": "3.78 GB",
        "usage_percent": 12.8,
        "used": 517316608,
        "used_human": "493.35 MB"
    },
    "platform": {
        "machine": "x86_64",
        "node": "linux",
        "processor": "x86_64",
        "release": "WSL2",
        "system": "Linux",
        "version": "#1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025"
    },
    "timestamp_utc": "2025-12-12T08:36:29.239188Z",
    "uptime": "10h 47m",
    "users": [
        "dan"
    ]
}
```

## GET /cpu
Returns CPU information.

Response Example:
```json
{
    "logical_cores": 4,
    "timestamp_utc": "2025-12-12T10:19:25.664935Z",
    "usage_percent": 1.0
}
```

## GET /disk
Returns disk information.

Response Example:
```json
{
    "timestamp_utc": "2025-12-12T10:19:33.163947Z",
    "total": 1081101176832,
    "total_human": "1006.85 GB",
    "usage_percent": 0.3,
    "used": 2655924224,
    "used_human": "2.47 GB"
}
```

## GET /memory
Returns memory information.

Response Example:
```json
{
    "timestamp_utc": "2025-12-12T10:19:43.091397Z",
    "total": 4057190400,
    "total_human": "3.78 GB",
    "usage_percent": 12.3,
    "used": 497418240,
    "used_human": "474.38 MB"
}
```

## GET /health
Service health check.

Response Example:
```json
{
    "status": "ok"
}
```

## GET /logs
Shows the history of GET /system requests

### Access to the /logs endpoint
The endpoint /logs is protected by a simple API key.
To gain access, you need to add a header to the request:
```
X-API-KEY: your_secret_key_here

```
If the key is not transmitted or is incorrect, the server will return a 401 Unauthorized error.

Response Example:
```json
{
    "count": 2,
    "records": [
        {
            "cpu": 0.5,
            "disk": 0.3,
            "id": 2,
            "ip": "172.21.160.1",
            "ram": 12.5,
            "ts": "2025-12-12T10:19:18.227433Z"
        },
        {
            "cpu": 0.0,
            "disk": 0.3,
            "id": 1,
            "ip": "172.21.160.1",
            "ram": 12.8,
            "ts": "2025-12-12T08:36:29.239188Z"
        }
    ]
}
```

---

# How to Run the Project

## Step 1 — Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

## Step 2 — Install dependencies
```
pip install -r requirements.txt
```

## Step 3 — Start the server
```
python app.py

```
API available at:
```
http://127.0.0.1:5000    

```

---

## Postman Usage
Examples:
```
GET http://localhost:5000/system
GET http://localhost:5000/cpu
GET http://localhost:5000/disk
GET http://localhost:5000/logs
```

---

# Video Demonstration

https://drive.google.com/file/d/1viwZtHaSinJePZU68k49MfRIq01PF6wb/view?usp=sharing

---
