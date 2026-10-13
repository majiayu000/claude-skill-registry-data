---
name: scrape-linkedin
description: "Fetches a LinkedIn profile via ScrapingDog API and displays a formatted summary (name, role, location, followers, about, experience, education). Use when asked to look up, scrape, or fetch a LinkedIn profile for a speaker, contact, or person. Accepts a LinkedIn profile URL or ID."
allowed-tools:
  - Bash(curl:*)
  - Bash(*/get-secret.sh:*)
  - Read
---

# Scrape LinkedIn Profile

## Purpose

Fetch a LinkedIn profile using ScrapingDog and display a clean summary. Always uses `premium=true` — this is required for reliability on many profiles.

## Step 1: Extract Profile ID

Accept either a full LinkedIn URL or a bare profile ID.

- URL: `https://linkedin.com/in/braddipaolo` → ID: `braddipaolo`
- URL: `https://ca.linkedin.com/in/nitasha-nijhawan` → ID: `nitasha-nijhawan`
- Bare ID: `juliazarb` → use as-is

Strip everything after `?` or trailing `/` from the extracted ID.

## Step 2: Fetch the Profile

```bash
# Get API key from Vault: query get_user_secret('scrapingdog_api_key') via Supabase RPC
# Or from config table: SELECT config_value FROM config WHERE config_key = 'scrapingdog_api_key'
API_KEY="<from_vault_or_config>"
curl -s "https://api.scrapingdog.com/linkedin?api_key=${API_KEY}&type=profile&linkId={PROFILE_ID}&premium=true" \
  | python3 -c "
import sys, json, re
raw = sys.stdin.buffer.read()
cleaned = re.sub(rb'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', b'', raw)
d = json.loads(cleaned)
if isinstance(d, list): d = d[0]
print(json.dumps(d, indent=2))
"
```

**If the response contains `"message"` key** (e.g. `{"message": "Something went wrong..."}`), the fetch failed. Report the error clearly and stop — do not proceed to display or cache steps.

## Step 3: Display

Present the profile in this format:

```
**[fullName]** — [headline]
[location] · [followers]

**About:** [about, first 3–4 sentences]

**Experience:**
- [experience[0].title] @ [experience[0].company_name]
- [experience[1].title] @ [experience[1].company_name]
- [experience[2].title] @ [experience[2].company_name]

**Education:**
- [education[0].degree] [education[0].field_of_study] @ [education[0].school]

**Posts/Articles:** [articles[0].title], [articles[1].title]
```

Omit any field that is missing or empty. Limit experience to 3 entries, education to 2, articles to 3.

## Step 4: Cache Update (Optional)

If working in a project that uses LinkedIn profile caching, update the cache at `/tmp/linkedin_cache.json`:

```bash
python3 - << 'PYEOF'
import json, os
CACHE = "/tmp/linkedin_cache.json"
PROFILE_ID = "{PROFILE_ID}"
RESULT = {PARSED_JSON}  # the full parsed dict from Step 2

cache = {}
if os.path.exists(CACHE):
    with open(CACHE) as f:
        cache = json.load(f)
cache[PROFILE_ID] = RESULT
with open(CACHE, "w") as f:
    json.dump(cache, f, indent=2)
print(f"Cache updated: {PROFILE_ID}")
PYEOF
```

## Constants

- **API key**: Stored in Vault (`scrapingdog_api_key`) or config table. Retrieve via Supabase RPC `get_user_secret('scrapingdog_api_key')`.
- **`premium=true`**: Required for profiles that block the standard endpoint (hyphens in IDs, newer profiles, private-ish accounts). Always include it.
- **Control char strip**: LinkedIn bios sometimes contain raw control characters (`\x00`–`\x1f`) that break JSON parsing. The `re.sub` in Step 2 handles this.
