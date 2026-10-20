import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_llm():
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.4
    )
    return llm

def get_parser():
    parser = StrOutputParser()
    return parser

def chunk_transcript(transcript: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )
    chunks = splitter.split_text(transcript)
    return chunks

def summarize_transcript(transcript: str) -> str:
    llm = get_llm()
    parser = get_parser()

    map_prompt = ChatPromptTemplate.from_messages([
        ("system", "Summarize this portion of a transcript concisely."),
        ("human", "{text}")
    ])

    map_chain = map_prompt | llm | parser

    chunks = chunk_transcript(transcript)

    chunk_summaries = [
        map_chain.invoke({"text": chunk})
        for chunk in chunks
    ]

    combined = "\n\n".join(chunk_summaries)

    combined_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Combine these partial summaries into one professional "
            "final summary using bullet points."
        ),
        ("human", "{text}"),
    ])

    combined_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | combined_prompt
        | llm
        | parser
    )

    return combined_chain.invoke(combined)
