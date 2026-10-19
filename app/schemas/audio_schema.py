from pydantic import BaseModel, Field, HttpUrl

class YoutubeAudioRequest(BaseModel):
    url: HttpUrl

class YoutubeAudioResponese(BaseModel):
    message: str
    filename: str
    file_path: str