from fastapi import APIRouter, HTTPException

from app.schemas.audio_schema import (YoutubeAudioRequest, YoutubeAudioResponese, PrepareAudioRequest, PrepareAudioResponse)
from app.utils.media_processor import download_youtube_audio, prepare_audio_for_transcription

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

@router.post("/prepare", response_model=PrepareAudioResponse)
def download_and_prepare_audio(request: YoutubeAudioRequest):
    try:
        download_path = download_youtube_audio(str(request.url))
        output_path = prepare_audio_for_transcription(download_path)

        return PrepareAudioResponse(
            message="Audio prepared successfully for transcription",
            output_path=output_path,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Audio processing failed: {str(exc)}",
        )

    