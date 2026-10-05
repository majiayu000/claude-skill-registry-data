---
name: domain-check
description: Batch domain availability checker via whois.com with Playwright browser automation. Handles anti-bot/CAPTCHA challenges by bringing browser to foreground for manual verification. Supports any TLD. Use when (1) checking if domains are available for registration, (2) batch-checking multiple domain candidates, (3) verifying domain availability before purchase, or (4) exporting domain check results to JSON.
---

# Domain Availability Check

Batch-check domain availability via whois.com with anti-bot/CAPTCHA assist.

## Quick Start

```powershell
# Setup (first time)
cd $SKILL_DIR && npm run setup

# Check domains from command line
node run.js scripts/domain-check.js --domains "example.ai,myapp.io" --nslookup

# Check domains from file
node run.js scripts/domain-check.js --file domains.txt --out results.json --nslookup
```

File format: one domain per line, `#` for comments. See `examples/domains.txt`.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--domains` | Comma-separated domain list | - |
| `--file` | Path to domain list file | - |
| `--out` | Output JSON file path | stdout |
| `--nslookup` | Corroborate with DNS lookup | `false` |
| `--user-data-dir` | Persistent browser profile (reduces CAPTCHA) | - |
| `--challenge-wait` | Max CAPTCHA wait time (ms) | `120000` |
| `--delay` | Delay between checks (ms) | `900` |

## Behavior

- Opens visible browser (`headless=false`) for CAPTCHA handling.
- On Security Check / CAPTCHA: brings browser to front, waits for manual completion.
- Classification rules:
  - `Looks like this domain has not been registered yet` -> **available**
  - `Domain Information` / `Registrar Information` -> **registered**
  - WHOIS patterns like `No match for`, `Domain not found` -> **available**
- `--nslookup`: NXDOMAIN suggests unregistered DNS (corroboration only).

## Output

JSON array with `domain`, `status` (`available`|`registered`|`unknown`|`error`), `nslookup`.

## Tips

- Use `--user-data-dir ./profile` to reduce repeated CAPTCHA challenges.
- Run sequentially to minimize anti-bot triggers.
