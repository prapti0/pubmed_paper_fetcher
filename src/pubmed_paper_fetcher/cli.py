# import argparse
# from pubmed_paper_fetcher.fetcher import fetch_papers, save_to_csv
# from pubmed_paper_fetcher.utils.logger import logger

# def main():
#     parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
#     parser.add_argument("query", type=str, help="Search query for PubMed.")
#     parser.add_argument("-f", "--file", type=str, help="Filename to save output as CSV.")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

#     args = parser.parse_args()

#     if args.debug:
#         logger.setLevel("DEBUG")

#     logger.info(f"Fetching papers for: {args.query}")
#     papers = fetch_papers(args.query)

#     if not papers:
#         logger.error("No papers found. Exiting.")
#         return

#     if args.file:
#         save_to_csv(papers, args.file)
#     else:
#         for paper in papers:
#             print(f"{paper['PubmedID']} - {paper['Title']} ({paper['Publication Date']})")

# if __name__ == "__main__":
#     main()
import argparse
from pubmed_paper_fetcher.fetcher import fetch_papers, save_to_csv
from pubmed_paper_fetcher.utils.logger import logger

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save output as CSV.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel("DEBUG")

    logger.info(f"🔍 Fetching papers for: {args.query}")
    papers = fetch_papers(args.query)

    if not papers:
        logger.error("⚠️ No papers found. Exiting.")
        return

    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(f"{paper['PubmedID']} - {paper['Title']} ({paper['Publication Date']})")

if __name__ == "__main__":
    main()
