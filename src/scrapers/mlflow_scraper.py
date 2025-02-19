import json
from scraper_helper import scrape_text
from docs_collection import get_mlflow_docs

MLFLOW_DOCS = get_mlflow_docs()


def scrape_mlflow():
    data = []
    for url in MLFLOW_DOCS:
        print(f"Scraping: {url}")

        clean_text = scrape_text(url)
        data.append({"url": url, "content": clean_text})
    
    with open("data/mlflow/mlflow_docs.json", "w") as f:
        json.dump(data, f, indent=4)
    print("MLflow Documentation Saved!")

if __name__ == "__main__":
    scrape_mlflow()