
import requests
import re
import sys

def get_gifs(query):
    url = f"https://tenor.com/search/{query}-gifs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        # Look for media.tenor.com urls in src attributes
        # Pattern: src="https://media.tenor.com/..."
        # Tenor often uses data-src or inside JSON
        # Let's simple regex for any media.tenor.com gif
        pattern = r'https://media\.tenor\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+\.gif'
        urls = re.findall(pattern, html)
        return list(set(urls)) # Deduplicate
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

keywords = ["hello-kitty", "hello-kitty-sad", "hello-kitty-happy", "hello-kitty-angry", "hello-kitty-confused", "hello-kitty-crying"]
all_urls = {}

for kw in keywords:
    print(f"Scanning {kw}...")
    found = get_gifs(kw)
    print(f"Found {len(found)} GIFs for {kw}")
    all_urls[kw] = found[:5] # Keep top 5

with open("gifs.txt", "w", encoding="utf-8") as f:
    f.write("\n--- RESULTS ---\n")
    for kw, urls in all_urls.items():
        f.write(f"\nCategory: {kw}\n")
        for u in urls:
            f.write(u + "\n")
print("Results written to gifs.txt")
