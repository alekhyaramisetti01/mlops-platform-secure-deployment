from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv("secrets/.env")


class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    model_path: str = os.getenv("MODEL_PATH", "model_artifacts/fraud_model.joblib")
    api_key: str = os.getenv("API_KEY", "demo-key-for-local-dev")


def get_settings() -> Settings:
    return Settings()


def get_model_path() -> Path:
    return Path(get_settings().model_path)