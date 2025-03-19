import streamlit as st

# Streamlit sidebar for file upload
st.sidebar.title("Upload Files")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
uploaded_excel = st.sidebar.file_uploader("Upload Excel", type=["xlsx"])

# Chatbot interface
st.title("Chatbot Interface")

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("assistant"):
        st.markdown(prompt)