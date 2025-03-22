import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from src.utils import load_pdf, split_documents, create_vector_db
load_dotenv()

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



