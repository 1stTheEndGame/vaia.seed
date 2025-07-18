from fastapi import FastAPI, HTTPException
import json, pathlib

app = FastAPI()
ROOT = pathlib.Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "core" / "registry.json"

@app.get("/heartbeat")
def heartbeat():
    return {"status": "alive"}

@app.get("/registry")
def read_registry():
    if not REGISTRY.exists():
        raise HTTPException(404, "Registry not found")
    return json.loads(REGISTRY.read_text("utf-8"))
