# -----------------------------------------------------------------------------
# Copyright (c) 2025 Kevin Keihani
# GitHub: https://github.com/keihani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import requests
import os

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


def count_dois(dois_file):
    """Count how many DOIs are stored."""
    try:
        with open(dois_file, "r", encoding="utf-8") as f:
            return sum(1 for line in f if line.strip())
    except FileNotFoundError:
        return 0


def add_doi(dois_file, snapshots_file):
    # Get DOI input from user
    doi = input("Enter DOI link: ").strip()
    # Remove known prefixes from the start
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

    # Read existing DOIs from file (if file exists)
    try:
        with open(dois_file, "r", encoding="utf-8") as f:
            existing_dois = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        existing_dois = set()

    # Check duplication
    if doi in existing_dois:
        print("⚠️ This DOI already exists in the file.")
        print(f"📊 Total DOIs stored: {len(existing_dois)}")
        return

    # Fetch metadata
    title, abstract = fetch_metadata(doi)
    if not title:
        print("❌ Invalid DOI or metadata not found. Nothing was saved.")
        print(f"📊 Total DOIs stored: {len(existing_dois)}")
        return

    # Show metadata
    print(f"\n📄 Title: {title}")
    print(f"\n📝 Abstract: {abstract}\n")

    # Save DOI to list
    with open(dois_file, "a", encoding="utf-8") as f:
        f.write(doi + "\n")

    # Save snapshot (DOI + Title + Abstract)
    with open(snapshots_file, "a", encoding="utf-8") as f:
        f.write("DOI: " + doi + "\n")
        f.write("Title: " + (title or "N/A") + "\n")
        f.write("Abstract: " + (abstract or "N/A") + "\n")
        f.write("-" * 80 + "\n")  # separator line

    total_dois = count_dois(dois_file)
    print("✅ DOI and snapshot added successfully.")
    print(f"📊 Total DOIs stored: {total_dois}")


if __name__ == "__main__":
    dois_file = os.path.join("data", "dois.txt")
    snapshots_file = os.path.join("data", "paper_snapshots.txt")

    # Show count at program start
    print(f"📊 Starting with {count_dois(dois_file)} DOIs stored.\n")

    while True:
        add_doi(dois_file, snapshots_file)
        again = input("Do you want to add another DOI? (y/n): ").strip().lower()
        if again != "y":
            break
