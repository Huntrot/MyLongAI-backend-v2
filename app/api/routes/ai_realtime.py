from fastapi import APIRouter
from pydantic import BaseModel, Field
import base64
import numpy as np
import cv2

from app.services.ai_service import process_frame

router = APIRouter()


class FrameRequest(BaseModel):
    image: str = Field(
        ...,
        description="Ảnh dạng base64 từ camera frontend",
        example="iVBORw0KGgoAAAANSUhEUgAA..."
    )


@router.post(
    "/detect-realtime",
    summary="Detect object realtime từ camera",
    description="""
    API nhận ảnh dạng base64 từ camera (frontend gửi lên).

    ### Input:
    - image: string base64

    ### Output:
    - message: trạng thái xử lý
    - objects: danh sách object detect được:
        - class: id object
        - confidence: độ chính xác
        - bbox: tọa độ

    ### Flow:
    base64 → decode → numpy → YOLO → trả kết quả
    """,
)
async def detect_realtime(req: FrameRequest):
    try:
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