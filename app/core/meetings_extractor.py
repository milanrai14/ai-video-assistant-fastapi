import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


def get_llm():
    llm = ChatOllama(
        model="llama3.2", 
        temperature=0.4
    )
    return llm

def get_parser():
    parser = StrOutputParser()
    return parser

def build_extraction_chain(system_prompt: str):
    llm = get_llm()
    passthrough = RunnablePassthrough()
    format_input = RunnableLambda( #format input is neccessary because ChatPromptTemplate expects dictionary containg a key named "text"
        lambda x : {"text":x}
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt), 
        ("human", "{text}")
    ])

    parser = get_parser()

    chain = (
        passthrough
        | format_input
        | prompt
        | llm
        | parser
    )

    return chain

def extract_action_items(transcript: str)->str:
    system_prompt = """
    You are an expert meetings analyst. From the meeting transcript,
    extract all action items. For each action item, provide:

    - Task description
    - Owner (who is responsible)
    - Deadline (if mentioned, otherwise write "Not specified")

    Format the results as a numbered list.
    If no action items are found, say "No action items found".
    """

    chain = build_extraction_chain(system_prompt)
    return chain.invoke(transcript)

def extract_key_decision(transcript: str) -> str: 
    system_prompt = """
    You are an expert meetings analyst. From the meeting transcript,
    extract all key decisions made.

    Format the results as a numbered list.
    If no key decisions are found, say "No key decisions found."
    """

    chain = build_extraction_chain(system_prompt)

    return chain.invoke(transcript)

def extract_open_questions(transcript: str) -> str:
    system_prompt = """
    From the meeting transcript, extract all unresolved questions
    or topics requiring follow-up.

    Format the results as a numbered list.
    If none are found, say "No open questions found."
    """
    chain = build_extraction_chain(system_prompt)

    return chain.invoke(transcript)