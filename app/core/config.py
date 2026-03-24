from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MyLongAI"
    DEBUG: bool = True
    MODEL_PATH: str = "app/models/my_model.pt"
    MAX_IMAGE_SIZE: int = 2 * 1024 * 1024  # 2MB

settings = Settings()