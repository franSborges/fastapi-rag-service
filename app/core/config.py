import os
from pydantic import BaseModel

class Settings(BaseModel):
    environment: str = "local"
    free_mode: bool = True
    port: int = 8000

settings = Settings()