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