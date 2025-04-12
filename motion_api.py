from fastapi import FastAPI
from gpiozero import MotionSensor
import datetime
import threading

app = FastAPI()
pir = MotionSensor(4)
log_file = "motion_log.txt"

def detect_motion():
    while True:
        pir.wait_for_motion()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Motion detected at {timestamp}")
        with open(log_file, "a") as f:
            f.write(f"Motion detected at {timestamp}\n")
        pir.wait_for_no_motion()

threading.Thread(target=detect_motion, daemon=True).start()

@app.get("/")
def home():
    return {"status": "Running", "sensor": "PIR on GPIO4"}

@app.get("/logs")
def get_logs():
    try:
        with open(log_file) as f:
            return {"logs": f.readlines()}
    except FileNotFoundError:
        return {"logs": []}

@app.delete("/logs")
def clear_logs():
    open(log_file, 'w').close()
    return {"message": "Logs cleared"}
