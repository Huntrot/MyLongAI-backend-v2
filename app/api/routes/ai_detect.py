from fastapi import APIRouter, UploadFile, File
from app.services.ai_service import detect_image

router = APIRouter()

@router.post("/detect")
async def detect(file: UploadFile = File(...)):
    return await detect_image(file)
