from managers.metadata_fetcher import MetadataFetcher
from managers.file_manager import FileManager

class DOIManager:
    """Manages DOIs: validation, adding, and saving."""

    def __init__(self, dois_file, snapshots_file):
        self.dois_file = dois_file
        self.snapshots_file = snapshots_file

    def add_doi(self):
        doi = input("Enter DOI link: ").strip()
        prefixes = [
            "https://doi.org/",
            "https://www.doi.org/",
            "www.doi.org/",
            "doi.org/",
            "/",
            "\\"
        ]
        for prefix in prefixes:
            if doi.startswith(prefix):
                doi = doi[len(prefix):]
        doi = doi.strip()

        try:
            with open(self.dois_file, "r", encoding="utf-8") as f:
                existing_dois = {line.strip() for line in f if line.strip()}
        except FileNotFoundError:
            existing_dois = set()

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

        with open(self.dois_file, "a", encoding="utf-8") as f:
            f.write(doi + "\n")

        with open(self.snapshots_file, "a", encoding="utf-8") as f:
            f.write("DOI: " + doi + "\n")
            f.write("Title: " + (title or "N/A") + "\n")
            f.write("Abstract: " + (abstract or "N/A") + "\n")
            f.write("-" * 80 + "\n")

        total_dois = FileManager.count_dois(self.dois_file)
        print("✅ DOI and snapshot added successfully.")
        print(f"📊 Total DOIs stored: {total_dois}")
