from fastapi import FastAPI
from app.api.routes.audio_route import router as audio_router



app = FastAPI(
    title="AI Video Assistant",
    description="API for audio processing and video assistance",
    version="1.0.0"
)

@app.get("/")
def root():
    return{
        "message": "AI Video Assistant API is running"
    }

app.include_router(audio_router)
