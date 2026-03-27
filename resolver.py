import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def resolve_subdomain(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return (subdomain, ip)
    except socket.gaierror:
        return None


def load_subdomains(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {path}")
        return []


def main():
    input_file = input("Enter subdomains file: ").strip()
    output_file = input("Enter output file (default: resolved.txt): ").strip()
    if not output_file:
        output_file = "resolved.txt"
    subdomains = load_subdomains(input_file)
    if not subdomains:
        print("[!] No subdomains loaded.")
        return
    print(f"[+] Resolving {len(subdomains)} subdomains with threads...\n")
    resolved = []
    #  Thread pool
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(resolve_subdomain, sub): sub for sub in subdomains}
        for future in as_completed(futures):
            result = future.result()
            if result:
                subdomain, ip = result
                print(f"[+] {subdomain} -> {ip}")
                resolved.append(f"{subdomain} -> {ip}")
    # Save results
    with open(output_file, "w") as f:
        for line in resolved:
            f.write(line + "\n")
    print(f"\n[+] Resolved {len(resolved)} subdomains")
    print(f"[+] Saved to {output_file}")


if __name__ == "__main__":
    main()