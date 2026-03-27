# Subdomain Enumerator

A fast and simple subdomain enumeration tool built in Python.
It generates possible subdomains using a wordlist and validates them via DNS resolution.

---

## 🚀 Features

* Wordlist-based subdomain generation
* Permutation support (e.g. dev-api.domain.com)
* Multi-threaded DNS resolution
* Wildcard DNS detection and filtering
* Clean CLI interface
* Saves results to file

---

## ⚙️ Installation

```bash
git clone https://github.com/liketosweep/subdomain_enumerator.git
cd subdomain-enumerator
```

No external dependencies required.

---

## 📌 Usage

```bash
python main.py -d <domain> -w <wordlist> -o <output> -t <threads>
```

### Example:

```bash
python main.py -d google.com -w wordlist.txt -o output/results.txt -t 100
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

## 📊 Sample Output

```
[+] Generating subdomains...

[+] Generated 81 subdomains

[+] No wildcard detected

[+] Resolving...

[+] api.google.com -> 172.217.27.164
[+] mail.google.com -> 142.250.182.5
[+] www.google.com -> 142.251.156.119

[+] Resolved 7 valid subdomains
[+] Saved to output/results.txt
```

---

## 🧠 How It Works

1. Loads a wordlist
2. Generates subdomains (including permutations)
3. Detects wildcard DNS behavior
4. Resolves subdomains using multi-threading
5. Filters valid results and saves them

---

## ⚠️ Limitations

* Uses basic DNS resolution (no advanced techniques)
* Limited wordlist size affects coverage
* No passive enumeration (e.g. crt.sh)

---

## 🔮 Future Improvements

* HTTP probing (check alive services)
* Integration with passive sources
* Better permutation strategies
* Output formats (JSON, CSV)
* Rate limiting and retry tuning

---

## 📜 License

This project is open-source and available under the MIT License.
