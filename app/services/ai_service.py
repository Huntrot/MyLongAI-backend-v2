from ultralytics import YOLO
import numpy as np
import cv2
from app.core.config import settings
from fastapi import HTTPException

# Load model 1 lần
model = YOLO(settings.MODEL_PATH)


def process_frame(img):
    # Resize tối ưu
    img = cv2.resize(img, (640, 640))

    results = model(img)

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