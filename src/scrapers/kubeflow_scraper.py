import json
from scraper_helper import scrape_text
from docs_collection import get_kubeflow_docs

KUBEFLOW_DOCS = get_kubeflow_docs()

def scrape_kubeflow():
    data = []
    for url in KUBEFLOW_DOCS:
        print(f"Scraping: {url}")

        clean_text = scrape_text(url)
        data.append({"url": url, "content": clean_text})
    
    with open("data/kubeflow/kubeflow_docs.json", "w") as f:
        json.dump(data, f, indent=4)
    print("Kubeflow Documentation Saved!")

if __name__ == "__main__":
    scrape_kubeflow()
