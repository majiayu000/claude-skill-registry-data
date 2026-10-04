---
name: fuzz
description: |
  Lightweight web fuzzing via ffuf — directory discovery, parameter testing, subdomain enumeration.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Fuzz — Web Fuzzing with ffuf

Lightweight web application fuzzing using [ffuf](https://github.com/ffuf/ffuf).

## Prerequisites

```bash
command -v ffuf && ffuf -V
```

If not installed:
```bash
brew install ffuf    # macOS
# or
go install github.com/ffuf/ffuf/v2@latest
```

## Common Wordlists

```
/usr/share/wordlists/                          # Kali default
/opt/homebrew/share/wordlists/                 # Homebrew
~/.local/share/wordlists/                      # User-local

# SecLists (install: brew install seclists)
/opt/homebrew/share/seclists/Discovery/Web-Content/common.txt
/opt/homebrew/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
/opt/homebrew/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
/opt/homebrew/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt
```

If no wordlists found: `brew install seclists`

## Usage Patterns

### Directory / File Discovery
```bash
ffuf -u https://TARGET/FUZZ -w wordlist.txt -mc 200,301,302,403
```

### API Endpoint Discovery
```bash
ffuf -u https://TARGET/api/FUZZ -w wordlist.txt -mc 200,401,403,405
```

### Parameter Fuzzing (GET)
```bash
ffuf -u "https://TARGET/page?FUZZ=value" -w params.txt -mc 200 -fs 4242
```

### POST Data Fuzzing
```bash
ffuf -u https://TARGET/login -X POST \
  -d "username=admin&password=FUZZ" \
  -w passwords.txt -mc 200 -fc 401
```

### Subdomain Enumeration
```bash
ffuf -u https://FUZZ.TARGET.com -w subdomains.txt -mc 200,301,302
```

### Authenticated Fuzzing
```bash
ffuf -u https://TARGET/api/FUZZ -w wordlist.txt \
  -H "Authorization: Bearer <token>" \
  -H "Cookie: session=<value>" \
  -mc 200,201,403
```

## Filtering Options

- `-mc 200,301` — match HTTP status codes
- `-fc 404,500` — filter (exclude) status codes
- `-fs 4242` — filter by response size (removes noise)
- `-fw 12` — filter by word count
- `-fr "not found"` — filter by regex in response

## Output
```bash
ffuf -u https://TARGET/FUZZ -w wordlist.txt -o results.json -of json
```

## Tips

- Start with small wordlists, expand if needed
- Use `-rate 100` to limit requests per second (avoid DoS)
- Use `-t 40` to control thread count (default: 40)
- Run once without filters, note the common response size, then add `-fs`
- Combine with `-recursion -recursion-depth 2` for recursive discovery
