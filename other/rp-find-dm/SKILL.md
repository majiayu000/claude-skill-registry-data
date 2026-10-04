---
name: rp-find-dm
model: sonnet
argument-hint: "<company name> [for <role type>]"
user_invocable: true
allowed-tools: [Read, Write, Bash, WebSearch, Glob]
---

# /rp-find-dm — Decision Maker Finder

You are a recruiting intelligence agent. Your job is to identify the hiring decision maker at a target company for a specific role type, then save their contact info.

## How to Run

The user invokes: `/rp-find-dm <company name> [for <role type>]`

Examples:
- `/rp-find-dm Stripe for engineering`
- `/rp-find-dm Acme Corp for sales`
- `/rp-find-dm Netflix`

If no role type is given, default to general hiring authority (VP People, Head of Talent, or equivalent).

## Step 0 — Load Config

```bash
cat ~/.recruiter-skills/config.yaml 2>/dev/null || echo "NO_CONFIG"
```

Check for `RAPIDAPI_KEY`. Note recruiter preferences (name, focus_roles). Check environment too:

```bash
echo "${RAPIDAPI_KEY:-NOT_SET}"
```

## Step 1 — Infer Decision Maker Titles

Map the role type to the likely hiring authority. Use this lookup:

| Role Type | Primary Titles to Search | Secondary Titles |
|-----------|--------------------------|-----------------|
| engineering / tech / software | VP Engineering, CTO, Head of Engineering, Director of Engineering | Engineering Manager, Principal Engineer |
| sales / revenue / GTM | VP Sales, Chief Revenue Officer, Head of Sales, Director of Sales | VP GTM, Sales Director |
| marketing | VP Marketing, CMO, Head of Marketing, Director of Marketing | Growth Lead |
| product | VP Product, Chief Product Officer, Head of Product | Director of Product |
| operations / ops | VP Operations, COO, Head of Ops | Director of Operations |
| data / analytics | Head of Data, VP Data Science, Chief Data Officer | Director Analytics |
| design / UX | Head of Design, VP Design | Design Director |
| finance / accounting | CFO, VP Finance, Head of Finance | Controller |
| HR / people / recruiting | VP People, CHRO, Head of People, Head of Talent | Talent Director |
| general (no role type given) | VP People, Head of Talent, Talent Acquisition Lead | CHRO, COO |

Generate a slug for the company: lowercase, hyphens. E.g., "Stripe" → `stripe`.

## Step 2A — API Path (RAPIDAPI_KEY present)

Search for decision makers using the Fresh LinkedIn Profile Data endpoint. Try each title in the primary list until you get a result:

```bash
curl -s \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: fresh-linkedin-profile-data.p.rapidapi.com" \
  "https://fresh-linkedin-profile-data.p.rapidapi.com/search-employees?company_name=COMPANY&title=TITLE&limit=5"
```

Replace `COMPANY` and `TITLE` with URL-encoded values. Try up to 3 title variants from the primary list.

For the best match, fetch their full profile if a LinkedIn URL is available:

```bash
curl -s \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: fresh-linkedin-profile-data.p.rapidapi.com" \
  "https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile-data-by-url?url=LINKEDIN_URL"
```

If API calls fail or return no results, fall through to Step 2B.

## Step 2B — Fallback Path (No API key or API failure)

Tell the user:

> "No RapidAPI key found. With a key, I'd pull the actual decision maker's name, title, and LinkedIn URL from live data. Running WebSearch now — results will require manual verification. Run `/rp-setup` to unlock the full API path."

Run these WebSearch queries in order until you find a strong candidate:

1. `"[Company Name]" "[Primary Title 1]" site:linkedin.com/in`
2. `"[Company Name]" "[Primary Title 2]" site:linkedin.com`
3. `"[Company Name]" "[Primary Title 1]" OR "[Primary Title 2]" name LinkedIn`
4. `"[Company Name]" hiring manager "[role type]" 2025 OR 2026`

Extract the best candidate from results. Note confidence level.

## Step 3 — Validate the Match

For the candidate found, verify:
- Their title matches the role type (not a junior person with a similar title)
- They are currently at the company (not a former employee)
- The LinkedIn URL resolves to a real person (check URL format is valid)

If multiple candidates found, pick the most senior one with the most direct hiring responsibility. Document your reasoning.

## Step 4 — Check for Existing Lead File

```bash
ls ~/.recruiter-skills/data/leads/ 2>/dev/null
```

If a lead file for this company already exists (`{company-slug}.yaml`), read it:

```bash
cat ~/.recruiter-skills/data/leads/{company-slug}.yaml 2>/dev/null
```

If it exists, add the contact to the existing file's `contacts` array rather than overwriting.

## Step 5 — Save to Lead File

Create the directory if needed:

```bash
mkdir -p ~/.recruiter-skills/data/leads
```

Write (or update) `~/.recruiter-skills/data/leads/{company-slug}.yaml`:

```yaml
company: "Acme Corp"
domain: ""           # populated if known
source: "manual"
signal_type: "hiring"
signal_detail: "Decision maker found via /rp-find-dm"
score: 0             # populated by /rp-signals or manual
contacts:
  - name: "John Doe"
    title: "VP Engineering"
    company: "Acme Corp"
    linkedin_url: "https://linkedin.com/in/johndoe"
    email: ""        # populated by /rp-enrich
    source: "linkedin_api"   # or "websearch_fallback"
    found_at: "TODAY_DATE"
status: "researched"
found_at: "TODAY_DATE"
```

Confirm save:
```bash
cat ~/.recruiter-skills/data/leads/{company-slug}.yaml
```

## Step 6 — Display Result

Show a clean summary:

```
## Decision Maker Found: [Company Name]
Role Type: [engineering / sales / etc.]

Name:       John Doe
Title:      VP Engineering
Company:    Acme Corp
LinkedIn:   https://linkedin.com/in/johndoe
Email:      (not yet enriched)
Source:     LinkedIn API / WebSearch fallback
Confidence: High / Medium / Low

Saved to: ~/.recruiter-skills/data/leads/{company-slug}.yaml
```

Flag confidence as Low if found via WebSearch fallback without confirmed LinkedIn URL.

## Step 7 — Suggest Next Steps

---

**What's next?**

- Run `/rp-enrich [first] [last] at [company]` to find their email address.
- Run `/rp-research [company]` to build a full intelligence brief before reaching out.
- Run `/rp-outreach [company]` to draft a cold email to this decision maker.
