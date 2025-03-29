import os
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from src import utils
load_dotenv()

import json

api_key = os.getenv("OPENAI_KEY")
# Load JSON from a file
with open("prompt.json", "r") as file:
    data = json.load(file)

system_message = data.get("currentSystemPrompt", "You are an assistant.")

print(system_message)
messages = [
    ("system", system_message),
    ("human", "Use the following pieces of retrieved context & chat history to answer the question. \n\
    chat history: {chat_history} \n\
    Context: {context} \n \
    Question: {question} \n\
    Answer:")
]

prompt = ChatPromptTemplate.from_messages(messages)
print(f"====== Prompt: {prompt}")

embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
db = utils.create_vector_db(embeddings_model=embeddings_model)
llm = OpenAI(openai_api_key=os.getenv("OPENAI_KEY"))

def retreive_context(user_question):
    print(f"===user question=== : {user_question}")
    docs = db.similarity_search(user_question)
    # docs = [doc.page_content for doc in docs]
    return docs


def format_docs(docs):
    return docs[0].page_content


rag_chain = (
    {
        "context": RunnableLambda(lambda x: retreive_context(x['question'])) | format_docs, 
        "chat_history":RunnableLambda(lambda x: x['chat_history']),
        "question": RunnableLambda(lambda x: x['question'])
     }

    | prompt
    | llm
    | StrOutputParser()
)

# rag_chain.invoke("Which topics are covered in the book?")
