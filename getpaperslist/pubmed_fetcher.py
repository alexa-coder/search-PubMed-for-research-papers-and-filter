import requests
import xml.etree.ElementTree as ET
from typing import List, Optional

def search_pubmed(query: str, max_results: int = 100) -> List[str]:
    """Searches PubMed for papers matching the query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": max_results}
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"PubMed API request failed with status {response.status_code}")

    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[dict]:
    """Fetches details for the given PubMed IDs."""
    if not pubmed_ids:
        return []

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"PubMed API request failed with status {response.status_code}")

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "No Title"
        papers.append({"PubmedID": pmid, "Title": title})

    return papers