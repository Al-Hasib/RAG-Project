# import streamlit as st
# from src.chat import ask_question

# # Streamlit sidebar for file upload
# st.sidebar.title("Upload Files")
# uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
# uploaded_excel = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])

# # Chatbot interface
# st.title("Chatbot Interface")

# # React to user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("assistant"):
#         st.markdown(ask_question(prompt))

from src.utils import retreive_db
from src.chat import rag_chain
from src.create_vector import create_knowledgebase
# load_dotenv()
# data_path = "/root/RAG-Project/data/150-WBE_500-TDS.pdf"
# data_path = r"F:\Projects\RAG-with-Qdrant\data\150-WBE_500-TDS.pdf"

# create_knowledgebase(data_path)
# db = retreive_db()
# print(db.similarity_search("What is the purpose of the document?"))
# # db = retreive_db()
# docs = db.similarity_search("What is the purpose of the document?")
# print(f"{docs[0].page_content}\n\n")

result = rag_chain.invoke({"chat_history":[], "question":"hi"})

print(result)