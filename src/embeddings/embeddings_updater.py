import json
import os
from database.database import initialize_chromadb
from embeddings.embeddings_helper import get_embedding

DATASET_FILE = "data/unified_mlops_dataset.json"

def load_dataset():
    if os.path.exists(DATASET_FILE):
        with open(DATASET_FILE, "r") as f:
            return json.load(f)
    return []


def update_embeddings():
    print("Updating embeddings for the dataset...")
    dataset = load_dataset()
    if not dataset:
        print("No dataset found. Run the data collection script first.")
        return

    collection = initialize_chromadb()
    for entry in dataset:
        if not entry.get("embedding"):
            embedding = get_embedding(entry["text"])
            entry["embedding"] = embedding

            collection.add(
                ids=[entry["id"]],
                documents=[entry["text"]],
                embeddings=[embedding],
                metadatas=[{"source": entry["source"], "url": entry["metadata"].get("url", "")}]
            )
            print(f"Embedding generated for document {entry['id']}.")

    with open(DATASET_FILE, "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"Embeddings generated and stored for {len(dataset)} documents.")

if __name__ == "__main__":
    update_embeddings()
