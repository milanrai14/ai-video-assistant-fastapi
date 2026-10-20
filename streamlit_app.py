import streamlit as st
from app.utils.media_processor import  prepare_audio_chunks
from app.core.transcriber import transcribe_all
from app.core.meetings_extractor import extract_action_items, extract_key_decision, extract_open_questions
from app.core.transcript_summarizer import summarize_transcript, generate_transcript_title
from app.core.rag_engine import build_transcript_rag_chain, answer_transcript_question
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 AI Video Assistant")
st.caption(
    "Summarize videos, extract insights, and ask questions "
    "using the video transcript."
)


# Store processed results and chat history in the session.
if "video_result" not in st.session_state:
    st.session_state.video_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Sidebar: video input
with st.sidebar:
    st.header("Video Source")

    source = st.text_input(
        "YouTube URL or local audio/video path",
        placeholder="Paste a YouTube URL...",
    )

    process_button = st.button(
        "Process Video",
        type="primary",
        use_container_width=True,
    )

    st.divider()
    st.caption("The assistant answers questions from the transcript.")


# Process the submitted video
if process_button:
    if not source.strip():
        st.warning("Please enter a YouTube URL or file path.")
    else:
        try:
            with st.spinner("Processing video. This may take a while..."):
                chunks = prepare_audio_chunks(source.strip())
                transcript = transcribe_all(chunks)

                title = generate_transcript_title(transcript)
                summary = summarize_transcript(transcript)

                action_items = extract_action_items(transcript)
                decisions = extract_key_decision(transcript)
                questions = extract_open_questions(transcript)

                rag_chain = build_transcript_rag_chain(transcript)

                st.session_state.video_result = {
                    "title": title,
                    "transcript": transcript,
                    "summary": summary,
                    "action_items": action_items,
                    "key_decisions": decisions,
                    "open_questions": questions,
                    "rag_chain": rag_chain,
                }

                # Clear the old conversation for the new video.
                st.session_state.chat_history = []

            st.success("Video processed successfully!")

        except Exception as exc:
            st.error(f"Video processing failed: {exc}")


# Display results and chat after processing
result = st.session_state.video_result

if result:
    st.header(result["title"])

    summary_tab, transcript_tab, insights_tab = st.tabs(
        ["📝 Summary", "📄 Transcript", "💡 Insights"]
    )

    with summary_tab:
        st.subheader("Video Summary")
        st.write(result["summary"])

    with transcript_tab:
        st.subheader("Full Transcript")
        st.text_area(
            "Transcript text",
            value=result["transcript"],
            height=350,
            disabled=True,
        )

    with insights_tab:
        st.subheader("Action Items")
        st.write(result["action_items"])

        st.subheader("Key Decisions")
        st.write(result["key_decisions"])

        st.subheader("Open Questions")
        st.write(result["open_questions"])

    st.divider()

    # Transcript-based RAG chat
    st.header("💬 Chat with Your Video")
    st.caption(
        "Ask questions about the video. Answers are generated "
        "using the retrieved transcript context."
    )

    # Render previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Question input
    question = st.chat_input(
        "Ask a question about this video..."
    )

    if question:
        st.session_state.chat_history.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the transcript..."):
                try:
                    answer = answer_transcript_question(
                        result["rag_chain"],
                        question,
                    )
                    st.markdown(answer)

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": answer,
                        }
                    )

                except Exception as exc:
                    st.error(f"Could not answer the question: {exc}")

else:
    st.info(
        "Enter a YouTube URL or local media path in the sidebar "
        "and click Process Video to get started."
    )
