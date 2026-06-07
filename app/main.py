from app.services.debug import log_memory
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.api.routes import ai_detect, ai_realtime, health, drying
from app.api.routes import health, drying
app = FastAPI(
    title="MyLongAI Backend",
    description="""
    Hệ thống AI Vision cho làng nghề MyLongAI
    
    Sử dụng YOLO để phân tích chất lượng sản phẩm.
    """,
    version="1.0.0"
)
    
@app.on_event("startup")
async def startup_event():
    print("=" * 50)
    log_memory("Startup")
    print("=" * 50)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ dev thì để *, production thì giới hạn domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(ai_detect.router, prefix="/ai", tags=["AI"])
# app.include_router(ai_realtime.router, prefix="/ai", tags=["AI Realtime"])
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(drying.router, prefix="/drying", tags=["Drying Prediction"])
@app.get("/")
def root():
    return {"status": "ok"}