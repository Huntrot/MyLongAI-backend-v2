from ultralytics import YOLO
import numpy as np
import cv2
from app.core.config import settings
from fastapi import HTTPException

# Load model 1 lần
model = YOLO(settings.MODEL_PATH)
model(np.zeros((320, 320, 3), dtype=np.uint8))

def process_frame(img):
    
    img = cv2.resize(img, (320, 320))

    results = model(img, imgsz=320, conf=0.5, device="cpu")

    detections = []

    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist()
            })

    return detections


async def detect_image(file):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="File không phải ảnh hợp lệ hoặc không có bánh tráng")
    
    detections = process_frame(img)

    return {
        "message": "AI processed successfully",
        "objects": detections
    }