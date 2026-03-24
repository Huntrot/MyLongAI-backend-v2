import gc

from fastapi import APIRouter
from pydantic import BaseModel, Field
import base64
import numpy as np
import cv2

from app.services.ai_service import detect_realtime_base64, process_frame

router = APIRouter()


class FrameRequest(BaseModel):
    image: str = Field(
        ...,
        description="Ảnh dạng base64 từ camera frontend"
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
    return await detect_realtime_base64(req.image)