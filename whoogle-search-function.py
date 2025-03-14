import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Whoogle instance URL (fixed typo)
WHOOGLE_URL = "http://localhost:5000/search"

def whoogle_search(team, month, year, pages=20, max_results = 50):
    """Search Whoogle for news articles about a football team from a specific month and year."""

    query = f"{team} Serie A {month}-{year} site:gazzetta.it"

    params = {
        "q": query,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_links = []

    # Fetch 5 pages to gather enough results
    try:
        response = requests.get(WHOOGLE_URL, params=params, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch: {e}")

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find <a> elements with class="fuLhoc ZWRArf"
    link_elements = soup.find_all("a", class_="fuLhoc ZWRArf")

    # Extract and filter links
    for element in link_elements:
        href = element.get("href", "")
        if href.startswith(f"https://www.gazzetta.it/Calcio/Serie-A/{team}"):
            all_links.append(href)
        if len(all_links) >= max_results:  # Stop at max_results (default 50)
            break

    # Limit to max_results
    all_links = all_links[:max_results]

    # Convert to JSON
    json_data = json.dumps(all_links, indent=4, ensure_ascii=False)

    # Print the JSON
    print(json_data)

    # Save to a file with team, month, and year in the filename
    filename = f"{team}_{month}_{year}_links.json"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_data)

    print(f"Saved {len(all_links)} links to {filename}")

# Example Usage
whoogle_search("Atalanta", "01", "2025")