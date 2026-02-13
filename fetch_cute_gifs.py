
import requests
import re
import sys

def get_gifs(query, limit=5):
    url = f"https://tenor.com/search/{query}-gifs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        pattern = r'https://media\.tenor\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+\.gif'
        urls = re.findall(pattern, html)
        return list(set(urls))[:limit]
    except Exception as e:
        sys.stderr.write(f"Error fetching {query}: {e}\n")
        return []

keywords = {
    "normal": ["hello-kitty-cute", "hello-kitty-aesthetic"],
    "confused": ["hello-kitty-confused", "hello-kitty-what"],
    "pleading": ["hello-kitty-pleading", "hello-kitty-please"],
    "sad": ["hello-kitty-sad-aesthetic", "hello-kitty-crying-soft"],
    "sadder": ["hello-kitty-heartbroken", "hello-kitty-devastated"],
    "devastated": ["hello-kitty-sobbing", "hello-kitty-crying-hard"],
    "very_devastated": ["hello-kitty-broken", "hello-kitty-depression"],
    "runaway": ["hello-kitty-running-away", "hello-kitty-leave"],
    "happy": ["hello-kitty-happy-aesthetic", "hello-kitty-celebrating-cute"]
}

with open("cute_gifs.txt", "w", encoding="utf-8") as f:
    f.write("--- CUTE GIF CANDIDATES ---\n")
    for category, queries in keywords.items():
        f.write(f"\n[{category.upper()}]\n")
        seen = set()
        for q in queries:
            print(f"Searching for {q}...")
            urls = get_gifs(q, limit=8)
            for u in urls:
                if u not in seen:
                    f.write(f"{u}\n")
                    seen.add(u)

print("Done! Check cute_gifs.txt")
