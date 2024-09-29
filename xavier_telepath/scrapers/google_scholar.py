import requests
import re
from parsel import Selector
import pandas as pd
import os


class GoogleScholar:
    def __init__(self):
        # Default headers for all requests
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
        }
        self.base_url_citations = "https://scholar.google.com/citations"
        self.base_url_article = "https://scholar.google.com/scholar"
    # Utility method for fetching the HTML content
    def _fetch_html(self, params, look_for: str = "citations"):
        try:
            if look_for == "citations":
                response = requests.get(self.base_url_citations, params=params, headers=self.headers, timeout=30)
                return Selector(response.text)
            elif look_for == "articles":
                response = requests.get(self.base_url_article, params=params, headers=self.headers, timeout=30)
                return Selector(response.text)
            else:
                return None
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None

    # Method to find professors by university and field label
    def findProfessorByUniversity(self, label: str, university_name: str, number_of_iterations: int = 10) -> list:
        params = {
            "view_op": "search_authors",  # Search for authors
            "mauthors": f'label:{label} "{university_name}"',  # Search query by label and university
            "hl": "en",  # Set language to English
            "astart": 0  # Starting page for pagination
        }
        iteration_count = 0
        profile_results = []
        profiles_is_present = True

        # Loop through multiple pages (pagination)
        while profiles_is_present and iteration_count < number_of_iterations:
            print(f"Extracting authors from page #{params['astart']}")
            select = self._fetch_html(params)
            if not select:
                break

            # Parse the profiles on the current page
            for profile in select.css(".gs_ai_chpr"):
                name = profile.css(".gs_ai_name a::text").get()
                link = f"https://scholar.google.com{profile.css('.gs_ai_name a::attr(href)').get()}"
                affiliations = profile.css(".gs_ai_aff").xpath('normalize-space()').get()
                email = profile.css(".gs_ai_eml::text").get()
                cited_by = profile.css(".gs_ai_cby::text").get()  # Cited by <count>
                interests = profile.css(".gs_ai_one_int::text").getall()

                profile_results.append({
                    "name": name,
                    "link": link,
                    "affiliations": affiliations,
                    "email": email,
                    "cited_by": cited_by,
                    "interests": interests
                })

            # Check if there is a next page
            if select.css("button.gs_btnPR::attr(onclick)").get():
                next_page_token = re.search(r"after_author\\x3d(.*)\\x26",
                                            select.css("button.gs_btnPR::attr(onclick)").get())
                if next_page_token:
                    params["after_author"] = next_page_token.group(1)  # Pagination token
                    params["astart"] += 10  # Move to the next page
                    iteration_count += 1
                else:
                    profiles_is_present = False
            else:
                profiles_is_present = False

        return profile_results

    # Method to find professors by field of study
    def findProfessorByField(self, field: str, number_of_iterations: int = 10) -> list:
        return self.findProfessorByUniversity(label="", university_name=f"{field}",
                                              number_of_iterations=number_of_iterations)

    # Method to find professors by name
    def findProfessorByName(self, name: str) -> list:
        params = {
            "view_op": "search_authors",  # Search for authors
            "mauthors": f'"{name}"',  # Search query by professor name
            "hl": "en",  # Set language to English
            "astart": 0  # Starting page for pagination
        }
        return self._extract_profiles(params)

    # Method to find professor by Google Scholar ID (profile link)
    def findProfessorByID(self, scholar_id: str) -> dict:
        profile_url = f"https://scholar.google.com/citations?hl=en&user={scholar_id}"
        select = self._fetch_html({"user": scholar_id, "hl": "en"})
        if not select:
            return {}

        name = select.css("#gsc_prf_in::text").get()
        affiliations = select.css(".gsc_prf_il::text").get()
        interests = select.css(".gsc_prf_inta .gsc_prf_inta::text").getall()
        cited_by = select.css("#gsc_rsb_st .gsc_rsb_std::text").get()

        return {
            "name": name,
            "affiliations": affiliations,
            "interests": interests,
            "cited_by": cited_by
        }

    # Method to find articles by professor's name
    # Method to find articles by professor's name
    def findArticleByProfessorName(self, professor_name: str, number_of_iterations: int = 2) -> list:
        """
        Find articles by a professor's name.

        :param professor_name: Name of the professor to search for.
        :param number_of_iterations: Number of pages to iterate through (pagination).
        :return: List of articles (with title, link, authors, and journal).
        """
        query = f'"{professor_name}"'
        return self._find_articles(query, number_of_iterations)

    # Method to find articles by field
    def findArticleByField(self, field: str, number_of_iterations: int = 2) -> list:
        """
        Find articles by a specific field of study.

        :param field: Field of study to search for.
        :param number_of_iterations: Number of pages to iterate through (pagination).
        :return: List of articles (with title, link, authors, and journal).
        """
        return self._find_articles(field, number_of_iterations)

    # Internal utility to find articles based on query
    def _find_articles(self, query: str, number_of_iterations: int) -> list:
        """
        Internal utility to find articles based on a query.

        :param query: The query string (field or professor's name).
        :param number_of_iterations: Number of pages to iterate through (pagination).
        :return: List of articles (with title, link, authors, and journal).
        """
        article_results = []


        for page in range(number_of_iterations):
            params = {
                "q": query,
                "hl": "en",
                "start": page * 10,  # Pagination: 10 results per page
                "as_sdt": "0,5"
            }

            # Fetch the HTML content
            select = self._fetch_html(params, "articles")
            if not select:
                break  # Stop if no more results

            # Extract article info from the div.gs_ri
            for article in select.css(".gs_ri"):
                title = "".join(article.css(".gs_rt a").xpath(".//text()").getall()).replace("\"", "")
                link = article.css(".gs_rt a::attr(href)").get()
                authors_journal = article.css(".gs_a").xpath('normalize-space()').get()

                # Split the authors and journal info
                authors = authors_journal.split(" - ")[0]
                journal_info = authors_journal.split(" - ")[1] if len(authors_journal.split(" - ")) > 1 else None

                article_results.append({
                    "title": title,
                    "link": link,
                    "authors": authors,
                    "journal_info": journal_info
                })

        return article_results

    # Internal utility to extract profiles
    def _extract_profiles(self, params):
        profile_results = []
        select = self._fetch_html(params)
        if not select:
            return profile_results

        for profile in select.css(".gs_ai_chpr"):
            name = profile.css(".gs_ai_name a::text").get()
            link = f"https://scholar.google.com{profile.css('.gs_ai_name a::attr(href)').get()}"
            affiliations = profile.css(".gs_ai_aff").xpath('normalize-space()').get()
            email = profile.css(".gs_ai_eml::text").get()
            cited_by = profile.css(".gs_ai_cby::text").get()
            interests = profile.css(".gs_ai_one_int::text").getall()

            profile_results.append({
                "name": name,
                "link": link,
                "affiliations": affiliations,
                "email": email,
                "cited_by": cited_by,
                "interests": interests
            })
        return profile_results


    # Method to save data to a CSV if a path is provided
    def _save_to_csv(self, data: list, path: str):
        # Ensure the directory exists
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Save the DataFrame to the specified CSV path
        df.to_csv(path, index=False)
        print(f"Data saved to {path}")

    # 1. Save professors by university to CSV
    def findProfessorByUniversityAndSave(self, label: str, university_name: str, path: str,
                                         number_of_iterations: int = 10):
        data = self.findProfessorByUniversity(label, university_name, number_of_iterations)
        self._save_to_csv(data, path)

    # 2. Save professors by field to CSV
    def findProfessorByFieldAndSave(self, field: str, path: str, number_of_iterations: int = 10):
        data = self.findProfessorByField(field, number_of_iterations)
        self._save_to_csv(data, path)

    # 3. Save professor by name to CSV
    def findProfessorByNameAndSave(self, name: str, path: str):
        data = self.findProfessorByName(name)
        self._save_to_csv(data, path)

    # 4. Save professor by Google Scholar ID to CSV
    def findProfessorByIDAndSave(self, scholar_id: str, path: str):
        data = [self.findProfessorByID(scholar_id)]  # Wrap the dict in a list to save as a single row
        self._save_to_csv(data, path)

    # 5. Save articles by professor's name to CSV
    def findArticleByProfessorNameAndSave(self, professor_name: str, path: str, number_of_iterations = 2):
        data = self.findArticleByProfessorName(professor_name, number_of_iterations)
        self._save_to_csv(data, path)

    # 6. Save articles by field to CSV
    def findArticleByFieldAndSave(self, field: str, path: str, number_of_iterations = 2):
        data = self.findArticleByField(field, number_of_iterations)
        self._save_to_csv(data, path)


if __name__ == '__main__':
    # Initialize the GoogleScholar object
    scholar = GoogleScholar()

    # Save professors by university to CSV
    scholar.findProfessorByUniversityAndSave(label="physics", university_name="Harvard University",
                                             path="./professors_harvard.csv")

    # Save professors by field to CSV
    scholar.findProfessorByFieldAndSave(field="quantum computing", path="./professors_quantum.csv")

    # Save a specific professor by name to CSV
    scholar.findProfessorByNameAndSave(name="John Doe", path="./professor_john_doe.csv")

    # Save a professor by Google Scholar ID to CSV
    scholar.findProfessorByIDAndSave(scholar_id="scholarID", path="./professor_scholar_id.csv")

    # Save articles by professor name to CSV
    scholar.findArticleByProfessorNameAndSave(professor_name="Carlo Rovelli", path="./articles_john_doe.csv", number_of_iterations=10)

    # Save articles by field to CSV
    scholar.findArticleByFieldAndSave(field="Category Theory", path="./articles_ai.csv", number_of_iterations= 10)

