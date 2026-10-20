
from fastapi import APIRouter, HTTPException

from app.schemas.video_schema import VideoRequest
from pipeline import run_pipeline

router = APIRouter(
    prefix="/video",
    tags=["Video Assistant"],
)


@router.post("/process")
def process_video(request: VideoRequest):
    try:
        result = run_pipeline(
            source=request.source,
            language=request.language,
        )

        # The RAG chain is a Python object, not JSON-serializable.
        result.pop("rag_chain", None)

        return {
            "success": True,
            "data": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Video processing failed: {str(exc)}",
        ) from exc
