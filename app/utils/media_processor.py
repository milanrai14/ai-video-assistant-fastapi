import os 
import yt_dlp
from pydub import AudioSegment
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storages"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
