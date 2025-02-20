import json
import os
import uuid

JSON_FILES = {
    "stackoverflow": "data/stackoverflow/stackoverflow_mlops.json",
    "github": "data/github/github_mlops_discussions.json",
    "arxiv": "data/arxiv/arxiv_papers.json",
    "mlflow_docs": "data/mlflow/mlflow_docs.json",
    "kubeflow_docs": "data/kubeflow/kubeflow_docs.json",
    "tensorflow_docs": "data/tensorflow/tensorflow_docs.json"
}

OUTPUT_FILE = "data/unified_mlops_dataset.json"

def generate_id(source, identifier):
    return f"{source}_{identifier}"

def transform_data(source, raw_data):
    unified_data = []
    
    for entry in raw_data:
        if source == "stackoverflow":
            if "title" in entry and "top_answers" in entry and entry["top_answers"]:
                qa_pairs = [{"question": entry["title"], "answer": ans["body"]} for ans in entry["top_answers"]]
            else:
                qa_pairs = []
            unified_data.append({
                "id": generate_id(source, entry["question_id"]),
                "source": "stackoverflow",
                "metadata": {
                    "tags": entry.get("tags", []),
                    "created_at": entry.get("creation_date", ""),
                    "url": entry.get("link", "")
                },
                "text": entry.get("title", ""),
                "qa_pairs": qa_pairs,
                "embedding": []
            })

        elif source == "github":
            unified_data.append({
                "id": generate_id(source, uuid.uuid4().hex[:8]),
                "source": "github",
                "metadata": {
                    "repo": entry.get("repo", ""),
                    "created_at": entry.get("createdAt", ""),
                    "url": entry.get("url", "")
                },
                "text": entry.get("title", ""),
                "qa_pairs": [{"question": entry.get("title", ""), "answer": entry.get("bodyText", "")}],
                "embedding": []
            })

        elif source == "arxiv":
            unified_data.append({
                "id": generate_id(source, entry["paper_id"]),
                "source": "arxiv",
                "metadata": {
                    "title": entry.get("title", ""),
                    "authors": entry.get("authors", []),
                    "published_at": entry.get("published_at", ""),
                    "url": entry.get("pdf_url", "")
                },
                "text": entry.get("text", ""),
                "qa_pairs": [],
                "embedding": []
            })

        elif source in ["mlflow_docs", "kubeflow_docs", "tensorflow_docs"]:
            unified_data.append({
                "id": generate_id(source, uuid.uuid4().hex[:8]),
                "source": source.replace("_docs", ""),
                "metadata": {
                    "url": entry.get("url", "")
                },
                "text": entry.get("content", ""),
                "qa_pairs": [],
                "embedding": []
            })

    return unified_data

def merge_datasets():
    unified_dataset = []

    for source, file_path in JSON_FILES.items():
        if os.path.exists(file_path):
            print(f"Loading {source} data from {file_path}...")
            with open(file_path, "r") as f:
                raw_data = json.load(f)
                transformed_data = transform_data(source, raw_data)
                unified_dataset.extend(transformed_data)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(unified_dataset, f, indent=4)
    
    print(f"Merged dataset saved to {OUTPUT_FILE} with {len(unified_dataset)} entries.")

if __name__ == "__main__":
    merge_datasets()
