from flask import Flask, render_template, request, jsonify
import os
from utils.chunking import chunk_pdf
from utils.embedding import generate_embeddings
from utils.vector_db import VectorDB
from transformers import pipeline

import re

app = Flask(__name__)

# Initialize Vector DB
db = VectorDB()

# Load summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def preprocess_chunks(pdf_dir):
    """Processes PDFs and stores embeddings in the vector DB."""
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            chunks = chunk_pdf(os.path.join(pdf_dir, pdf_file))
            for idx, chunk in enumerate(chunks):
                print(f"📚 Chunk {idx + 1} (Length: {len(chunk)} chars):\n{chunk}\n{'=' * 50}")
                embedding = generate_embeddings(chunk)
                db.add_document(chunk, embedding)

pdf_dir = "data/"
preprocess_chunks(pdf_dir)


def intelligent_formatting(text, user_input):
    """Enhanced formatting for chatbot's response with better structure detection."""

    def add_indentation(text):
        lines = text.strip().split("\n")
        formatted_lines = []

        # Regular expressions to detect sections
        section_patterns = {
            "main": re.compile(r"^(I{1,3}\.|IV\.)"),  # Matches I., II., III., IV.
            "sub": re.compile(r"^(A|B|C)\."),        # Matches A., B., C.
            "sub_sub": re.compile(r"^\d+\."),        # Matches 1., 2., 3.
        }

        for line in lines:
            stripped = line.strip()

            # Main section (I., II., III., etc.)
            if section_patterns["main"].match(stripped):
                formatted_lines.append(f"\n➡️ {stripped}")
            
            # Subsection (A., B., C., etc.)
            elif section_patterns["sub"].match(stripped):
                formatted_lines.append(f"    • {stripped}")

            # Sub-subsection (1., 2., etc.)
            elif section_patterns["sub_sub"].match(stripped):
                formatted_lines.append(f"        {stripped}")

            # Normal line, provide deeper indentation
            else:
                formatted_lines.append(f"          - {stripped}")

        return "\n".join(formatted_lines)

    # Prioritize point format if the user asks for it
    if "in points" in user_input.lower():
        sentences = text.split(". ")
        return "\n".join([f"• {sentence.strip()}" for sentence in sentences if sentence])

    # Summarize only if explicitly requested
    if "summarize" in user_input.lower():
        text = summarizer(text, max_length=150, min_length=80, do_sample=False)[0]["summary_text"]

    # Auto-detect and format using structured points
    return add_indentation(text)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Query the vector database (retrieve top 3 results for better context)
    results = db.query(user_input, top_k=3)

    print(f"💬 User Input: {user_input}")
    print(f"🔍 Query Results: {results}")

    if results:
        # Combine the most relevant chunks
        combined_answer = " ".join(results)
        print(f"📚 Combined Answer (Before Formatting): {combined_answer}")

        formatted_response = intelligent_formatting(combined_answer, user_input)

        print(f"📊 Formatted Response: {formatted_response}")

        return jsonify({"response": formatted_response})
    else:
        return jsonify({"response": "I'm sorry, I couldn't find relevant information."})


if __name__ == "__main__":
    app.run(debug=True)
