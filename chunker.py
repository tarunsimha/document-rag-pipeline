from nltk.tokenize import sent_tokenize

def chunk_text(text, chunk_size=500, overlap_sentences=1):
    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        if current_length + len(sentence) <= chunk_size:
            current_chunk.append(sentence)
            current_length += len(sentence)
        else:
            chunks.append(" ".join(current_chunk))

            current_chunk = (
                current_chunk[-overlap_sentences:]
                if len(current_chunk) >= overlap_sentences
                else current_chunk
            )

            current_length = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += len(sentence)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks