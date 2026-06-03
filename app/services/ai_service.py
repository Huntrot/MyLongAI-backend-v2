import os
import gc
import asyncio
import time
import base64

import numpy as np
import cv2
from ultralytics import YOLO
from fastapi import HTTPException

from app.core.config import settings

# ==============================
# FIX Ultralytics temp directory
# ==============================
os.environ["YOLO_CONFIG_DIR"] = "/tmp/yolo"

# ==============================
# LOAD MODEL 1 LẦN DUY NHẤT
# ==============================
model = YOLO(settings.DETECT_MODEL_PATH)

# warmup (giảm lag lần đầu)
model(np.zeros((320, 320, 3), dtype=np.uint8))

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

    # ⚠️ QUAN TRỌNG: clear memory
    del results
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