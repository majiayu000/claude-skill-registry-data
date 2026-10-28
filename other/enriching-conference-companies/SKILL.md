---
name: enriching-conference-companies
description: Turn a list of conference companies, sponsors or exhibitors into named decision-makers with LinkedIn profile URLs and verified email addresses. Use after scraping a conference roster, or whenever you have company names and need the actual person to contact inside each one.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Enriching Conference Companies

## Goal
Turn "186 sponsor logos" into "the person at each company whose job is the thing I sell, their LinkedIn, and an address that won't bounce."

## When to use
- Straight after `scraping-conference-rosters`
- Any time you have company names but no contacts
- "Who do I talk to at these companies?"

## The four layers

Cheapest first. Each one is independently skippable.

| # | Layer | Tool | Cost |
|---|---|---|---|
| 1 | Company website | Tavily | free |
| 2 | Decision-makers by role | Tavily | free |
| 3 | LinkedIn profile URL | Exa | free |
| 4 | Email + SMTP verification | Apify | **paid, off by default** |

Layers 1–3 are free tiers with no card. Layer 4 is the only one that can surprise you with a bill, which is why it needs `--emails` explicitly.

**Tavily** answers "who runs marketing at this company" the way a search engine would. **Exa** is embedding-based and much better at "which LinkedIn profile is *this exact person*" — the step where a keyword engine hands you the wrong Sarah Chen with total confidence.

## Process

### Step 1 — always start with a limit
```bash
python -X utf8 -m scripts.enrich_conference_companies \
    --input data/example-sponsors.csv \
    --output data/example-enriched.csv \
    --roles "VP of Marketing" "Chief Marketing Officer" \
    --limit 10
```

Read those 10 rows before going further. If the names look wrong, the roles are wrong.

### Step 2 — set the roles to match what YOU sell
This is the flag that decides whether the output is useful:

| You sell | `--roles` |
|---|---|
| Video, brand, web design | `"VP of Marketing" "Head of Brand" "Chief Marketing Officer"` |
| Compliance, legal tech | `"General Counsel" "Chief Compliance Officer"` |
| Recruiting | `"Head of Talent" "VP People" "Chief People Officer"` |
| Clinical software | `"Chief Medical Officer" "VP Clinical Operations"` |
| Sponsorship, events | `"Head of Events" "VP Partnerships"` |

Default is marketing leadership. Change it.

### Step 3 — the full run
```bash
python -X utf8 -m scripts.enrich_conference_companies \
    --input data/example-sponsors.csv \
    --output data/example-enriched.csv \
    --roles "VP of Marketing" "Head of Brand" --workers 4
```

### Step 4 — emails, when you're ready to spend
```bash
python -X utf8 -m scripts.enrich_conference_companies \
    --input data/example-sponsors.csv --output data/example-enriched.csv \
    --roles "VP of Marketing" --emails --verify-emails --limit 25
```
Prints a cost estimate before it starts. **Always verify before a first send** — bounces damage domain reputation and it is slow to rebuild.

## Reading the output — this matters

The `confidence` column is doing real work here. Do not ignore it.

| `confidence` | What it means | Do this |
|---|---|---|
| `confirmed` | LinkedIn URL verified — the surname matches the profile slug | Reach out |
| `probable` | Name found, LinkedIn unverified | Check the profile before sending |
| `weak` | Name found, no LinkedIn match | Verify manually first |
| — with `next_action: research-manually` | No confident contact at all | The booth is still worth visiting |

**Check `evidence` for the title.** It says either `title from source` (the source stated their real title) or `title unconfirmed; matched on search for '...'` (the title column is the role we searched for, not a confirmed fact). Never quote an unconfirmed title back to someone.

## Three things it deliberately will not do

**It will not attach a LinkedIn URL it can't verify.** If the surname isn't in the profile slug, the cell stays empty. A wrong LinkedIn becomes a message to a stranger — worse than an empty cell, because a full-looking row never gets checked.

**It will not invent a name.** Names come from search-result titles and pass a strict shape test with a stopword blocklist. Mining prose produced contacts called "combine design". Conservative on purpose: a missed contact costs one row, a fabricated one costs credibility at a company you're courting.

**It will not silently drop companies.** No confident contact means the row stays, flagged. Dropping it would overstate your coverage.

## Edge cases

- **"No TAVILY_API_KEY set"** — free at tavily.com, 1,000/month, no card.
- **Everything comes back `weak`** — usually no `EXA_API_KEY`. Exa is what confirms LinkedIn matches. Free at exa.ai.
- **Names look wrong for a company** — its name is probably a common word and search is matching the wrong thing. Enrich it by hand.
- **All keys rate-limited (Tavily 432)** — often temporary rather than a hard cap. Wait, then retry; keys rotate automatically.
- **Big lists** — start with `--limit 25`. 186 companies × 3 roles is 558 searches.

## Cost
Layers 1–3: free. Layer 4: roughly $0.02 per contact looked up, plus verification.
