import fitz
import re

def chunk_pdf(pdf_path, chunk_size=1000):
    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)

    # Split by paragraphs, sections, or semantic markers
    chunks = re.split(r'(\n{2,}|(?=I{1,3}\.)|(?<=Definition:)|(?<=means)|(?<=is defined as))', text)

    valid_chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 100]
    return valid_chunks