from fastapi import APIRouter, HTTPException

from app.schemas.audio_schema import (YoutubeAudioRequest, YoutubeAudioResponese)
from app.utils.media_processor import download_youtube_audio

router = APIRouter(prefix="/audio", tags=['Audio'])

@router.post("/download", response_model=YoutubeAudioResponese)
def download_audio(request: YoutubeAudioRequest):
    try: 
        file_path = download_youtube_audio(str(request.url))

        return YoutubeAudioResponese(
            message="Audio downloaded successfully",
            file_path=file_path
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Audio download failed: {exc}"
        ) from exc