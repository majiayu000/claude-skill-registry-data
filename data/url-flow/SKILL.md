---
name: url-flow
description: Reference guide for LinkedIn URL handling in SourcingX. Consult this when debugging URL matching issues, enrichment deduplication problems, or "already enriched" count mismatches. NOT user-invocable - this is internal documentation for Claude.
---

# LinkedIn URL Flow — Complete Reference

This document explains how LinkedIn URLs flow through SourcingX from input to database storage and back to lookup. **Consult this when working on URL-related bugs.**

## Quick Reference

| Source | URL Format Example | Key Function |
|--------|-------------------|--------------|
| CSV/GEM | `john-doe-12345` | `normalize_uploaded_csv()` |
| PhantomBuster | `defaultProfileUrl` | `normalize_phantombuster_columns()` |
| Crustdata Echo | `query_linkedin_profile_urn_or_slug` | `enrich_batch()` - PRIMARY match |
| Crustdata Canonical | `linkedin_flagship_url` | `enrich_batch()` - fallback |
| Database PK | `linkedin_url` column | `save_enriched_profile()` |
| Database Matching | `original_url` column | `get_recently_enriched_urls()` |

## Crustdata Input Echo (Critical for Matching)

**Crustdata echoes our input URL back in the response!**

When we send: `linkedin_profile_url=john-doe-12345`

Crustdata returns:
```json
{
  "query_linkedin_profile_urn_or_slug": ["john-doe-12345"],  // OUR INPUT ECHOED BACK
  "linkedin_flagship_url": "https://linkedin.com/in/jdoe",   // Their canonical URL
  "name": "John Doe"
}
```

**Why this matters:**
- `query_linkedin_profile_urn_or_slug` is the PRIMARY matching method (Tier 1)
- It's an array - always use `[0]` to get the first element
- This solves 95%+ of URL mismatches since we can match our exact input
- Fallback tiers (2-5) are rarely needed now

## Multi-Source Duplicate Problem

**Scenario:** Same profile uploaded from PhantomBuster AND Jam CSV with different URLs.

| Upload | Input URL | Crustdata Returns | DB Result |
|--------|-----------|-------------------|-----------|
| 1st (PB) | `john-doe-12345` | `jdoe` | `original_url = john-doe-12345` |
| 2nd (Jam) | `johndoe` | `jdoe` | `original_url = johndoe` (OVERWRITES!) |

**Current limitation:** `original_url` is a single TEXT field, not an array.
- Only the MOST RECENT input URL is stored
- Previous input URLs are lost
- "Already enriched" check may miss profiles from earlier sources

**Workaround:** The Crustdata echo (`query_linkedin_profile_urn_or_slug`) helps during enrichment, but doesn't solve the DB storage issue.

## The Core Problem

**Crustdata often returns different URLs than input:**

| Input URL | Crustdata Returns | Why Different |
|-----------|-------------------|---------------|
| `yoav-derman-365736152` | `yderman` | Canonical short form |
| `daniel-rubin-8b694b65` | `1989danielrubin` | Birth year prefix |
| `assaf-fridman-42299324` | `assafridman` | Hyphen removed + spelling |
| `tsaela-pinto-51a12315` | `tsaela` | Last name dropped |

## URL Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. INPUT: CSV/GEM or PhantomBuster                                 │
│     URL: https://www.linkedin.com/in/john-doe-12345                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. NORMALIZATION: normalize_linkedin_url() in normalizers.py       │
│     - Add https:// if missing                                        │
│     - Ensure www.linkedin.com (not linkedin.com)                    │
│     - Remove query params (?param=value)                            │
│     - Remove trailing slashes                                        │
│     - Lowercase everything                                           │
│     OUTPUT: https://www.linkedin.com/in/john-doe-12345              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. PRE-ENRICH MAPPING: enrich_batch() lines 2469-2505              │
│                                                                      │
│  Build 4 maps from input URLs for matching results:                  │
│                                                                      │
│  original_url_map:                                                   │
│    "john-doe-12345" → input URL                                     │
│    "john-doe" → input URL (base, suffix stripped)                   │
│    "doe-john" → input URL (reversed)                                │
│                                                                      │
│  normalized_url_map:                                                 │
│    "johndoe" → input URL (hyphen-free)                              │
│                                                                      │
│  name_url_map:                                                       │
│    "john doe" → input URL (name extracted from username)            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. CRUSTDATA API: GET /screener/person/enrich                      │
│     Returns:                                                         │
│       query_linkedin_profile_urn_or_slug: ["john-doe-12345"]        │
│         ^^^ IMPORTANT: Crustdata ECHOES our input URL back! ^^^     │
│       linkedin_flagship_url = "https://linkedin.com/in/jdoe"        │
│       name = "John Doe"                                              │
│       first_name = "John", last_name = "Doe"                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. RESULT MATCHING: 5-tier cascade (lines 2531-2620)               │
│                                                                      │
│  Tier 1: query_linkedin_profile_urn_or_slug (Crustdata echoes input)│
│  Tier 2: linkedin_flagship_url username matching                    │
│          - Exact: "jdoe" in original_url_map?                       │
│          - Base: get_base_username("jdoe") in map?                  │
│          - Reversed: "doe-john" in map?                             │
│          - Hyphen-free: "jdoe" in normalized_url_map?               │
│  Tier 3: Loop through map keys, compare base versions               │
│  Tier 4: Name-based matching (Crustdata's name vs name_url_map)     │
│          - Full name: "john doe" in name_url_map?                   │
│          - First+Last: f"{first} {last}" in map?                    │
│          - Reversed: f"{last} {first}" in map?                      │
│  Tier 5: Partial name (subset matching for middle names)            │
│          - {"john", "doe"} subset of {"john", "middle", "doe"}?     │
│                                                                      │
│  SUCCESS: item['_original_url'] = matched input URL                 │
│  FAILURE: item['_original_url'] = None (safe, no guessing)          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  6. DATABASE SAVE: save_enriched_profile() in db.py lines 202-293   │
│                                                                      │
│  linkedin_url (PK): Crustdata's canonical URL (normalized)          │
│  original_url:      Input URL from matching (_original_url)         │
│  raw_data:          Full Crustdata JSON response                    │
│                                                                      │
│  UPSERT on linkedin_url (primary key)                               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  7. LATER: "Already Enriched" Check                                 │
│                                                                      │
│  get_recently_enriched_urls() in db.py lines 1348-1364              │
│  Returns BOTH columns:                                               │
│    - linkedin_url (e.g., "jdoe")                                    │
│    - original_url (e.g., "john-doe-12345")                          │
│                                                                      │
│  Dashboard matching (lines 5699-5735):                              │
│  For each input URL, generate variants and check against DB set     │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Functions Reference

### Normalization

**File: `normalizers.py`**

```python
normalize_linkedin_url(url: str) -> str | None
# Lines 170-221
# Transforms URL to canonical format
# Returns None if invalid
```

### Enrichment & Matching

**File: `dashboard.py`**

```python
enrich_batch(urls: list[str], api_key: str) -> list[dict]
# Lines 2425-2626
# Calls Crustdata API and matches results to input URLs

# Key helper functions inside enrich_batch:
extract_username(url)           # Line 2431 - Get username from URL
get_base_username(username)     # Line 2438 - Strip numeric suffix
get_reversed_name(username)     # Line 2455 - Reverse first-last order
get_normalized_name(username)   # Line 2464 - Remove hyphens
extract_name_from_username(u)   # Line 2469 - Extract probable name
```

### Database Operations

**File: `db.py`**

```python
save_enriched_profile(client, linkedin_url, crustdata_response, original_url=None)
# Lines 202-293
# Saves profile with BOTH linkedin_url and original_url

get_recently_enriched_urls(client, months=6) -> list
# Lines 1348-1364
# Returns both linkedin_url AND original_url for matching

get_profile(client, linkedin_url) -> dict | None
# Line 498
# Lookup by exact linkedin_url
```

## Common Issues & Fixes

### Issue: "X profiles to enrich" never reaches 0

**Symptoms:** After enrichment, some profiles still show as "to enrich" even though they were processed.

**Cause:** Crustdata returned a different URL than input, and matching failed. The profile was saved with `original_url = None`.

**Debug Steps:**
1. Check the debug expander in Enrich tab for unmatched URLs
2. Search DB by name: `db.search_profiles(client, "Person Name")`
3. Compare DB URL vs input URL

**Fix:**
1. Update `original_url` in DB:
   ```python
   client.upsert('profiles', {
       'linkedin_url': db_url,
       'original_url': input_url,
       'status': 'enriched'
   }, on_conflict='linkedin_url')
   ```
2. Improve matching in `enrich_batch()` if pattern is systematic

### Issue: Duplicate profiles in database

**Symptoms:** Same person appears twice with different `linkedin_url` values.

**Cause:** Input URL and Crustdata URL are both stored as separate profiles.

**Debug Steps:**
1. Search by name to find duplicates
2. Check if both have `raw_data` (one may be empty)

**Fix:** Merge profiles, keeping the one with `raw_data`. Set `original_url` on the kept profile.

### Issue: Email not persisting after SalesQL enrichment

**Symptoms:** Emails show in session but gone after refresh.

**Cause:** Profiles loaded from DB don't have email, and SalesQL email wasn't saved.

**Fix:** After SalesQL enrichment, save to DB:
```python
update_profile_email(db_client, linkedin_url, email, source='salesql')
```

### Issue: Same profile from multiple sources (PhantomBuster + Jam CSV)

**Symptoms:**
- Profile uploaded from source A, then from source B with different URL
- Source A's URL no longer detected as "already enriched"
- Potential duplicate enrichment (wasted Crustdata credits)

**Cause:** `original_url` is a single TEXT field that gets overwritten on each UPSERT.

**Current behavior:**
1. PhantomBuster URL `john-doe-12345` saved as `original_url`
2. Jam CSV URL `johndoe` overwrites `original_url`
3. PhantomBuster URL no longer in DB, won't match "already enriched" check

**Workaround:**
- Crustdata's `query_linkedin_profile_urn_or_slug` echo helps during enrichment
- But DB only stores one `original_url` - previous source URLs are lost

**Future fix:** Consider changing `original_url` to `original_urls TEXT[]` array to store all historical input URLs.

## Database Schema (Relevant Columns)

```sql
profiles (
    linkedin_url TEXT UNIQUE PRIMARY KEY,  -- Crustdata canonical URL
    original_url TEXT,                      -- Input URL for matching
    raw_data JSONB,                         -- Full Crustdata response
    email TEXT,                             -- From SalesQL or CSV
    email_source TEXT,                      -- 'salesql', 'csv', etc.
    enriched_at TIMESTAMP,
    enrichment_status TEXT                  -- 'enriched', 'not_found', etc.
)
```

## Matching Algorithm Pseudocode

```python
def match_result_to_input(result, original_url_map, normalized_url_map, name_url_map):
    # Tier 1: Check query_linkedin_profile_urn_or_slug (Crustdata ALWAYS echoes input!)
    # This is the most reliable matching method - Crustdata returns our exact input
    query_slugs = result.get('query_linkedin_profile_urn_or_slug', [])
    if query_slugs and query_slugs[0]:
        input_slug = query_slugs[0].lower()
        if input_slug in original_url_map:
            return original_url_map[input_slug]

    # Tier 2: Match via result's canonical URL
    result_username = extract_username(result.linkedin_flagship_url)

    if result_username in original_url_map:
        return original_url_map[result_username]

    base = get_base_username(result_username)
    if base in original_url_map:
        return original_url_map[base]

    normalized = result_username.replace('-', '')
    if normalized in normalized_url_map:
        return normalized_url_map[normalized]

    # Tier 3: Check if result matches any map key's base version
    for map_key, map_url in original_url_map.items():
        if get_base_username(map_key) == result_username:
            return map_url

    # Tier 4: Name-based matching
    cd_name = result.name.lower()
    if cd_name in name_url_map:
        return name_url_map[cd_name]

    first_last = f"{result.first_name} {result.last_name}".lower()
    if first_last in name_url_map:
        return name_url_map[first_last]

    # Tier 5: Partial name (subset matching)
    cd_parts = set(cd_name.split())
    for map_name, map_url in name_url_map.items():
        if set(map_name.split()).issubset(cd_parts):
            return map_url

    # No match - return None (safe!)
    return None
```

## Testing URL Matching

```python
# Quick test script
import db

client = db.get_supabase_client()

# Check if profile exists by canonical URL
profile = db.get_profile(client, 'https://www.linkedin.com/in/jdoe')

# Search by name if URL unknown
results = db.search_profiles(client, 'John Doe')

# Check original_url field
if profile:
    print(f"linkedin_url: {profile.get('linkedin_url')}")
    print(f"original_url: {profile.get('original_url')}")

# Get all recently enriched URLs (both columns)
urls = db.get_recently_enriched_urls(client, months=6)
print(f"Total URLs in lookup set: {len(urls)}")
```

## Related Files

- `normalizers.py` - URL normalization functions
- `dashboard.py` lines 2425-2626 - Enrichment and matching
- `dashboard.py` lines 5632-5750 - "Already enriched" check
- `db.py` lines 202-293 - save_enriched_profile
- `db.py` lines 1348-1364 - get_recently_enriched_urls
- `migrations/008_*.sql` - Added original_url column
- `migrations/015_*.sql` - Exact URL matching RPC
