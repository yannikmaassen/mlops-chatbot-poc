import json
from scraper_helper import scrape_text
from docs_collection import get_tensorflow_docs

TENSORFLOW_DOCS = get_tensorflow_docs()


def scrape_tensorflow():
    data = []
    for url in TENSORFLOW_DOCS:
        print(f"Scraping: {url}")

        clean_text = scrape_text(url)
        data.append({"url": url, "content": clean_text})
    
    with open("data/tensorflow/tensorflow_docs.json", "w") as f:
        json.dump(data, f, indent=4)
    print("TensorFlow Documentation Saved!")

if __name__ == "__main__":
    scrape_tensorflow()