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
git clone https://github.com/svasvignesh/Sustain-A-Thon or 
https://cisco.sharepoint.com/sites/GreenTeam-BengaluruChapter/Shared%20Documents/Forms/AllItems.aspx?csf=1&web=1&e=kQiOzH&CID=c91ca141%2D896b%2D46a3%2Dbd08%2D885aafd576ec&FolderCTID=0x0120007EC4E7F5FFDB5C43A2A1AA0E9719E4E9&id=%2Fsites%2FGreenTeam%2DBengaluruChapter%2FShared%20Documents%2FSustain%2Da%2Dthon%20%2D%20Participant%20Submission%2FCWS%2FDevelopment%20of%20a%20Wildlife%20and%20Environmental%20Law%20Gen%20AI%20to%20aid%20in%20Human%2DWildlife%20Conflict%20Resolution%2FPing%20Intelligence&viewid=f8242a3b%2D8fcf%2D43be%2Dbac1%2D0ff561170923
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


