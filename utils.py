def chunk_text(text, max_len=500, overlap=100):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + max_len, len(words))
        chunks.append(" ".join(words[start:end]))
        start += max_len - overlap
    return chunks
