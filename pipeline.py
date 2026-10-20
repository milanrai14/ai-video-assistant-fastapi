from app.utils.media_processor import  prepare_audio_chunks
from app.core.transcriber import transcribe_all
from app.core.meetings_extractor import extract_action_items, extract_key_decision, extract_open_questions
from app.core.transcript_summarizer import summarize_transcript, generate_transcript_title
from app.core.rag_engine import build_transcript_rag_chain

def run_pipeline(source: str):
    print("Starting AI Video Assistant")
    chunks = prepare_audio_chunks(source)

    transcript = transcribe_all(chunks)
    title = generate_transcript_title(transcript)
    summary = summarize_transcript(transcript)
    action_items = extract_action_items(transcript)
    decisions = extract_key_decision(transcript)
    questions = extract_open_questions(transcript)

    rag_chain = build_transcript_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }