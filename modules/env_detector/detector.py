"""Simple environment snapshotter for VAIA.
Prints CPU, memory, and disk utilisation every 10 seconds.
"""
import json, time, psutil

def snapshot():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "mem_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
    }

if __name__ == "__main__":
    while True:
        print(json.dumps(snapshot()), flush=True)
        time.sleep(10)
