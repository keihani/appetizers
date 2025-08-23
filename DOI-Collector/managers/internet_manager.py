import requests

class InternetManager:
    """Handles internet connectivity checks."""

    @staticmethod
    def check_internet():
        """Check internet connection by pinging CrossRef API."""
        url = "https://api.crossref.org/works/10.1038/nphys1170"  # Known DOI
        try:
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    @classmethod
    def wait_for_internet(cls):
        """Wait until internet connection is available."""
        while not cls.check_internet():
            print("⚠️ No internet connection detected. Please connect to the internet.")
            input("Press ENTER after connecting to retry...")
        print("✅ Internet connection verified.\n")
