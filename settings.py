from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    http_url: str = "http://10.29.237.29:3001/"
    ws_url: str = "ws://10.29.237.29:3000/"

settings = Settings()