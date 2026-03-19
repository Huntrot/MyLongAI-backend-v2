from fastapi import FastAPI
from app.api.routes import ai_detect, ai_realtime, health

app = FastAPI(title="MyLongAI Backend")

app.include_router(ai_detect.router, prefix="/ai", tags=["AI"])
app.include_router(ai_realtime.router, prefix="/ai", tags=["AI Realtime"])
app.include_router(health.router, prefix="/health", tags=["Health"])
