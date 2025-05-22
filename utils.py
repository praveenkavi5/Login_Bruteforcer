import os
import random
import requests

WORDLISTS = {
    "rockyou.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou.txt",
    "usernames.txt": "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/98.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def update_wordlists(folder="wordlists"):
    os.makedirs(folder, exist_ok=True)
    for name, url in WORDLISTS.items():
        path = os.path.join(folder, name)
        try:
            print(f"[+] Downloading latest {name}...")
            res = requests.get(url, timeout=15)
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(res.text)
            print(f"[+] Saved to {path}")
        except Exception as e:
            print(f"[!] Failed to update {name}: {e}")

def get_random_user_agent():
    return random.choice(USER_AGENTS)

