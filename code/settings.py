# code/settings.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str = "Legodb"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # NUEVO
    DEBUG: bool = False                  # activa trazas en respuesta (solo temporalmente)
    LOG_LEVEL: str = "INFO"              # DEBUG, INFO, WARNING...

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
