from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "vaia_comm_engine online"}

@app.get("/relay/heartbeat")
def relay():
    import requests
    try:
        r = requests.get("http://vaia_core:8000/heartbeat", timeout=2)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8010)
