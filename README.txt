#Sustain-A-Thon
Sustain-A-Thon


🐾 Wildlife Bot – RAG Chatbot for Human-Wildlife Conflict Information
The Wildlife Bot is a Flask-based RAG (Retrieval-Augmented Generation) chatbot designed to provide intelligent and contextual answers related to wildlife compensation and human-wildlife conflict policies. It uses PDF documents as a knowledge base, processes them for semantic search, and leverages deepseek-r1:1.5b for natural language understanding.

📌 Features
🧠 RAG System: Retrieves context from PDF documents and generates intelligent responses.
🌐 Bilingual Support: Provides responses in English and Hindi.
📚 PDF Knowledge Base: Upload and query additional PDFs by adding them to the data/ folder.
🔍 Semantic Search: Uses vector embeddings to find the most relevant information.
🗣️ Dynamic Chat: Supports intelligent conversations with deepseek-r1:1.5b via ollama.
📊 Summarization & Formatting: Summarizes and formats content for better clarity.

1. Clone the Repository
git clone https://github.com/svasvignesh/Sustain-A-Thon
cd wildlife-bot

python --version

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install Dependencies

pip install -r requirements.txt

3. Set Up Ollama and deepseek-r1:1.5b
Download and install Ollama: https://ollama.ai/download

Pull the deepseek-r1:1.5b model:

4. Run the Application

python app.py


