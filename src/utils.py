from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents

def load_csv(file_path):
    # Load CSV
    csv_file = "data.csv"  # Replace with your CSV file
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


def retreive_context(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=api_key)
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    print(docs)
    return docs

def generate_embeddings(texts)
    # Generate embeddings for the texts
    embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
    embeddings = embeddings_model.embed_documents(texts)


def create_vector_db(texts, embeddings_model):
    url = "http://localhost:6333"
    qdrant = Qdrant.from_texts(
        texts=texts,
        embedding=embeddings_model,
        url=url,
        prefer_grpc=False,
        collection_name="vector_db"
    )
    print("Vector DB Successfully Created!")


if __name__ == "__main__":
    documents = load_documents("data/15.pdf")
    split_docs = split_documents(documents)