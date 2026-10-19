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


def chunk_audio(wav_path: str, chunk_minut: int) -> str:
    if chunk_minut <= 0:
        raise ValueError("Chunk minute must be greater than zero.")
    audio = AudioSegment.from_wav(wav_path)
    chunks_ms = chunk_minut * 60 * 1000

    chunks = []
    for i, start in enumerate(range(0, len(audio)), chunks_ms):
        chunk = audio[start:start+chunks_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format='wav')

        chunks.append(chunk)
    return chunks

def prepare_audio_chunks(source: str) -> list[str]:
    if source.startswith(("http://", "https://")):
        print("Detected YouTube URL. Downloading audio...")
        audio_path = download_youtube_audio(source)
    else:
        print("Detected local file.")
        audio_path = source

    print("Converting to WAV...")
    wav_path = prepare_audio_for_transcription(audio_path)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    print(f"Audio ready - {len(chunks)} chunk(s) created.")

    return chunks