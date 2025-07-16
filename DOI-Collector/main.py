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
    """Count how many DOIs are stored (excluding the project name line)."""
    try:
        with open(dois_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            return len(lines) - 1 if lines else 0
    except FileNotFoundError:
        return 0

def ensure_project_name(dois_file, snapshots_file):
    """Ensure both files exist and start with 'project name:'."""
    def check_or_set_project(file_path, project_name=None):
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            if not project_name:
                project_name = input("Enter project name: ").strip()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"project name: {project_name}\n")
            return project_name

        with open(file_path, "r+", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if not first_line.lower().startswith("project name:"):
                if not project_name:
                    project_name = input("Enter project name: ").strip()
                rest = f.read()
                f.seek(0)
                f.write(f"project name: {project_name}\n")
                f.write(rest)
        return project_name

    project_name = check_or_set_project(dois_file)
    check_or_set_project(snapshots_file, project_name)

def add_doi(dois_file, snapshots_file):
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
        with open(dois_file, "r", encoding="utf-8") as f:
            existing_dois = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        existing_dois = set()

    if doi in existing_dois:
        print("⚠️ This DOI already exists in the file.")
        print(f"📊 Total DOIs stored: {len(existing_dois)-1}")  # subtract project name
        return

    title, abstract = fetch_metadata(doi)
    if not title:
        print("❌ Invalid DOI or metadata not found. Nothing was saved.")
        print(f"📊 Total DOIs stored: {len(existing_dois)-1}")
        return

    print(f"\n📄 Title: {title}")
    print(f"\n📝 Abstract: {abstract}\n")

    with open(dois_file, "a", encoding="utf-8") as f:
        f.write(doi + "\n")

    with open(snapshots_file, "a", encoding="utf-8") as f:
        f.write("DOI: " + doi + "\n")
        f.write("Title: " + (title or "N/A") + "\n")
        f.write("Abstract: " + (abstract or "N/A") + "\n")
        f.write("-" * 80 + "\n") 

    total_dois = count_dois(dois_file)
    print("✅ DOI and snapshot added successfully.")
    print(f"📊 Total DOIs stored: {total_dois}")

if __name__ == "__main__":
    dois_file = os.path.join("data", "dois.txt")
    snapshots_file = os.path.join("data", "paper_snapshots.txt")

    ensure_project_name(dois_file, snapshots_file)

    print(f"📊 Starting with {count_dois(dois_file)} DOIs stored.\n")

    while True:
        add_doi(dois_file, snapshots_file)
        again = input("Do you want to add another DOI? (y/n): ").strip().lower()
        if again != "y":
            break
