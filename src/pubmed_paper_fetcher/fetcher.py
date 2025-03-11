import requests
import pandas as pd
from typing import List, Dict
from pubmed_paper_fetcher.utils.logger import logger

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def fetch_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch research papers from PubMed."""
    logger.info(f"Searching PubMed for: {query}")

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
    }

    try:
        response = requests.get(PUBMED_API_URL, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Failed: {e}")
        return []

    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        logger.warning("No papers found!")
        return []

    logger.info(f"Found {len(paper_ids)} papers. Fetching details...")

    # Fetch paper details
    details_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json",
    }

    try:
        details_response = requests.get(PUBMED_SUMMARY_URL, params=details_params)
        details_response.raise_for_status()
        details_data = details_response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch paper details: {e}")
        return []

    papers = []
    for paper_id in paper_ids:
        info = details_data["result"].get(paper_id, {})
        papers.append(
            {
                "PubmedID": paper_id,
                "Title": info.get("title", "N/A"),
                "Publication Date": info.get("pubdate", "N/A"),
            }
        )

    logger.info("Successfully fetched paper details!")
    return papers


def save_to_csv(papers: List[Dict], filename: str):
    """Save fetched papers to a CSV file."""
    if not papers:
        logger.warning("No data to save!")
        return

    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    logger.info(f"Results saved to {filename}")
