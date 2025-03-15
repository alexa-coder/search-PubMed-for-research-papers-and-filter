import argparse
import csv
from getpaperslist.pubmed_fetcher import search_pubmed, fetch_paper_details

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers based on a query.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-f", "--file", help="Save results to a file (CSV)")
    args = parser.parse_args()

    print(f"Searching PubMed for: {args.query}")
    pubmed_ids = search_pubmed(args.query)
    print(f"Found {len(pubmed_ids)} papers")

    papers = fetch_paper_details(pubmed_ids)

    if args.file:
        with open(args.file, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["PubmedID", "Title"])
            for paper in papers:
                writer.writerow([paper["PubmedID"], paper["Title"]])
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(f"{paper['PubmedID']}: {paper['Title']}")

if __name__ == "__main__":
    main()