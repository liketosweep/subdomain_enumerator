import socket
import random
import string
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests
import json

def get_subdomains_crtsh(domain):   
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except:
        return []
    subdomains = set()
    for entry in data:
        name = entry.get("name_value", "")
        for sub in name.split("\n"):
            if domain in sub:
                subdomains.add(sub.strip())
    return list(subdomains)


def probe_http(subdomain):
    urls = [
        f"https://{subdomain}",
        f"http://{subdomain}"
    ]
    for url in urls:
        try:
            response = requests.get(url, timeout=3)
            return (subdomain, url, response.status_code)
        except requests.RequestException:
            continue
    return None


def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {path}")
        return []


def generate_subdomains(domain, words, max_permutations=10000):
    subdomains = set()
    for word in words:
        subdomains.add(f"{word}.{domain}")
    count = 0
    for w1 in words:
        for w2 in words:
            if w1 != w2:
                subdomains.add(f"{w1}-{w2}.{domain}")
                count += 1
                if count >= max_permutations:
                    return list(subdomains)
    return list(subdomains)


def resolve_subdomain(subdomain, retries=2):
    for _ in range(retries):
        try:
            ip = socket.gethostbyname(subdomain)
            return (subdomain, ip)
        except socket.gaierror:
            continue
    return None


def generate_random_subdomain(domain):
    rand = ''.join(random.choices(string.ascii_lowercase, k=12))
    return f"{rand}.{domain}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", required=True)
    parser.add_argument("-w", "--wordlist", required=True)
    parser.add_argument("-o", "--output", default="resolved.txt")
    parser.add_argument("-t", "--threads", type=int, default=100)
    parser.add_argument("--passive", action="store_true")
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    words = load_wordlist(args.wordlist)
    if not words:
        return
    print("[+] Generating subdomains...\n")
    generated_subs = generate_subdomains(args.domain, words)
    print("[+] Fetching passive subdomains from crt.sh...\n")
    crt_subs = []
    if args.passive:
        print("[+] Fetching passive subdomains from crt.sh...\n")
        crt_subs = get_subdomains_crtsh(args.domain)
        print(f"[+] Found {len(crt_subs)} passive subdomains\n")
    subdomains = list(set(generated_subs + crt_subs))
    print(f"[+] Generated {len(subdomains)} subdomains\n")
    test_sub = generate_random_subdomain(args.domain)
    wildcard_result = resolve_subdomain(test_sub)
    wildcard_ip = None
    if wildcard_result:
        wildcard_ip = wildcard_result[1]
        print(f"[!] Wildcard detected -> {wildcard_ip}\n")
    else:
        print("[+] No wildcard detected\n")
    print("[+] Resolving...\n")
    resolved = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(resolve_subdomain, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            result = future.result()
            if result:
                subdomain, ip = result
                if wildcard_ip and ip == wildcard_ip:
                    continue
                if args.probe:
                    probe_result = probe_http(subdomain)
                    if probe_result:
                        sub, url, status = probe_result
                        if status not in [200, 301, 302, 403]:
                            continue
                        print(f"[+] {sub} -> {url} [{status}]")
                        resolved.append({
                        "subdomain": sub,
                        "url": url,
                        "status": status
                        })
                else:
                    print(f"[+] {subdomain} -> {ip}")
                    resolved.append({
                    "subdomain": subdomain,
                    "ip": ip
                    })
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        if args.json:
            json.dump(resolved, f, indent=2)
        else:
            for entry in resolved:
                if "url" in entry:
                    f.write(f"{entry['subdomain']} -> {entry['url']} [{entry['status']}]\n")
                else:
                    f.write(f"{entry['subdomain']} -> {entry['ip']}\n")

if __name__ == "__main__":
    main()