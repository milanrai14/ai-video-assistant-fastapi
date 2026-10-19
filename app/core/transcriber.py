import os
import whisper
from dotenv import load_dotenv

WISHPER_MODEL= os.getenv("WISHPER_SMALL", "small")

_model = None


def load_model(): 
    global _model

    if _model is None:
        print("loading model ...")
        _model = whisper.load_model(WISHPER_MODEL)
        print("Whisper model loaded successfully")

    return _model
