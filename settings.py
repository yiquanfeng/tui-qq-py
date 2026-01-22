from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    http_url: str = "http://localhost:3001/"
    ws_url: str = "ws://10.29.237.29:3001/"
    token: str = "G4z=DTM$3G<Xorc="
    debug_mode: bool = False

settings = Settings()