import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from src.utils import load_pdf, split_documents, create_vector_db
load_dotenv()
from typing import List
from dataclasses import dataclass

def create_knowledgebase(data_path):
    try:
        documents = load_pdf(data_path)
        split_docs = split_documents(documents)
        # texts = [doc.page_content for doc in split_docs]

        embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
        create_vector_db(split_docs, embeddings_model)
        print("Vector database created successfully")
    except Exception as e:
        print(f"Error: {e}")


@dataclass
class chat_history:
    user: List[str]
    assistant: List[str]

    def create_chat_history(self, user, assistant):
        self.user.append(user)
        self.assistant.append(assistant)
    
    def get_chat_history(self):
        return (self.user[-5:], self.assistant[-5:])
    
    def __len__(self):
        return len(self.user)
    
    def all_chat_history(self):
        return (self.user, self.assistant)



