import os
import uuid
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from agents import reward_system  

CHAPTER_ID = "Chapter_1"
VERSION_PATH = f"versions/{CHAPTER_ID}/v2.txt"
COLLECTION_NAME = CHAPTER_ID.replace(" ", "_")

def split_text(text, max_length=500):
    return [p.strip() for p in text.split("\n") if len(p.strip()) > 0]

def index_final_version():
    client = chromadb.PersistentClient(path="chromadb_data")
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)

    with open(VERSION_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = split_text(content)
    print(f"Indexing {len(chunks)} chunks from: {VERSION_PATH}")

    for i, chunk in enumerate(chunks):
        doc_id = f"{CHAPTER_ID}-{i}-{uuid.uuid4().hex[:8]}"
        collection.add(
            documents=[chunk],
            ids=[doc_id],
            metadatas=[{"chunk_number": i, "chunk_id": doc_id, "chapter": CHAPTER_ID}]
        )
        print(f"Indexed chunk {i+1}: {doc_id}")

    print(f"\n Indexing complete. Stored in ChromaDB collection: '{COLLECTION_NAME}'")

def semantic_search(query, top_k=3):
    client = chromadb.PersistentClient(path="chromadb_data")
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embedding_fn)

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    search_results = []
    for i in range(len(documents)):
        doc = documents[i]
        meta = metadatas[i] if i < len(metadatas) else {}
        dist = distances[i] if i < len(distances) else None

        search_results.append({
            "chunk_number": meta.get("chunk_number", i),
            "chunk_id": meta.get("chunk_id", f"{CHAPTER_ID}-unknown-{i}"),
            "chapter": meta.get("chapter", CHAPTER_ID),
            "text": doc,
            "distance": dist
        })

    return search_results


if __name__ == "__main__":
    index_final_version()

    while True:
        q = input("\n Enter a search query (or 'exit'): ")
        if q.lower() == "exit":
            break

        results = semantic_search(q)
        for result in results:
            print(f"\n  Chunk #{result['chunk_number']}")
            print(result['text'])
            print(f"---\nDistance: {result['distance']:.4f}")

