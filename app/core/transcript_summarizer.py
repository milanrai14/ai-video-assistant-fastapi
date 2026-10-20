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