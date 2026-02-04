---
name: fetch-favicons
description: Fetch favicons for any website using multiple fallback sources (Google, DuckDuckGo, direct). Use when needing website icons, favicons, site logos, or domain icons for any URL or domain.
---

# Fetch Favicons

Retrieve favicons for any domain using multiple sources with automatic fallback.

## Requirements

- Python 3.6+
- `requests` library: `pip install requests`

## Quick Usage

```bash
python3 scripts/fetch_favicon.py example.com
python3 scripts/fetch_favicon.py example.com --output ./icons/
python3 scripts/fetch_favicon.py example.com --size 128
```

## Sources (in order of preference)

| Source     | URL Pattern                                                    | Notes                          |
| ---------- | -------------------------------------------------------------- | ------------------------------ |
| Google     | `https://www.google.com/s2/favicons?domain={domain}&sz={size}` | Best quality, supports sizes   |
| DuckDuckGo | `https://icons.duckduckgo.com/ip3/{domain}.ico`                | Privacy-focused, no size param |
| Direct     | `https://{domain}/favicon.ico`                                 | May be low quality or missing  |

## Parameters

- **domain**: Target domain (e.g., `github.com`). Full URLs are automatically parsed to extract domain.
- **size**: Size hint for Google API (16, 32, 64, 128, 256). Default: 128. Falls back to 16x16 if unavailable.
- **output**: Output directory. Default: current directory.

## Output

- Returns PNG format (Google) or ICO format (DuckDuckGo/direct)
- Filename: `{domain}.png` or `{domain}.ico`
- Exits with code 0 on success, 1 on failure

## Examples

```bash
# Single domain
python3 scripts/fetch_favicon.py github.com

# From full URL (domain extracted automatically)
python3 scripts/fetch_favicon.py "https://docs.github.com/en/pages"

# Custom size and output
python3 scripts/fetch_favicon.py twitter.com --size 256 --output ~/icons/

# Batch fetch (one per line in file)
cat domains.txt | xargs -I {} python3 scripts/fetch_favicon.py {} --output ./favicons/
```

## Rate Limiting

Google's API may rate-limit after ~55 consecutive requests. Add delays for batch operations:

```bash
cat domains.txt | while read domain; do
  python3 scripts/fetch_favicon.py "$domain" --output ./favicons/
  sleep 0.5
done
```
