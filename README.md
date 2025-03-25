# Retrieval-Augmented Generation (RAG) with Qdrant and OpenAI

This project demonstrates how to perform Retrieval-Augmented Generation (RAG) using Qdrant for vector storage and OpenAI for language generation. The setup involves loading documents, generating embeddings, storing them in Qdrant, and querying them to generate responses using OpenAI.

## Setup

1. **Ensure you have a running instance of Qdrant**. You can use Docker to run Qdrant:

   ```bash
   docker compose up --build -d
   ```
2. **Create a `.env` file** in the project directory and add your OpenAI API key:

   ```env
   OPENAI_KEY=your-openai-api-key
   ```

**chatbot**: http://134.122.1.211:5000/
**upload file to knowledgebase and remove from knowledgebase**: http://134.122.1.211:5000/upload_file


## License

This project is licensed under the MIT License. See the LICENSE file for details.
