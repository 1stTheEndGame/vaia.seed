import time, json, pathlib

LOG_FILE = pathlib.Path("/data/memory_log.json")

def log_event(event):
    events = []
    if LOG_FILE.exists():
        events = json.loads(LOG_FILE.read_text("utf-8"))
    events.append({"timestamp": time.time(), "event": event})
    LOG_FILE.write_text(json.dumps(events, indent=2), encoding="utf-8")

if __name__ == "__main__":
    while True:
        log_event("heartbeat")
        print("Memory log heartbeat")
        time.sleep(10)
