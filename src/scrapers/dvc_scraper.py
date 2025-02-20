import json
from scraper_helper import scrape_text
from docs_collection import get_dvc_docs

DVC_DOCS = get_dvc_docs()

def scrape_dvc():
    data = []
    for url in DVC_DOCS:
        print(f"Scraping: {url}")
        clean_text = scrape_text(url)
        data.append({"url": url, "content": clean_text})
    
    with open("data/dvc/dvc_docs.json", "w") as f:
        json.dump(data, f, indent=4)
    print("DVC Documentation Saved!")

if __name__ == "__main__":
    scrape_dvc()