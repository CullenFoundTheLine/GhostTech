# receiver.py
# Connects to PS5/GT7, converts each frame, POSTs it to the running
# GhostTech FastAPI server at /telemetry.
#
# Usage:
#   1. In one terminal:  uvicorn pipeline:app --reload
#   2. In another:       export TELEMETRY_IP="10.0.0.133"
#                         python3 receiver.py
#   3. Answer the session setup questions BEFORE GT7 connects.

import os
import time
import requests
from gt_telem import TurismoClient
from models import TelemetryFrame
from session import setup

PS_IP = os.getenv("TELEMETRY_IP")
SERVER_URL = "http://127.0.0.1:8000/telemetry"

INTERVAL_MS = 100

if not PS_IP:
    print("No PS5 IP set.")
    print("Run: export TELEMETRY_IP=10.0.0.133")
    exit()

# Step 1 — capture session context BEFORE connecting to PS5.
# Every frame from this point on is tagged with this context.
session = setup()
if not session:
    exit()

last_sent = 0.0
frame_count = 0
sent_count = 0


def handle_data(t):
    global last_sent, frame_count, sent_count
    frame_count += 1

    now = time.time() * 1000
    if now - last_sent < INTERVAL_MS:
        return
    last_sent = now

    try:
        frame = TelemetryFrame.from_gt7(t, session)
    except Exception as e:
        print(f"\n[Receiver] Failed to build frame: {e}")
        return

    try:
        resp = requests.post(SERVER_URL, json=frame.model_dump(mode="json"), timeout=1)
        sent_count += 1
        print(
            f"\r  {session.track} | Lap {frame.lap} | "
            f"{frame.speed_kph:.1f} kph | "
            f"G{frame.gear} | "
            f"T:{int(frame.throttle)} B:{int(frame.brake)} | "
            f"Sent: {sent_count} | "
            f"Server total: {resp.json().get('total_frames', '?')}    ",
            end="", flush=True
        )
    except requests.exceptions.RequestException as e:
        print(f"\n[Receiver] Could not reach server: {e}")
        print("[Receiver] Is uvicorn running? Run: uvicorn pipeline:app --reload")


print(f"\n[Receiver] Connecting to PS5 at {PS_IP}...")
print(f"[Receiver] Posting to {SERVER_URL}")
print("[Receiver] Open GT7 and get into a race.\n")

try:
    client = TurismoClient(ps_ip=PS_IP)
    client.register_callback(handle_data)
    client.run()
except KeyboardInterrupt:
    print(f"\n\n[Receiver] Stopped. Frames seen: {frame_count} | Sent to server: {sent_count}")