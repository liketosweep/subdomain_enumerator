import socket
import random
import string
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

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
    args = parser.parse_args()
    words = load_wordlist(args.wordlist)
    if not words:
        return
    print("[+] Generating subdomains...\n")
    subdomains = generate_subdomains(args.domain, words)
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
                print(f"[+] {subdomain} -> {ip}")
                resolved.append(f"{subdomain} -> {ip}")
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        for line in resolved:
            f.write(line + "\n")
    print(f"\n[+] Resolved {len(resolved)} valid subdomains")
    print(f"[+] Saved to {args.output}")

if __name__ == "__main__":
    main()