import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

def add_chunks(chunks, embeddings, file_id, path, filename, extension, modified):
    ids = []
    metadatas = []

    for i in range(len(chunks)):
        ids.append(f"{file_id}_{i}")

        metadatas.append({
            "file_id": file_id,
            "path": path,
            "filename": filename,
            "extension": extension,
            "modified": modified,
            "chunk_index": i
        })

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def get_count():
    return collection.count()

def search(query, embedding_model, n_results=5):
    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    )

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results