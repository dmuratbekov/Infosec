import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import psutil
import platform
import logging
import logging
import sqlite3


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "requests.log")
os.makedirs(LOG_DIR, exist_ok=True)

DB_DIR = "db"
DB_PATH = os.path.join(DB_DIR, "system_history.db")
os.makedirs(DB_DIR, exist_ok=True)

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "qwerty")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s\t%(levelname)s\t%(message)s"
)

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT,
            ip TEXT,
            cpu REAL,
            ram REAL,
            disk REAL
        );
    """)
    conn.commit()
    conn.close()

init_db()


def format_bytes(n):
    for unit in ['B','KB','MB','GB','TB','PB']:
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def uptime_str():
    boot_ts = psutil.boot_time()
    boot = datetime.utcfromtimestamp(boot_ts)
    delta = datetime.utcnow() - boot
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if not parts: parts.append("0m")
    return " ".join(parts)


def collect_system_info():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count(logical=True) or 1

    vm = psutil.virtual_memory()
    ram_total = vm.total
    ram_used = vm.used
    ram_percent = vm.percent

    disk_path = "/" if os.name != 'nt' else "C:\\"
    du = None
    try:
        du = psutil.disk_usage(disk_path)
    except Exception:
        for part in psutil.disk_partitions(all=False):
            try:
                du = psutil.disk_usage(part.mountpoint)
                break
            except Exception:
                continue
    if du is None:
        raise RuntimeError("Failed to determine disk usage for any partition")
    
    disk_total = du.total
    disk_used = du.used
    disk_percent = du.percent

    users = []
    try:
        users_info = psutil.users()
        users = list({getattr(u, 'name', str(u)) for u in users_info})
    except Exception:
        pass

    plat = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

    data = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "platform": plat,
        "cpu": {
            "usage_percent": cpu_percent,
            "logical_cores": cpu_count
        },
        "memory": {
            "total": ram_total,
            "used": ram_used,
            "usage_percent": ram_percent,
            "total_human": format_bytes(ram_total),
            "used_human": format_bytes(ram_used)
        },
        "disk": {
            "total": disk_total,
            "used": disk_used,
            "usage_percent": disk_percent,
            "total_human": format_bytes(disk_total),
            "used_human": format_bytes(disk_used)
        },
        "uptime": uptime_str(),
        "users": users
    }
    return data


def log_request(path, remote_addr, info_summary):
    try:
        logging.info(json.dumps({
            "path": path,
            "remote_addr": remote_addr,
            "summary": info_summary
        }))
    except Exception as e:
        logging.error(f"Failed to log request: {e}")


def save_request_history(ts, ip, cpu, ram, disk):
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO requests (ts, ip, cpu, ram, disk) VALUES (?,?,?,?,?)",
            (ts, ip, cpu, ram, disk)
        )
        conn.commit()
        conn.close()
    except Exception:
        logging.exception("Failed to write history to DB")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/system", methods=["GET"])
def system_info():
    data = collect_system_info()
    summary = {
        "cpu": data["cpu"]["usage_percent"],
        "ram": data["memory"]["usage_percent"],
        "disk": data["disk"]["usage_percent"]
    }
    log_request("/system", request.remote_addr, summary)

    try:
        save_request_history(data["timestamp_utc"], request.remote_addr,
                             data["cpu"]["usage_percent"], data["memory"]["usage_percent"],
                             data["disk"]["usage_percent"])
    except Exception:
        logging.exception("Failed to save history (continuing)")

    return jsonify(data), 200


@app.route("/cpu", methods=["GET"])
def cpu_only():
    cpu = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "usage_percent": psutil.cpu_percent(interval=0.5),
        "logical_cores": psutil.cpu_count(logical=True)
    }
    log_request("/cpu", request.remote_addr, {"cpu": cpu["usage_percent"]})
    return jsonify(cpu), 200


@app.route("/memory", methods=["GET"])
def memory_only():
    vm = psutil.virtual_memory()
    resp = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "total": vm.total,
        "used": vm.used,
        "usage_percent": vm.percent,
        "total_human": format_bytes(vm.total),
        "used_human": format_bytes(vm.used)
    }
    log_request("/memory", request.remote_addr, {"ram": resp["usage_percent"]})
    return jsonify(resp), 200


@app.route("/disk", methods=["GET"])
def disk_only():
    try:
        du = psutil.disk_usage("/")
    except Exception:
        du = psutil.disk_usage("C:\\") if os.name == 'nt' else psutil.disk_usage("/")
    resp = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "total": du.total,
        "used": du.used,
        "usage_percent": du.percent,
        "total_human": format_bytes(du.total),
        "used_human": format_bytes(du.used)
    }
    log_request("/disk", request.remote_addr, {"disk": resp["usage_percent"]})
    return jsonify(resp), 200


@app.route("/logs", methods=["GET"])
def view_logs():
    key = request.headers.get("X-API-KEY", "")
    if key != ADMIN_API_KEY:
        return jsonify({"error": "unauthorized", "message": "provide correct X-API-KEY header"}), 401
    
    try:
        limit = int(request.args.get("limit", "100"))
    except Exception:
        limit = 100
    
    conn = get_db_connection()
    cur = conn.execute("SELECT id, ts, ip, cpu, ram, disk FROM requests ORDER BY id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    records = [dict(r) for r in rows]
    return jsonify({"count": len(records), "records": records}), 200


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "System Report API",
        "endpoints": ["/health", "/system", "/cpu", "/memory", "/disk", "/logs"]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
