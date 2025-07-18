import os
from chromadb import PersistentClient

CHAPTER_DIR = "data"  
PERSIST_DIR = "db/chroma_store" 

client = PersistentClient(path=PERSIST_DIR)
collection = client.get_or_create_collection(name="chapter_versions")

def index_chapter_versions():
    print("Indexing chapter versions...")

    for fname in os.listdir(CHAPTER_DIR):
        if fname.endswith(".txt"):
            version_id = fname.replace(".txt", "")
            file_path = os.path.join(CHAPTER_DIR, fname)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            try:
                collection.add(
                    documents=[content],
                    ids=[version_id],
                    metadatas=[{"filename": fname}]
                )
                print(f"Indexed: {fname}")
            except Exception as e:
                print(f" Skipped {fname}: {e}")

    print(" ChromaDB vector store updated at:", PERSIST_DIR)

def search_similar_versions(query: str, n_results=3):
    print(f"\n Searching for versions similar to: \"{query}\"...")
    results = collection.query(query_texts=[query], n_results=n_results)

    for i, doc in enumerate(results["documents"][0]):
        print(f"\n  Match {i+1}:")
        print("Preview:", doc[:300], "...")
        print(" Metadata:", results["metadatas"][0][i])
