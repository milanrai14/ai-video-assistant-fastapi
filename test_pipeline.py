from app.utils.media_processor import  prepare_audio_chunks
from app.core.transcriber import transcribe_all
from app.core.meetings_extractor import extract_action_items, extract_key_decision, extract_open_questions

from app.core.transcript_summarizer import summarize_transcript, generate_transcript_title

source = "https://www.youtube.com/watch?v=YGgNBcIgI4s"

chunks = prepare_audio_chunks(source)
transcript = transcribe_all(chunks)
print("\n" + "=" * 60)
print("TRANSCRIPT")
print("=" * 60)
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)

title = generate_transcript_title(transcript)
summary = summarize_transcript(transcript)

print("\n" + "=" * 60)
print(f"TITLE: {title}")
print("=" * 60)
print("\nSUMMARY")
print("-" * 60)
print(summary)

action_items = extract_action_items(transcript)
decisions = extract_key_decision(transcript)
questions = extract_open_questions(transcript)

print("\n" + "=" * 60)
print("ACTION ITEMS")
print("=" * 60)
print(action_items)

print("\n" + "=" * 60)
print("KEY DECISIONS")
print("=" * 60)
print(decisions)

print("\n" + "=" * 60)
print("OPEN QUESTIONS")
print("=" * 60)
print(questions)