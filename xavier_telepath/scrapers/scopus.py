import requests
import json
import csv


class ScopusAPI:
    BASE_URL = "https://api.elsevier.com/content/"

    def __init__(self, api_key, max_results=10):
        self.api_key = api_key
        self.max_results = max_results
        self.headers = {"X-ELS-APIKey": self.api_key}

    def search_articles(self, field, query, subject=None, start_index=0):
        """
        Search for articles based on a field like title, abstract, etc. and filter by subject.

        Parameters:
        - field: The field to search by (e.g., 'title', 'keywords')
        - query: The search term
        - subject: The subject area (e.g., 'astro-ph', 'gr-qc')
        - start_index: The starting index for paginated results

        Returns:
        - A list of dictionaries containing article information
        """
        url = f"{self.BASE_URL}search/scopus"
        query_str = f"{field}({query})"

        if subject:
            query_str += f" AND SUBJAREA({subject})"  # Add subject to the query

        params = {
            "query": query_str,
            "start": start_index,
            "count": self.max_results
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")

        data = response.json()
        return self.parse_article_results(data)

    def search_people(self, query, start_index=0):
        """
        Search for authors based on a query (name, ORCID, etc.)

        Parameters:
        - query: The search term (e.g., author's name or ORCID)
        - start_index: The starting index for paginated results

        Returns:
        - A list of dictionaries containing author information
        """
        url = f"{self.BASE_URL}content/author"
        params = {
            "query": query,
            "start": start_index,
            "count": self.max_results
        }

        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve data: {response.status_code}")

        data = response.json()
        return self.parse_people_results(data)

    def parse_article_results(self, data):
        """
        Parse the results from the Scopus Search API for articles.

        Parameters:
        - data: The JSON response from the API

        Returns:
        - A list of dictionaries, each representing an article
        """
        entries = data.get('search-results', {}).get('entry', [])
        articles = []

        for entry in entries:
            article = {
                'title': entry.get('dc:title'),
                'authors': entry.get('dc:creator'),
                'publication_name': entry.get('prism:publicationName'),
                'doi': entry.get('prism:doi'),
                'scopus_id': entry.get('dc:identifier'),
                'abstract': entry.get('dc:description'),
                'publication_date': entry.get('prism:coverDate'),
            }
            articles.append(article)

        return articles

    def parse_people_results(self, data):
        """
        Parse the results from the Scopus Author Search API.

        Parameters:
        - data: The JSON response from the API

        Returns:
        - A list of dictionaries, each representing an author
        """
        entries = data.get('search-results', {}).get('entry', [])
        people = []

        for entry in entries:
            person = {
                'name': entry.get('preferred-name', {}).get('surname') + ', ' + entry.get('preferred-name', {}).get(
                    'given-name'),
                'affiliation': entry.get('affiliation-current', {}).get('affiliation-name'),
                'orcid': entry.get('orcid'),
                'scopus_id': entry.get('dc:identifier'),
                'email': entry.get('author-profile', {}).get('author-email'),
                'research_areas': entry.get('subject-area', [])
            }
            people.append(person)

        return people

    def save_to_csv(self, data, file_path, data_type="articles"):
        """
        Save the search results to a CSV file.

        Parameters:
        - data: A list of dictionaries (articles or author information).
        - file_path: The path where the CSV file will be saved.
        - data_type: Type of data to save ('articles' or 'people').
        """
        if data_type == "articles":
            fieldnames = ["scopus_id", "title", "authors", "publication_name", "doi", "abstract", "publication_date"]
        elif data_type == "people":
            fieldnames = ["scopus_id", "name", "affiliation", "orcid", "email", "research_areas"]
        else:
            raise ValueError("Invalid data_type. Expected 'articles' or 'people'.")

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                if data_type == "people":
                    # Join research areas for CSV
                    entry['research_areas'] = ', '.join([area.get('$', '') for area in entry.get('research_areas', [])])
                writer.writerow(entry)


# Example usage
if __name__ == "__main__":
    api_key = "93d9ddaaa8f5849a21e722073cf0053b"
    scopus = ScopusAPI(api_key, max_results=2)

    # Search for articles by title in quantum computing within the 'phys' subject
    articles = scopus.search_articles(field="author", query="Roger", subject="PHYS")

    # Save articles to CSV
    scopus.save_to_csv(articles, "scopus_quantum_computing_articles.csv", data_type="articles")

    # # Search for people (authors) by name
    # authors = scopus.search_people(query="Penrose")
    #
    # # Save author information to CSV
    # scopus.save_to_csv(authors, "scopus_authors.csv", data_type="people")

    # Display search results
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"DOI: {article['doi']}")
        print(f"Authors: {article['authors']}")
        print(f"Publication: {article['publication_name']}")
        print("-" * 80)

    # for author in authors:
    #     print(f"Name: {author['name']}")
    #     print(f"Affiliation: {author['affiliation']}")
    #     print(f"ORCID: {author['orcid']}")
    #     print(f"Research Areas: {author['research_areas']}")
    #     print("-" * 80)
