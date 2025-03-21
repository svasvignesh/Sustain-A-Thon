from flask import Flask, render_template, request, jsonify
import os
import ollama
from utils.chunking import chunk_pdf
from utils.embedding import generate_embeddings
from utils.vector_db import VectorDB
from transformers import pipeline
import re
import torch

app = Flask(__name__)


db = VectorDB()

# Load summarization and translation models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

try:
    translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
except Exception as e:
    print(f"Error loading translation model: {e}")

# Preprocess the PDF and store embeddings in the vector DB
def preprocess_chunks(pdf_dir):
    for pdf_file in os.listdir(pdf_dir):
        if pdf_file.endswith(".pdf"):
            chunks = chunk_pdf(os.path.join(pdf_dir, pdf_file))
            for idx, chunk in enumerate(chunks):
                embedding = generate_embeddings(chunk)
                db.add_document(chunk, embedding)

pdf_dir = "data/"
preprocess_chunks(pdf_dir)

def intelligent_formatting(text, user_input):
    def add_indentation(text):
        lines = text.strip().split("\n")
        formatted_lines = []

        section_patterns = {
            "main": re.compile(r"^(I{1,3}\.|IV\.)"),
            "sub": re.compile(r"^(A|B|C)\."), 
            "sub_sub": re.compile(r"^\d+\."),
        }

        for line in lines:
            stripped = line.strip()
            if section_patterns["main"].match(stripped):
                formatted_lines.append(f"\n➡️ {stripped}")
            elif section_patterns["sub"].match(stripped):
                formatted_lines.append(f"    • {stripped}")
            elif section_patterns["sub_sub"].match(stripped):
                formatted_lines.append(f"        {stripped}")
            else:
                formatted_lines.append(f"          - {stripped}")

        return "\n".join(formatted_lines)

    if "in points" in user_input.lower():
        sentences = text.split(". ")
        return "\n".join([f"• {sentence.strip()}" for sentence in sentences if sentence])

    if "summarize" in user_input.lower():
        text = summarizer(text, max_length=150, min_length=80, do_sample=False)[0]["summary_text"]

    return add_indentation(text)

def chunk_and_translate(text, max_length=512):
    """Chunk large text and translate in parts."""
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    translated_text = []

    for chunk in chunks:
        try:
            output = translator(chunk, max_length=600)[0]["translation_text"]
            translated_text.append(output)
        except Exception as e:
            translated_text.append("अनुवाद में त्रुटि हुई।")

    return " ".join(translated_text)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    language = request.json.get("language", "en")

    results = db.query(user_input, top_k=3)

    print(f"💬 User Input: {user_input}, Language: {language}")
    print(f"🔍 Query Results: {results}")

    if results:
        combined_answer = " ".join(results)
        print(f"📚 Combined Answer (Before Formatting): {combined_answer}")

        try:
            response = ollama.chat(model="deepseek-r1:1.5b", messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Based on the following context: {combined_answer}, answer the question: {user_input}"}
            ])

            raw_content = getattr(response.message, 'content', "")

            # Clean unwanted tags and artifacts
            cleaned_content = re.sub(r"<think>.*?</think>", "", raw_content, flags=re.DOTALL).strip()
            formatted_response = cleaned_content if cleaned_content else "No content available from model."

            # Translate if Hindi is selected
            if language == "hi":
                print("🌐 Translating to Hindi...")
                formatted_response = chunk_and_translate(formatted_response)

        except Exception as e:
            formatted_response = f"Error occurred while processing the request: {str(e)}"
            

        print(f"📊 Final Response Sent to Frontend: {formatted_response}")
        return jsonify({"response": formatted_response})

    else:
        return jsonify({"response": "I'm sorry, I couldn't find relevant information."})

if __name__ == "__main__":
    app.run(debug=True)
