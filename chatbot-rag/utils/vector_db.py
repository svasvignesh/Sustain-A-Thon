# Add this to all files under "utils"
import sys
sys.path.append("..")
from .embedding import generate_embeddings
import chromadb
import uuid
import numpy as np

class VectorDB:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_document(self, doc, embedding):
        self.documents.append(doc)
        self.embeddings.append(np.array(embedding))

    def query(self, query_text, top_k=3):
        query_embedding = np.array(generate_embeddings(query_text))
        similarities = [np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb)) for emb in self.embeddings]

        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return [self.documents[i] for i in top_indices]

