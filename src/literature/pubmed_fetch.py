import argparse
import yaml
import os
import pandas as pd
from Bio import Entrez
from Bio.Entrez.Parser import DictionaryElement
import matplotlib.pyplot as plt

# load configuration from YAML file
def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)

# Normalize a single PubMed summary record to a dictionary
def normalize_pubmed_record(record: DictionaryElement) -> dict:
    return {
        "PMID": record["Id"],
        "title": record.get("Title"),
        "year": record.get("PubDate", "")[:4],  # wyciągamy tylko rok
        "journal": record.get("FullJournalName"),
        "authors": "; ".join(a["Name"] for a in record.get("Authors", []))
    }

# fetch papers from PubMed for a given year and query
def fetch_pubmed(year: int, query: str, email: str, retmax: int) -> list[dict]:
    Entrez.email = email

    query_year = f"{query} AND ({year}[PDAT])" # PDAT = Publication Date

    handle = Entrez.esearch(
        db="pubmed",
        term=query_year,
        retmax=retmax
    )
    record = Entrez.read(handle)
    pmids = record["IdList"]

    # if no papers found, return empty list
    if not pmids:
        return []

    # fetch summaries for the found PMIDs
    handle = Entrez.esummary(db="pubmed", id=",".join(pmids))
    summaries = Entrez.read(handle)

    papers = [normalize_pubmed_record(doc) for doc in summaries]

    return papers

def main():
    # parse arguments and load config
    parser = argparse.ArgumentParser(description="Perform a small literature search.")
    parser.add_argument("-y", "--year", required=True, help="Literature search will be limited to papers published in this year")
    parser.add_argument("--config")

    args = parser.parse_args()
    config = load_config(args.config)

    # create output directory
    outdir = f"results/literature/{args.year}"
    os.makedirs(outdir, exist_ok=True)

    # fetch papers from PubMed
    papers = fetch_pubmed(
        year=args.year,
        query=config["pubmed"]["query"],
        email=config["pubmed"]["email"],
        retmax=config["pubmed"]["limit"],
    )

    # Save papers metadata
    df = pd.DataFrame(papers)
    df.to_csv(f"{outdir}/pubmed_papers.csv", index=False)

    # Aggregate summary statistics by year
    summary_by_year = (
        df.groupby("year")
          .size()
          .reset_index(name="n_papers")
    )
    summary_by_year.to_csv(f"{outdir}/summary_by_year.csv", index=False)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.bar(summary_by_year["year"], summary_by_year["n_papers"])
    plt.xlabel("Year")
    plt.ylabel("Number of Papers")
    plt.title("Number of Papers by Year")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{outdir}/papers_by_year.png")
    plt.close()

    # Top journals
    top_journals = (
        df["journal"]
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={"index": "journal", "journal": "n_papers"})
    )
    top_journals.to_csv(f"{outdir}/top_journals.csv", index=False)

if __name__ == "__main__":
    main()