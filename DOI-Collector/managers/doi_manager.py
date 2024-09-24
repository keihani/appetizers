from managers.metadata_fetcher import MetadataFetcher
from managers.file_manager import FileManager
import os
import requests

class DOIManager:
    """Manages DOIs: validation, adding, and saving."""

    def __init__(self, dois_file, snapshots_file):
        self.dois_file = dois_file
        self.batch_file = os.path.join("data", "batch.txt")
        self.snapshots_file = snapshots_file

    def get_user_input(self):
        """Get keywords and row count from user input."""
        keyword = input("Enter keywords: ").strip()
        try:
            rows = int(input("Enter number of rows: ").strip())
            if rows <= 0:
                rows = 10
        except ValueError:
            rows = 10
        return keyword, rows

    def fetch_dois(self, keyword, rows):
        """Fetch DOIs from CrossRef API."""
        url = f"https://api.crossref.org/works?query={keyword}&rows={rows}"
        response = requests.get(url).json()
        items = response.get("message", {}).get("items", [])
        dois = [item.get("DOI", "") for item in items if "DOI" in item]
        return dois

    def save_dois(self, dois):
        """Append DOIs to file using FileManager."""
        if not dois:
            print("No DOIs found.")
            return
        content = "\n".join(dois) + "\n"
        
        FileManager.append_file(self.batch_file, content)
        print(f"✅ {len(dois)} DOIs saved to {self.batch_file}")

    def auto_lookup(self):
        """Run the workflow."""
        keyword, rows = self.get_user_input()
        dois = self.fetch_dois(keyword, rows)
        self.save_dois(dois)

    @staticmethod
    def clean_doi_prefix(doi: str) -> str:
        """Remove known DOI prefixes and return normalized DOI string."""
        prefixes = [
            "https://doi.org/",
            "https://www.doi.org/",
            "www.doi.org/",
            "doi.org/",
            "/",
            "\\"
        ]
        doi = doi.strip()
        for prefix in prefixes:
            if doi.startswith(prefix):
                doi = doi[len(prefix):]
        return doi.strip()

    def add_doi(self):
        doi = input("Enter DOI link: ").strip()
        doi = self.clean_doi_prefix(doi)

        content = FileManager.read_file(self.dois_file)
        existing_dois = {line.strip() for line in content.splitlines()} if content else set()

        if doi in existing_dois:
            print("⚠️ This DOI already exists in the file.")
            print(f"📊 Total DOIs stored: {len(existing_dois)-1}")  # subtract project name
            return

        title, abstract = MetadataFetcher.fetch_metadata(doi)
        if not title:
            print("❌ Invalid DOI or metadata not found. Nothing was saved.")
            print(f"📊 Total DOIs stored: {len(existing_dois)-1}")
            return

        print(f"\n📄 Title: {title}")
        print(f"\n📝 Abstract: {abstract}\n")

        # Save DOI
        FileManager.append_file(self.dois_file, doi + "\n")

        # Save snapshot
        snapshot = (
            f"DOI: {doi}\n"
            f"Title: {title or 'N/A'}\n"
            f"Abstract: {abstract or 'N/A'}\n"
            + "-" * 80 + "\n"
        )
        FileManager.append_file(self.snapshots_file, snapshot)

        total_dois = FileManager.count_dois(self.dois_file)
        print("✅ DOI and snapshot added successfully.")
        print(f"📊 Total DOIs stored: {total_dois}")

    def batch_input_menu(self):
        print("\nBatch DOI Input Menu")
        print("1. Enter DOIs as a string (separated by ';')")
        print("2. Provide a file address containing DOIs (separated by ';')")
        print("0. Back to main menu")
        choice = input("Select an option: ").strip()

        if choice == "1":
            print("⚠️ Attention: You are responsible for ensuring the accuracy of the information provided.")
            dois = input("Enter DOIs separated by ';': ").strip().replace(";", "\n")
            if not dois:
                print("No input provided.")
            else:
                FileManager.append_file(self.batch_file, dois)
                print(f"DOIs saved to {self.batch_file}")

        elif choice == "2":
            file_path = input("Enter the file path: ").strip()
            content = FileManager.read_file(file_path)

            if content is None:
                print("File not found or empty.")
            else:
                FileManager.append_file(self.batch_file, content)
                print(f"DOIs from file saved to {self.batch_file}")

        elif choice == "0":
            return

        else:
            print("Invalid option.")

        input("\nPress Enter to return to the menu...")
