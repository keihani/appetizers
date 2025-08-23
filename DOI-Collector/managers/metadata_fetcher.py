import requests

class MetadataFetcher:
    """Fetches metadata from CrossRef."""

    @staticmethod
    def fetch_metadata(doi: str):
        """Fetch title and abstract using CrossRef API."""
        url = f"https://api.crossref.org/works/{doi}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()["message"]
                title = data.get("title", ["No title found"])[0]
                abstract = data.get("abstract", "No abstract found")
                return title, abstract
        except requests.RequestException as e:
            print(f"⚠️ Request error: {e}")
        return None, None
