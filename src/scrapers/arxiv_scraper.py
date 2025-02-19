import requests
import xml.etree.ElementTree as ET
import json
import fitz
import re

ARXIV_API_URL = "http://export.arxiv.org/api/query"
MAX_RESULTS = 3

def fetch_arxiv_papers(query="MLOps", max_results=MAX_RESULTS):
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    response = requests.get(ARXIV_API_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data from arXiv: {response.status_code}")
        return []

    root = ET.fromstring(response.text)
    papers = []
    
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
        pdf_url = entry.find("{http://www.w3.org/2005/Atom}id").text.strip().replace("abs", "pdf") + ".pdf"
        
        papers.append({
            "title": title,
            "summary": summary,
            "pdf_url": pdf_url
        })
    
    with open("data/arxiv/raw_arxiv_papers.json", "w") as f:
        json.dump(papers, f, indent=4)
    
    print(f"Saved {len(papers)} arXiv papers to data/arxiv/raw_arxiv_papers.json")
    return papers


def download_arxiv_paper(paper_id):
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    response = requests.get(pdf_url)
    
    if response.status_code == 200:
        pdf_path = f"data/arxiv/pdf/{paper_id}.pdf"
        with open(pdf_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {paper_id}.pdf successfully.")
        return pdf_path
    else:
        print(f"Failed to download {paper_id}.pdf")
        return None


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])

        clean_text = re.sub(r"\n+", "\n", text)
        clean_text = re.sub(r"[ ]{2,}", " ", clean_text).strip()
        clean_text = clean_text.encode("ascii", "ignore").decode()
        clean_text = "\n".join([line for line in clean_text.split("\n") if len(line.split()) > 5])

        return clean_text.strip()
    
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


if __name__ == "__main__":
    papers = fetch_arxiv_papers()
    
    arxiv_paper_ids = [paper["pdf_url"].split("/")[-1].replace(".pdf", "") for paper in papers]

    papers_data = []
    for paper_id in arxiv_paper_ids:
        pdf_path = download_arxiv_paper(paper_id)
        if pdf_path:
            paper_text = extract_text_from_pdf(pdf_path)
            if paper_text:
                papers_data.append({
                    "paper_id": paper_id,
                    "text": paper_text
                })

    with open("data/arxiv/arxiv_papers.json", "w") as f:
        json.dump(papers_data, f, indent=4)

    print("Extracted content saved to data/arxiv/arxiv_papers.json")
