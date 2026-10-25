import chromadb
from sentence_transformers import SentenceTransformer
from ingest import build_chunks

def build_index():
    chunks = build_chunks("data/raw")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="chroma_db")
    try:
        client.delete_collection("docs")
    except Exception:
        pass
    collection = client.create_collection(name="docs",
                                          metadata={"hnsw:space": "cosine"})
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()
    for i in range(0, len(chunks), 100):
        batch = chunks[i:i+100]
        collection.add(
            ids = [chunk["id"] for chunk in batch],
            documents = [chunk["text"] for chunk in batch],
            embeddings = embeddings[i: i+100],
            metadatas = [{"source": chunk["source"], "section": chunk["section"], "chunk_index": chunk["chunk_index"]} for chunk in batch]
        )
    print("Indexed", collection.count(), "chunks")

if __name__ == "__main__":
    build_index()