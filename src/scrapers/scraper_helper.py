import re
import requests
from bs4 import BeautifulSoup


def scrape_text(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    raw_text = "\n".join([p.get_text() for p in soup.find_all(["p", "h1", "h2", "h3", "li", "code", "pre"])])
    clean_text = re.sub(r"\n+", "\n", raw_text)
    clean_text = re.sub(r"[ ]{2,}", " ", clean_text).strip()
    clean_text = clean_text.encode("ascii", "ignore").decode()
    clean_text = "\n".join([line for line in clean_text.split("\n") if len(line.split()) > 5])

    return clean_text