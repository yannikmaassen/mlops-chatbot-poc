import chromadb

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
