import requests
import xml.etree.ElementTree as ET
import csv


class ArxivAPI:
    BASE_URL = "http://export.arxiv.org/api/query"

    # Search types with their corresponding arXiv query labels
    SEARCH_FIELDS = {
        "title": "ti",
        "author": "au",
        "abstract": "abs",
        "doi": "doi",
        "orcid": "orcid",
        "arxiv_id": "id",
        "all": ""
    }

    def __init__(self, max_results=10):
        self.max_results = max_results

    def search(self, field, query, subject=None, start_index=0):
        """
        Search arXiv by a specific field and optionally in a specific subject area.

        Parameters:
        - field: The field to search by (title, author, abstract, etc.)
        - query: The search term
        - subject: The arXiv subject category (e.g., 'astro-ph', 'gr-qc') (optional)
        - start_index: The starting index for paginated results

        Returns:
        - A list of dictionaries containing paper information
        """
        if field not in self.SEARCH_FIELDS:
            raise ValueError(f"Invalid search field. Valid options are: {list(self.SEARCH_FIELDS.keys())}")

        field_query = self.SEARCH_FIELDS[field]
        full_query = f"{field_query}:{query}" if field_query else query

        if subject:
            full_query += f"+AND+cat:{subject}"

        params = {
            "search_query": full_query,
            "start": start_index,
            "max_results": self.max_results
        }


        response = requests.get(self.BASE_URL, params=params)

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")


        return self.parse_response(response.content)

    def parse_response(self, xml_data):
        """
        Parse the arXiv XML response.

        Parameters:
        - xml_data: The XML content to parse

        Returns:
        - A list of dictionaries, each representing a paper
        """
        root = ET.fromstring(xml_data)
        namespace = {"atom": "http://www.w3.org/2005/Atom"}
        papers = []

        for entry in root.findall("atom:entry", namespace):
            paper = {
                "id": entry.find("atom:id", namespace).text.split("/")[-1],  # Extract arXiv ID from the URL
                "title": entry.find("atom:title", namespace).text.strip(),
                "authors": [author.find("atom:name", namespace).text for author in
                            entry.findall("atom:author", namespace)],
                "published": entry.find("atom:published", namespace).text,
                "updated": entry.find("atom:updated", namespace).text,
                "summary": entry.find("atom:summary", namespace).text.strip().replace("\n", " "),
            }
            papers.append(paper)

        return papers

    def save_to_csv(self, papers, file_path):
        """
        Save the list of papers to a CSV file.

        Parameters:
        - papers: A list of dictionaries, each representing a paper.
        - file_path: The path where the CSV file will be saved.
        """
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "title", "authors", "published", "updated", "summary"])
            writer.writeheader()
            for paper in papers:
                paper['authors'] = ' / '.join(paper['authors'])
                writer.writerow(paper)



if __name__ == "__main__":
    arxiv = ArxivAPI(max_results=10)

    # Search by title in quantum computing, and limit search to the 'quant-ph' subject
    papers = arxiv.search(field="author", query="K. Azizi")

    # Save the search results to a CSV file
    arxiv.save_to_csv(papers, "arxiv_data.csv")

    # Display search results
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {paper['authors']}")
        print(f"Published: {paper['published']}")
        print(f"arXiv ID: {paper['id']}")
        print(f"Summary: {paper['summary'][:200]}...")  # print a snippet of the summary
        print("-" * 80)
