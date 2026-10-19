import os 
import yt_dlp
from pydub import AudioSegment
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storages"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def download_youtube_audio(url):
    output_path = os.path.join(STORAGE_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = (
            ydl.prepare_filename(info)
            .replace(".webm", ".wav")
            .replace(".m4a", ".wav")
        )

    return filename       

def prepare_audio_for_transcription(input_path):
    audio = AudioSegment.from_file(input_path)
    audio =audio.set_channels(1).set_frame_rate(16000)

    output_path = os.path.splitext(input_path)[0]+ "_converted.wav"
    audio.export(output_path, fromat="wav")
    return output_path