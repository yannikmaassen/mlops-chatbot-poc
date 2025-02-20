import chromadb
import json

def initialize_chromadb():
    chroma_client = chromadb.PersistentClient(path="chroma_db")
    collection = chroma_client.get_or_create_collection(name="mlflow_docs")
    return collection

def add_to_database(collection, text_chunks, embeddings, metadata):
    for idx, chunk in enumerate(text_chunks):
        collection.add(
            ids=[str(idx)],
            documents=[chunk],
            embeddings=[embeddings[idx]],
            metadatas=[metadata[idx]]
        )
    print("Data stored in DB.")


def populate_chromadb():
    with open("data/mlflow_chunks.json", "r") as f:
        chunks_data = json.load(f)
    
    with open("data/mlflow_embeddings.json", "r") as f:
        embeddings_data = json.load(f)
    
    collection = initialize_chromadb()
    if collection.count() > 0:
        print("ChromaDB already populated - skipping data insertion")
        return
    
    for idx, (chunk, embedding) in enumerate(zip(chunks_data, embeddings_data)):
        collection.add(
            ids=[str(idx)],
            documents=[chunk["chunk"]],
            embeddings=[embedding["embedding"]],
            metadatas=[{"url": chunk["url"]}]
        )
    
    print(f"Populated ChromaDB with {len(chunks_data)} documents")

if __name__ == "__main__":
    populate_chromadb()

