from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/",
    summary="Kiểm tra trạng thái server",
    description="""
    API dùng để kiểm tra backend có đang hoạt động hay không.

    ### Output:
    - status: "ok" nếu server chạy bình thường
    """
)
def health_check():
    return {"status": "ok"}