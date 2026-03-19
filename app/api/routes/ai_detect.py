from fastapi import APIRouter, UploadFile, File

from app.services.ai_service import detect_image

router = APIRouter()

@router.post(
    "/detect",
    summary="Detect object từ ảnh upload",
    description="""
    API dùng để nhận ảnh từ người dùng và detect object bằng AI.

    ### Input:
    - file: Ảnh (jpg, png)

    ### Output:
    - message: trạng thái xử lý
    - objects: danh sách object gồm:
        - class: id object
        - confidence: độ chính xác
        - bbox: tọa độ [x1, y1, x2, y2]

    ### Use case:
    - Upload ảnh bánh tráng → kiểm tra lỗi
    """,
)
async def detect(file: UploadFile = File(...)):
    return await detect_image(file)