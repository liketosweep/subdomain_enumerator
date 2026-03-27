import socket

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
    print(f"[+] Resolving {len(subdomains)} subdomains...\n")
    resolved = []
    for sub in subdomains:
        result = resolve_subdomain(sub)
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