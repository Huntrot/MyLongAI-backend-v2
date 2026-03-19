from fastapi import APIRouter
from pydantic import BaseModel
import base64
import numpy as np
import cv2

from app.services.ai_service import process_frame

router = APIRouter()


class FrameRequest(BaseModel):
    image: str  # base64 string


@router.post("/detect-realtime")
async def detect_realtime(req: FrameRequest):
    try:
        # decode base64 → image
        img_data = base64.b64decode(req.image)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        detections = process_frame(img)

        return {
            "message": "Realtime processed",
            "objects": detections
        }

    except Exception as e:
        return {"error": str(e)}