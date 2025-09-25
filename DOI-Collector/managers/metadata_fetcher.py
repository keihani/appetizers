# DOI-Collector
# SPDX-License-Identifier: MIT
#
# Author: Kevin Keihani
# Company: Soroush Fanavari Co
# Contact: yz.keihani@gmail.com
# GitHub:  https://github.com/keihani
# LinkedIn: https://linkedin.com/in/keihani
#
# This file is part of DOI-Collector, an open source project.

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
                data = response.json().get("message", {})

                # Handle title safely
                titles = data.get("title", [])
                title = titles[0] if titles else "No title found"

                # Handle abstract safely
                abstract = data.get("abstract") or "No abstract found"

                return title, abstract
        except requests.RequestException as e:
            print(f"⚠️ Request error: {e}")
        return None, None
