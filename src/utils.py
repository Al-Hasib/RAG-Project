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
    collection_name = "vector_db"
    client = QdrantClient(
        url=url, 
        prefer_grpc=False
    )
    
    # Get the dimension of your current embedding model
    embedding_dimension = 1536  # Assuming you're using a model with 1536 dimensions
    
    try:
        # Try to get the collection to see if it exists
        collection_info = client.get_collection(collection_name=collection_name)
        existing_dimension = collection_info.config.params.vectors.size
        
        # If dimensions don't match, recreate the collection
        if existing_dimension != embedding_dimension:
            print(f"Recreating collection to match embedding dimension: {embedding_dimension}")
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=embedding_dimension, distance=Distance.COSINE)
            )
    except Exception as e:
        # Collection doesn't exist, create it
        print(f"Creating new collection with dimension: {embedding_dimension}")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embedding_dimension, distance=Distance.COSINE)
        )
    
    # Now create the store with the collection that exists
    # db = QdrantVectorStore(client=client, embedding=embeddings_model, collection_name=collection_name)
    qdrant = QdrantVectorStore.from_documents(
        docs,
        embeddings_model,
        url=url,
        collection_name="vector_db",
    )
    return qdrant


if __name__ == "__main__":
    documents = load_pdf("data/15.pdf")
    split_docs = split_documents(documents)