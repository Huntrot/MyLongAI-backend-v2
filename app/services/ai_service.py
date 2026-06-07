import os
import gc
import asyncio
import time
import base64

import numpy as np
from app.services.debug import log_memory
import cv2
# from ultralytics import YOLO
from fastapi import HTTPException

from app.core.config import settings

# ==============================
# FIX Ultralytics temp directory
# ==============================
os.environ["YOLO_CONFIG_DIR"] = "/tmp/yolo"

# ==============================
# LAZY LOAD MODEL
# ==============================
model = None

def get_model():
    global model

    if model is None:

        from ultralytics import YOLO

        print("Loading YOLO model...")

        model = YOLO(settings.DETECT_MODEL_PATH)

        print("YOLO model loaded.")

        log_memory("After YOLO load")

    return model

# ==============================
# LIMIT CONCURRENCY (QUAN TRỌNG)
# ==============================
semaphore = asyncio.Semaphore(1)

# ==============================
# ANTI-SPAM realtime
# ==============================
last_call_time = 0

def allow_request(interval=3):
    global last_call_time
    now = time.time()
    if now - last_call_time < interval:
        return False
    last_call_time = now
    return True


# ==============================
# CORE AI PROCESS
# ==============================
def process_frame(img):

    log_memory("Before detect")

    model = get_model()

    img = cv2.resize(img, (320, 320))

    results = model(
        img,
        imgsz=320,
        conf=0.5,
        device="cpu",
        verbose=False
    )

    detections = []

    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    # Giải phóng từng object
    for r in results:
        del r

    del results
    del img

    gc.collect()

    log_memory("After detect")

    return detections


# ==============================
# API: detect image upload
# ==============================
async def detect_image(file):
    async with semaphore:

        contents = await file.read()

        # limit size
        if len(contents) > settings.MAX_IMAGE_SIZE:
            raise HTTPException(status_code=400, detail="Ảnh quá lớn (>2MB)")

        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        log_memory("After decode image")

        if img is None:
            raise HTTPException(status_code=400, detail="File không hợp lệ")

        detections = process_frame(img)

        # cleanup
        del img, np_arr, contents
        gc.collect()

        return {
            "message": "AI processed successfully",
            "objects": detections
        }


# ==============================
# API: realtime base64
# ==============================
async def detect_realtime_base64(image_base64: str):
    async with semaphore:

        # anti spam
        if not allow_request():
            raise HTTPException(status_code=429, detail="Too many requests")

        try:
            img_data = base64.b64decode(image_base64)
        except Exception:
            raise HTTPException(status_code=400, detail="Base64 không hợp lệ")

        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        log_memory("After decode image")

        if img is None:
            raise HTTPException(status_code=400, detail="Ảnh decode lỗi")

        detections = process_frame(img)

        # cleanup
        del img, np_arr, img_data
        gc.collect()

        return {
            "message": "Realtime processed",
            "objects": detections
        }