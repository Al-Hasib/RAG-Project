import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from src import utils
load_dotenv()
from typing import List, Tuple, Optional
from dataclasses import dataclass, field

def create_knowledgebase(data_path):
    try:
        file_extension = os.path.splitext(data_path)[1].lower()
        if file_extension == '.txt':
            basename, document = utils.load_text(data_path)
        elif file_extension == '.csv':
            basename, document = utils.load_csv(data_path)
        elif file_extension == '.pdf':
            basename, document = utils.load_pdf(data_path)
        else:
            pass
        
        split_docs, uuids = utils.split_documents(basename, document)
        # texts = [doc.page_content for doc in split_docs]

        embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
        vector_store = utils.create_vector_db(embeddings_model)
        message =utils.add_document_to_vector(vector_store=vector_store,
                                              documents=split_docs,
                                              ids=uuids
                                              )
        print("Vector database created successfully")
        return message
    except Exception as e:
        print(f"Error: {e}")


def delete_data_from_knowledgebase(file):
    try:
        embeddings_model = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_KEY"))
        vector_store = utils.create_vector_db(embeddings_model)
        message = utils.remove_document_from_vector(
                    vector_store=vector_store,
                    filename=file
        )
        print(message)
        return message

    except Exception as e:
        print(e)



@dataclass
class chat_history:
    user_assistant: List[Tuple[str, str]] = field(default_factory=list)
    

    def create_chat_history(self, user, assistant):
        self.user_assistant.append((user, assistant))
        # self.assistant.append(assistant)
    
    def get_chat_history(self):
        return (self.user_assistant[-5:])
    
    def __len__(self):
        return len(self.user_assistant)
    
    def all_chat_history(self):
        return (self.user_assistant)



