# Xavier Telepath

Xavier Telepath is the data gathering component of the Xavier project. It is responsible for collecting raw data about researchers, their publications, and affiliations from various academic sources.

## Components

### 1. Scrapers

Located in `xavier_telepath/scrapers/`, this directory contains scrapers for different data sources:

- `scopus_scraper.py`: Interfaces with the Scopus API to fetch comprehensive publication data.
- `google_scholar_scraper.py`: Scrapes Google Scholar profiles for researcher information and publications.
- `orcid_scraper.py`: Utilizes the ORCID API to retrieve researcher profiles and publication lists.
- `arxiv_scraper.py`: Fetches preprints and e-prints from the arXiv API.
- `researchgate_scraper.py`: Scrapes ResearchGate profiles for researcher information and publications.

### 2. Data Collection

Located in `xavier_telepath/data_collection/`, this directory manages the data collection process:

- `api_integrations.py`: Handles API authentication, rate limiting, and request management for various sources.
- `web_crawling.py`: Implements web crawling techniques for sources without official APIs.

### 3. Storage

Located in `xavier_telepath/storage/`, this directory manages data storage:

- `data_storage.py`: Handles the storage of raw data in appropriate formats (e.g., JSON, CSV) and interfaces with the database.

## Usage

To use Xavier Telepath:

1. Ensure all required API keys and credentials are set in the `.env` file.
2. Run the main Telepath script:

```
python -m xavier_telepath
```

This will initiate the data gathering process from all configured sources.

## Configuration

Adjust the `config.py` file to set:

- Target data sources
- Data collection frequency
- Storage preferences

## Note

Ensure that you comply with the terms of service of all data sources and respect rate limits to avoid being blocked.