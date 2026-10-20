
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from app.core.vector_store import (
    build_vector_store,
    load_vector,
    get_retriver,
)


def get_llm():
    return ChatOllama(
        model="llama3.2",
        temperature=0.3,
    )


def format_retrieved_documents(docs) -> str:
    return "\n\n".join(
        document.page_content
        for document in docs
    )


def create_rag_prompt():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            """You are an expert transcript assistant.

Answer the user's question using only the transcript
information provided in the context.

Rules:
1. Use only information from the transcript.
2. If the answer is missing, say:
   "I could not find this information in the transcript."
3. Be concise, clear, and precise.
4. Identify speakers when possible.
5. Never invent information.

Transcript context:
{context}"""
        ),
        ("human", "{question}"),
    ])


def create_rag_pipeline(retriever):
    llm = get_llm()
    prompt = create_rag_prompt()
    output_parser = StrOutputParser()

    context_chain = (
        retriever
        | RunnableLambda(format_retrieved_documents)
    )

    rag_chain = (
        {
            "context": context_chain,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | output_parser
    )

    return rag_chain


def build_transcript_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)

    retriever = get_retriver(
        vector_store,
        k=4,
    )

    return create_rag_pipeline(retriever)


def load_transcript_rag_chain():
    vector_store = load_vector()

    retriever = get_retriver(
        vector_store,
        k=4,
    )

    return create_rag_pipeline(retriever)


def answer_transcript_question(rag_chain, question: str) -> str:
    print(f"Question: {question}")

    answer = rag_chain.invoke(question)

    print(f"Answer: {answer}")

    return answer
