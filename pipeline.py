from app.utils.media_processor import  prepare_audio_chunks
from app.core.transcriber import transcribe_all
from app.core.meetings_extractor import extract_action_items, extract_key_decision, extract_open_questions

from app.core.transcript_summarizer import summarize_transcript, generate_transcript_title

source = "https://www.youtube.com/watch?v=YGgNBcIgI4s"