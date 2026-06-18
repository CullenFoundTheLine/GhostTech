# pipeline.py
from fastapi import FastAPI
from models import TelemetryFrame
from database import SessionLocal, TelemetryFrameDB, init_db

app = FastAPI(
    title="Ghost AI",
    description="Telemetry analysis pipeline for sim racing",
    version="0.1.0"
)

init_db()  # creates the table if it's missing


class Pipeline:
    def __init__(self):
        self.frames = []

    def add_frame(self, frame: TelemetryFrame):
        self.frames.append(frame)
        self._save_to_db(frame)

    def _save_to_db(self, frame: TelemetryFrame):
        db = SessionLocal()
        try:
            row = TelemetryFrameDB(**frame.model_dump())
            db.add(row)
            db.commit()
        finally:
            db.close()


pipeline = Pipeline()


@app.get("/")
def home():
    return {"status": "Ghost AI running"}


@app.post("/telemetry")
def receive_frame(frame: TelemetryFrame):
    pipeline.add_frame(frame)
    return {
        "received": True,
        "total_frames": len(pipeline.frames)
    }