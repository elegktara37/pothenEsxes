import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# List of URLs containing PDF links
page_urls = [
    "https://www.hellenicparliament.gr/Organosi-kai-Leitourgia/epitropi-elegxou-ton-oikonomikon-ton-komaton-kai-ton-vouleftwn/Diloseis-Periousiakis-Katastasis2022",
    "https://www.hellenicparliament.gr/Organosi-kai-Leitourgia/epitropi-elegxou-ton-oikonomikon-ton-komaton-kai-ton-vouleftwn/Diloseis-Periousiakis-Katastasis2021",
    "https://www.hellenicparliament.gr/Organosi-kai-Leitourgia/epitropi-elegxou-ton-oikonomikon-ton-komaton-kai-ton-vouleftwn/Diloseis-Periousiakis-Katastasis2020",
    "https://www.hellenicparliament.gr/Organosi-kai-Leitourgia/epitropi-elegxou-ton-oikonomikon-ton-komaton-kai-ton-vouleftwn/Diloseis-Periousiakis-Katastasis2019"
]

# Main download folder
base_folder = "all_downloads"
os.makedirs(base_folder, exist_ok=True)

for page_url in page_urls:
    # Extract domain or unique identifier from the URL for folder naming
    url_parts = urlparse(page_url)
    site_folder = os.path.join(base_folder, f"{url_parts.netloc}_{url_parts.path.strip('/').replace('/', '_')}")
    os.makedirs(site_folder, exist_ok=True)

    print(f"\nFetching PDFs from: {page_url}")

    # Fetch the webpage content
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch {page_url}")
        continue

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all PDF links
    pdf_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".pdf"):
            if href.startswith("http"):
                pdf_links.append(href)
            else:
                pdf_links.append(page_url + href)  # Handle relative URLs

    # Download PDFs into the respective folder
    for pdf_url in pdf_links:
        pdf_name = os.path.join(site_folder, pdf_url.split("/")[-1])

        if os.path.exists(pdf_name):  # Skip if file already exists
            print(f"Skipping {pdf_name}, already exists.")
            continue

        print(f"Downloading {pdf_url} into {site_folder}...")
        pdf_response = requests.get(pdf_url)
        with open(pdf_name, "wb") as pdf_file:
            pdf_file.write(pdf_response.content)

print("\nAll PDFs downloaded (skipping existing ones).")