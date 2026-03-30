# Subdomain Enumerator

A fast and modular subdomain enumeration tool built in Python.
It combines active and passive techniques to discover and validate subdomains.

---

## 🚀 Features

* Wordlist-based subdomain generation
* Permutation support (e.g. dev-api.domain.com)
* Passive enumeration via crt.sh
* Multi-threaded DNS resolution
* Wildcard DNS detection and filtering
* HTTP probing (detect live services)
* Status code filtering (200, 301, 302, 403)
* JSON and plain text output
* CLI-based usage with flexible flags

---

## ⚙️ Installation

```bash
git clone https://github.com/liketosweep/subdomain-enumerator.git
cd subdomain-enumerator
pip install -r requirements.txt
```

---

## 📌 Usage

```bash
python main.py -d <domain> -w <wordlist> [options]
```

---

## 🔧 Options

| Flag        | Description                         |
| ----------- | ----------------------------------- |
| `-d`        | Target domain                       |
| `-w`        | Wordlist file                       |
| `-o`        | Output file                         |
| `-t`        | Number of threads (default: 100)    |
| `--passive` | Enable passive enumeration (crt.sh) |
| `--probe`   | Enable HTTP probing                 |
| `--json`    | Save output in JSON format          |

---

## 📊 Examples

### Basic scan

```bash
python main.py -d example.com -w wordlist.txt
```

### With passive enumeration

```bash
python main.py -d example.com -w wordlist.txt --passive
```

### Full scan (recommended)

```bash
python main.py -d example.com -w wordlist.txt --passive --probe --json -o output/results.json
```

---

## 📂 Project Structure

```
subdomain-enumerator/
│
├── main.py
├── wordlist.txt
├── requirements.txt
├── README.md
└── output/
```

---

## 📸 Sample Output

```
[+] Generating subdomains...

[+] Fetching passive subdomains from crt.sh...

[+] Found 399 passive subdomains

[+] Generated 478 subdomains

[+] No wildcard detected

[+] Resolving...

[+] www.example.com -> http://www.example.com [200]

[+] Final valid targets: 1
```

---

## 🧠 How It Works

1. Generates subdomains using a wordlist and permutations
2. Fetches real subdomains from crt.sh (optional)
3. Merges and deduplicates results
4. Filters invalid domain names
5. Resolves subdomains using DNS
6. Filters wildcard responses
7. Probes HTTP/HTTPS services (optional)
8. Outputs clean, validated results

---

## ⚠️ Limitations

* Limited passive sources (only crt.sh)
* Depends on wordlist quality
* Basic HTTP probing (no deep scanning)

---

## 🔮 Future Improvements

* Additional passive sources (Wayback, SecurityTrails)
* Advanced permutation engine
* Rate limiting and retries tuning
* Colored CLI output
* Integration with tools like httpx

---

## 📜 License

MIT License
