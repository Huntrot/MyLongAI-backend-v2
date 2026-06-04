from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MyLongAI"
    DEBUG: bool = True
    #MODEL_PATH: str = "app/models/my_model.pt"
    DETECT_MODEL_PATH: str = "app/models/detect_model.pt"
    DRYING_MODEL_PATH: str = "app/models/drying_model.pkl"
    MAX_IMAGE_SIZE: int = 2 * 1024 * 1024  # 2MB

settings = Settings()