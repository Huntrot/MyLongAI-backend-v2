from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MyLongAI"
    DEBUG: bool = True
    MODEL_PATH: str = "app/models/my_model.pt"

settings = Settings()