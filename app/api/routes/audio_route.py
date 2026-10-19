from fastapi import APIRouter, HTTPException

from app.schemas.audio_schema import (YoutubeAudioRequest, YoutubeAudioResponese, PrepareAudioRequest, PrepareAudioResponse, ProcessAudioResponse, ProcessAudioRequest)
from app.utils.media_processor import download_youtube_audio, prepare_audio_for_transcription, prepare_audio_chunks

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


@router.post("/process",response_model=ProcessAudioResponse)
def process_audio(request: ProcessAudioRequest):
    try: 
        chunks = prepare_audio_chunks(request.source)
        return ProcessAudioResponse(
            message= "Audio processed and chunked successfully", 
            chunks=chunks,
            total_chunks=len(chunks)
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Audio processing failed: {exc}",
        ) from exc