from db_handler import get_text_files
from chromadb_handler import add_chunks
from chunker import chunk_text
from extraction_manager import extract_text
from sentence_transformers import SentenceTransformer

files_data = get_text_files()

all_chunks = []
chunk_counts = []
valid_files = []

print("Extracting and chunking files...")

for file in files_data:
    try:
        print(f"Chunking {file[2]}")

        text = extract_text(file[1], file[3])

        if not text or not text.strip():
            continue

        chunks = chunk_text(text)

        if not chunks:
            continue

        all_chunks.extend(chunks)

        chunk_counts.append(len(chunks))
        valid_files.append(file)

    except Exception as e:
        print(f"Failed to process {file[2]}: {e}")

print(f"\nTotal chunks: {len(all_chunks)}")

print("\nCreating embeddings...")

model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    all_chunks,
    batch_size=200,
    convert_to_numpy=True,
    show_progress_bar=True
)

print("\nStoring in ChromaDB...")

current = 0

for file, num_chunks in zip(valid_files, chunk_counts):

    file_chunks = all_chunks[current:current + num_chunks]

    file_embeddings = embeddings[current:current + num_chunks]

    add_chunks(
        file_chunks,
        file_embeddings,
        file[0],  # file_id
        file[1],  # path
        file[2],  # filename
        file[3],  # extension
        file[5]   # modified
    )

    current += num_chunks

    print(f"Indexed {file[2]} ({num_chunks} chunks)")

print("\nIndexing complete.")