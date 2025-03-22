import os
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()


from src.utils import retreive_db

api_key = os.getenv("OPENAI_KEY")

messages = [
    ("system", "You are an assistant. You are given a question and a context. You need to answer the question based on the context.\
     If the context is not relevant to the question, then give me answer from your knowledge."),
    ("human", "Use the following pieces of retrieved context to answer the question. \n\
    If the retrieved context is not relevant to the question, then give me answer by yourself.\n\
    Context: {context} \n \
    Question: {question} \n\
    Answer:")
]

prompt = ChatPromptTemplate.from_messages(messages)

db = retreive_db()
llm = OpenAI(openai_api_key=os.getenv("OPENAI_KEY"))

def retreive_context(user_question):
    docs = db.similarity_search(user_question)
    # docs = [doc.page_content for doc in docs]
    return docs


def format_docs(docs):
    return docs[0].page_content


rag_chain = (
    {"context": RunnableLambda(lambda x: retreive_context(x)) | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("Which topics are covered in the book?")
