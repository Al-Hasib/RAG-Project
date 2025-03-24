from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
import pandas as pd
from qdrant_client.http.models import Distance, VectorParams
from uuid import uuid4
from src.store import store


def load_pdf(file_path):
    basename = os.path.basename(file_path)
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return basename, documents

def load_csv(csv_file):
    from langchain_community.document_loaders.csv_loader import CSVLoader
    basename = os.path.basename(csv_file)
    loader = CSVLoader(file_path=csv_file, encoding="utf-8")
    data = loader.load()
    return basename, data

def load_text(file):
    from langchain_community.document_loaders import TextLoader
    basename = os.path.basename(file)
    loader = TextLoader(file,encoding="utf-8")
    document = loader.load()
    return basename, document


# Split documents into smaller chunks
def split_documents(basename, documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    split_docs = text_splitter.split_documents(documents)
    print(len(split_docs))
    uuids = [str(uuid4()) for _ in range(len(split_docs))]
    print(uuids)
    store.append(basename,uuids)
    print(store.get_all())
    return split_docs, uuids


# def retreive_context(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=api_key)
#     new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
#     docs = new_db.similarity_search(user_question)
#     print(docs)
#     return docs

# def retreive_db():
#     # url = "http://134.122.1.211:6333"
#     url = "http://localhost:6333"

#     client = QdrantClient(
#         url=url, prefer_grpc=False
#     )
#     collection_name = "vector_db"
#     embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
#     db = QdrantVectorStore(client=client, embedding=embeddings_model, collection_name="vector_db")
#     return db


def generate_embeddings(texts):
    # Generate embeddings for the texts
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
    embeddings = embeddings_model.embed_documents(texts)
    return embeddings

def create_vector_db(embeddings_model):
    url = "http://134.122.1.211:6333"
    # url = "http://localhost:6333"
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
    # qdrant = QdrantVectorStore.from_documents(
    #     docs,
    #     embeddings_model,
    #     url=url,
    #     collection_name="vector_db",
    # )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings_model,
    )
    return vector_store


def add_document_to_vector(vector_store,documents, ids):
    vector_store.add_documents(documents=documents, ids=ids)
    return "Documents added to vector db"

def remove_document_from_vector(vector_store, filename):
    ids = store.data[filename]
    vector_store.delete(ids=ids)
    store.delete(filename)
    print(f"Deleted Ids: {ids}")
    return f"{filename} has been deleted from vectordb"


def get_all_metadata():
    # url = "http://localhost:6333"
    url = "http://134.122.1.211:6333"
    collection_name = "vector_db"

    client = QdrantClient(url=url, prefer_grpc=False)

    # Scroll through all stored vectors
    scroll_results = client.scroll(collection_name=collection_name, limit=100)

    for result in scroll_results[0]:  # The first item contains the points
        print(f"ID: {result.id}, Metadata: {result.payload}")

    return scroll_results

def delete_collection():
    # url = "http://localhost:6333"
    url = "http://134.122.1.211:6333"
    collection_name = "vector_db"

    client = QdrantClient(url=url, prefer_grpc=False)

    # Delete the entire collection
    client.delete_collection(collection_name=collection_name)
    print(f"Collection '{collection_name}' deleted successfully!")


if __name__ == "__main__":
    documents = load_pdf("data/15.pdf")
    split_docs = split_documents(documents)