import requests
from bs4 import BeautifulSoup
from utils import chunk_text

def scrape_and_clean(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = ' '.join(text.split())
    chunks = chunk_text(text)
    return chunks
