from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from src.chat import rag_chain
from src.create_vector import create_knowledgebase, chat_history
chat_history = chat_history(user_assistant= None)
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# Initialize FastAPI app
app = FastAPI(title="RAG Chat API", description="API for RAG-based chat application")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify your frontend origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# class ChatResponse(BaseModel):
#     response: str

# class ChatRequest(BaseModel):
#     messages: List[ChatMessage]
#     stream: Optional[bool] = False

# # Initialize chat components
# try:
#     # Initialize the RAG chain and database
#     # You might want to place this in a separate function or module
#     logger.info("Initializing RAG components...")
#     data_path = "/root/RAG-Project/data/150-WBE_500-TDS.pdf"
#     db = create_knowledgebase(data_path)
#     logger.info("RAG components initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize RAG components: {str(e)}")
#     raise

@app.get("/")
async def root():
    return {"message": "RAG Chat API is running. Use /chat endpoint to interact."}


@app.post("/chat")
async def chat(user_input: str):
    latest_chat_history = chat_history.get_chat_history()
    print(latest_chat_history)
    result = rag_chain.invoke({"chat_history":latest_chat_history, "question":user_input})
    chat_history.create_chat_history(user_input, result)
    return JSONResponse(status_code=200, content={"response": result})


@app.get("/chat_history")
async def get_chat_history():
    all_chat =  chat_history.all_chat_history()
    length = len(chat_history)
    return JSONResponse(status_code=200, content={ "length": length, "chat_history": all_chat})
#     try:
#         # Extract the last user message
#         user_messages = [msg.content for msg in request.messages if msg.role == "user"]
#         if not user_messages:
#             raise HTTPException(status_code=400, detail="No user message found")
        
#         last_user_message = user_messages[-1]
#         logger.info(f"Processing chat request: {last_user_message[:50]}...")
        
#         # Get chat history (excluding the last user message)
#         chat_history = []
#         for i in range(0, len(request.messages) - 1, 2):
#             if i+1 < len(request.messages):
#                 if request.messages[i].role == "user" and request.messages[i+1].role == "assistant":
#                     chat_history.append((request.messages[i].content, request.messages[i+1].content))
        
#         # Process with RAG chain
#         # Adjust this based on your actual chain's input format
#         result = chain.invoke({
#             "question": last_user_message,
#             "chat_history": chat_history
#         })
        
#         # Extract response and sources
#         # Adjust based on your chain's output format
#         response = result.get("answer", "")
#         sources = result.get("sources", [])
        
#         logger.info(f"Generated response of length {len(response)}")
        
#         return ChatResponse(response=response, sources=sources)
    
#     except Exception as e:
#         logger.error(f"Error processing chat request: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# # from typing import Dict, List, Optional
# # import uvicorn
# # import os
# # from dotenv import load_dotenv


# # Import your RAG chain components
# # Replace these imports with your actual implementation



# # Load environment variables
# load_dotenv()







# # Pydantic models
# class ChatMessage(BaseModel):
#     role: str  # "user" or "assistant"
#     content: str










# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     logger.error(f"Unhandled exception: {str(exc)}")
#     return JSONResponse(
#         status_code=500,
#         content={"detail": f"An unexpected error occurred: {str(exc)}"}
#     )

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 8000))
#     uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)


# # from src.chat import rag_chain

# # while True:
# #     user_input = input("Enter your question: ")
# #     result = rag_chain.invoke(user_input)
# #     print(result)
# #     if user_input == "exit":
# #         break