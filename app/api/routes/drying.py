from fastapi import APIRouter
from pydantic import BaseModel

from app.services.drying_service import predict_drying_time

router = APIRouter()

class DryingRequest(BaseModel):
    avg_temperature: float
    avg_humidity: float

@router.post("/predict")
def predict(request: DryingRequest):
    return predict_drying_time(
        avg_temperature=request.avg_temperature,
        avg_humidity=request.avg_humidity
    )