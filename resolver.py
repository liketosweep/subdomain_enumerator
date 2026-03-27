import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def resolve_subdomain(subdomain, retries=2):
    for _ in range(retries):
        try:
            ip = socket.gethostbyname(subdomain)
            return (subdomain, ip)
        except socket.gaierror:
            continue
    return None


def load_subdomains(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {path}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Subdomain Resolver")
    parser.add_argument("-i", "--input", required=True, help="Input file (subdomains)")
    parser.add_argument("-o", "--output", default="resolved.txt", help="Output file")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads")
    args = parser.parse_args()
    subdomains = load_subdomains(args.input)
    if not subdomains:
        print("[!] No subdomains loaded.")
        return
    print(f"[+] Resolving {len(subdomains)} subdomains...\n")
    resolved = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(resolve_subdomain, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            result = future.result()
            if result:
                subdomain, ip = result
                print(f"[+] {subdomain} -> {ip}")
                resolved.append(f"{subdomain} -> {ip}")
    with open(args.output, "w") as f:
        for line in resolved:
            f.write(line + "\n")
    print(f"\n[+] Resolved {len(resolved)} subdomains")
    print(f"[+] Saved to {args.output}")


if __name__ == "__main__":
    main()