#!/usr/bin/env python3
"""
Seed.VAIA bootstrapper
"""
import subprocess, json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
def load(p): return json.load(open(p, "r", encoding="utf-8"))
def run(cmd): subprocess.check_call(cmd, cwd=ROOT)
def main():
    print("Loaded doctrine:", load(ROOT / "core" / "doctrine.json")["mission"])
    run(["docker", "compose", "up", "-d"])
if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(0)