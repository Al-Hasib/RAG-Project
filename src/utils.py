from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
import pandas as pd
from qdrant_client.http.models import Distance, VectorParams

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def load_csv(csv_file):
    # Load CSV
    # csv_file = "data.csv"  # Replace with your CSV file
    df = pd.read_csv(csv_file)

    # Convert CSV into text format
    docs = []
    for i, row in df.iterrows():
        text = " ".join([f"{col}: {row[col]}" for col in df.columns])  # Convert row to text
        docs.append(text)
    return docs


# Split documents into smaller chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)
    print(len(split_docs))
    return split_docs


# def retreive_context(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=api_key)
#     new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
#     docs = new_db.similarity_search(user_question)
#     print(docs)
#     return docs

def retreive_db():
    url = "http://134.122.1.211:6333"

    client = QdrantClient(
        url=url, prefer_grpc=False
    )

    collection_name = "vector_db"
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
    db = QdrantVectorStore(client=client, embedding=embeddings_model, collection_name="vector_db")
    # docs = db.similarity_search(user_question)
    # print(docs)
    # return docs
    return db


def generate_embeddings(texts):
    # Generate embeddings for the texts
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
    embeddings = embeddings_model.embed_documents(texts)
    return embeddings

def create_vector_db(docs, embeddings_model):
    url = "http://134.122.1.211:6333"
    # Check if collection exists and create it if it doesn't
    collection_name = "vector_db"
    client = QdrantClient(
        url=url, prefer_grpc=False
    )
    try:
        client.get_collection(collection_name=collection_name, 
                              force_recreate=True,
                              vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
                              )
        print(f"Collection {collection_name} exists")
    except Exception as e:
        # Collection doesn't exist, create it
        # You need to specify the vector dimension based on your embeddings model
        client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        force_recreate=True,
    )
        print(f"Collection {collection_name} created successfully")
    
    # vector_store = QdrantVectorStore(
    # client=client,
    # collection_name="vector_db",
    # embedding=embeddings_model,
    # )

    qdrant = QdrantVectorStore.from_documents(
        documents=docs,
        embedding=embeddings_model,
        url=url,
        prefer_grpc=False,
        collection_name="vector_db"
    )
    print("Vector DB Successfully Created!")


if __name__ == "__main__":
    documents = load_pdf("data/15.pdf")
    split_docs = split_documents(documents)