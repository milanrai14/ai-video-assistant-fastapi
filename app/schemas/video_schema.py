
from pydantic import BaseModel, Field


class VideoRequest(BaseModel):
    source: str = Field(
        ...,
        min_length=1,
        description="YouTube URL or local audio/video file path",
    )
    language: str = Field(
        default="english",
        description="Transcription language: english or hinglish",
    )
