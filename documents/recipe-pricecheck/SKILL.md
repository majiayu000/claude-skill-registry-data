---
name: recipe-pricecheck
description: "Research active and sold Reverb listings to establish a used-market price range for purchasing intake."
metadata:
  version: 0.1.1
  openclaw:
    category: "recipe"
    domain: "purchasing"
    requires:
      bins:
        - revcli
      skills:
        - reverb-listings
---

# Price Check: Market Research for Purchasing Intake

> **PREREQUISITE:** Load the following skills to execute this recipe: `reverb-listings`

Research active listings and recent sold prices on Reverb.com to establish a used-market price range for gear submitted for possible purchase.

## Required Output Format

**You MUST produce two markdown tables** — one for sold listings, one for active listings. Do not produce prose summaries instead of tables.

### Sold Listings

| Title   | Condition   | Caveats             | Asking                   | Sold            | Listed            | Source                     |
| ------- | ----------- | ------------------- | ------------------------ | --------------- | ----------------- | -------------------------- |
| [title] | [condition] | [repairs/mods or —] | [original_price.display] | [price.display] | [created_at date] | [link](URL?show_sold=true) |

### Active Listings

| Title   | Condition   | Caveats             | Asking          | Listed            | Source      |
| ------- | ----------- | ------------------- | --------------- | ----------------- | ----------- |
| [title] | [condition] | [repairs/mods or —] | [price.display] | [created_at date] | [link](URL) |

**Source column rules:**

- Every row MUST have a hyperlinked source using `_links.web.href`
- Sold listing URLs: append `?show_sold=true`
- Format: `[View](https://reverb.com/...)`

After the tables, add a **Price Range Summary** (2–4 sentences max): sold baseline range by condition, active ask range, notable discount depth if present.

---

## Steps

1. Fetch active and sold listings in parallel (write to files to avoid output truncation):

   ```
   revcli listings list --query "MAKE MODEL" --page-all --per-page 50 --page-limit 4 --format json --output /tmp/active.json
   revcli listings list --query "MAKE MODEL" --params '{"show_only_sold":true}' --page-all --per-page 50 --page-limit 4 --format json --output /tmp/sold.json
   ```

2. Parse both files with Python. **`--page-all` emits one JSON object per page, not a single array** — use `raw_decode`:

   ```python
   import json
   from json import JSONDecoder

   def load_pages(path):
       with open(path) as f:
           text = f.read().strip()
       decoder, pos, listings = JSONDecoder(), 0, []
       while pos < len(text):
           while pos < len(text) and text[pos] in ' \n\r\t':
               pos += 1
           if pos >= len(text):
               break
           obj, pos = decoder.raw_decode(text, pos)
           listings.extend(obj.get('listings', []))
       return listings

   active = load_pages('/tmp/active.json')
   sold   = load_pages('/tmp/sold.json')
   ```

3. Extract per listing, using python:
   - `title`
   - `condition.display_name` — e.g. `"Excellent"`, `"Brand New"`
   - `price.display` — asking or final sold price
   - `original_price.display` — pre-discount price (sold listings only; gap = negotiability signal)
   - `created_at` — date listed **(sort by this, descending)**
   - `description` — HTML; strip tags; scan for caveats (replaced parts, repairs, mods, damage); do NOT flag negated phrases (`"no cracks"`, `"not modified"`)
   - `_links.web.href` — listing URL **(required for Source column)**

4. Apply filters before building tables:
   - **Exclude** `condition.display_name == "Brand New"` from used-market baseline
   - **Flag but include** listings with repairs/mods/replaced parts — put the caveat in the Caveats column
   - **Flag but include** "unplayed"/"new-old-stock" listings — treat as Excellent condition, note in Caveats

5. Populate the tables defined in **Required Output Format** above, then write the summary.
