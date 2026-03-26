def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Wordlist not found: {path}")
        return []


def generate_subdomains(domain, words):
    subdomains = set()

    # Single word
    for word in words:
        subdomains.add(f"{word}.{domain}")

    # Two-word permutations
    for w1 in words:
        for w2 in words:
            if w1 != w2:
                subdomains.add(f"{w1}-{w2}.{domain}")

    return list(subdomains)


def main():
    domain = input("Enter target domain: ").strip()
    wordlist_path = input("Enter wordlist path: ").strip()

    words = load_wordlist(wordlist_path)

    if not words:
        print("[!] No words loaded. Exiting.")
        return

    subdomains = generate_subdomains(domain, words)

    print("\n[+] Generated Subdomains:\n")
    for sub in subdomains:
        print(sub)


if __name__ == "__main__":
    main()