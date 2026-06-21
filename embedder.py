from sentence_transformers import SentenceTransformer
from extraction_manager import extract_text
from chunker import chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embeddings(path, extension):
    text = extract_text(path, extension)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks, convert_to_numpy=True)
    return chunks, embeddings