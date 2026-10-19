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

def transcribe_chunk(chunk_path : str, translate: bool = False)-> str:
    model = load_model()
    task = "translate" if translate else "transcribe"

    result = model.transcribe(chunk_path, task=task)

    return result['text']

def transcribe_all(chunks, translate=False):
    transcripts = []

    for i, chunk_path in enumerate(chunks, start=1):
        print(f"Transcribing chunk {i}: {chunk_path}")

        text = transcribe_chunk(
            chunk_path,
            translate=translate
        )

        transcripts.append(text)

    return "\n".join(transcripts)