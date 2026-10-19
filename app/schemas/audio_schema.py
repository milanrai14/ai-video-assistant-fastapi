from pydantic import BaseModel, Field, HttpUrl

class YoutubeAudioRequest(BaseModel):
    url: HttpUrl

class YoutubeAudioResponese(BaseModel):
    message: str
    filename: str
    file_path: str

class PrepareAudioRequest(BaseModel):
    input_path: str = Field(..., description="Path to the existing audio or video files")

class PrepareAudioResponse(BaseModel): 
    message: str
    output_path: str