from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    http_url: str = "http://localhost:3001/"
    ws_url: str = "ws://localhost:3001/"
    token: str = "110119"
    header: dict = {
        "Authorization": f"{token}"
    }

settings = Settings()