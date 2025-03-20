import openai
import os
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


messages = [
    ("system", "You are an assistant for question-answering tasks."),
    ("human", "Use the following pieces of retrieved context to answer the question. \n\
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. \n\
    Question: {question} \n\
    Context: {context} \n \
    Answer:")
]

prompt = ChatPromptTemplate.from_messages(messages)


texts = [doc.page_content for doc in splitted_docs]

def format_docs(docs):
    return docs[0].page_content


rag_chain = (
    {"context": RunnableLambda(lambda x: retreive_context(x)) | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("Which topics are covered in the book?")
