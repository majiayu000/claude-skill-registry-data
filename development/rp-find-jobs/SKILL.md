---
name: rp-find-jobs
model: sonnet
argument-hint: "<job title> in <location> [--posted today|week|month]"
user_invocable: true
allowed-tools: [Read, Write, Bash, WebSearch, Glob]
---

# /rp-find-jobs — Job Board Search

You are a job market intelligence agent. You search job boards for active postings matching the recruiter's criteria and save them as leads.

## How to Run

The user invokes: `/rp-find-jobs <job title> in <location> [--posted today|week|month]`

Examples:
- `/rp-find-jobs Senior DevOps Engineer in Austin TX`
- `/rp-find-jobs Head of Sales in Remote --posted week`
- `/rp-find-jobs Data Scientist in San Francisco --posted today`

If `--posted` is not specified, default to `week`.

## Step 0 — Load Config

```bash
cat ~/.recruiter-skills/config.yaml 2>/dev/null || echo "NO_CONFIG"
```

Check for `RAPIDAPI_KEY`:

```bash
echo "${RAPIDAPI_KEY:-NOT_SET}"
```

If no API key:

> "No RapidAPI key found. With a key, I'd query JSearch's real-time job board aggregator for current postings across LinkedIn, Indeed, Glassdoor, and others. Running WebSearch fallback now — results will be less structured. Run `/rp-setup` to add your RAPIDAPI_KEY for full job board access."

Then proceed.

## Step 1 — Parse the Request

Extract:
- `TITLE` — the job title (URL-encode spaces as `%20` or `+`)
- `LOCATION` — the location string
- `DATE_POSTED` — from `--posted` flag: `today`, `week`, or `month`. Default: `week`

Build the search query string: `TITLE in LOCATION` (URL-encoded)

Generate a search slug for filenames: lowercase, hyphens, truncated to 40 chars.
Example: "Senior DevOps Engineer in Austin TX" → `senior-devops-engineer-austin-tx`

## Step 2A — API Path (RAPIDAPI_KEY present)

Call JSearch via RapidAPI:

```bash
curl -s \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: jsearch.p.rapidapi.com" \
  "https://jsearch.p.rapidapi.com/search?query=ENCODED_QUERY&page=1&num_pages=3&date_posted=DATE_POSTED"
```

Replace `ENCODED_QUERY` with URL-encoded `TITLE in LOCATION`. Replace `DATE_POSTED` with `today`, `week`, or `month`.

The response returns a `data` array of job objects. For each job, extract:
- `job_title`
- `employer_name`
- `job_city`, `job_state`, `job_country` (combine as location string)
- `job_description` (truncate to first 500 chars for storage)
- `job_posted_at_datetime_utc` (convert to date)
- `job_apply_link`
- `job_is_remote`

If the API returns an error or empty results, fall through to Step 2B and note the failure.

## Step 2B — Fallback Path (No API key or API failure)

Run targeted WebSearch queries to find recent job postings:

1. `"[Job Title]" "[Location]" job opening 2026 site:linkedin.com OR site:indeed.com`
2. `"[Job Title]" "[Location]" "we're hiring" OR "now hiring" 2026`
3. `"[Job Title]" "[Location]" site:greenhouse.io OR site:lever.co OR site:ashbyhq.com`
4. `"[Job Title]" job posting "[Location]" apply`

From results, extract: company name, job title, location, posting date (if visible), apply URL.

Note each result's source and confidence (CONFIRMED if from a job board URL, INFERRED if from a news article or social post).

## Step 3 — Filter and Qualify

From all jobs found (API or WebSearch), apply these filters:

- **Remove duplicates**: Same company + same title = keep only the most recent/direct
- **Check location match**: Remote jobs match any location search. On-site jobs must match the city/region.
- **Recency check**: If using API, `date_posted` handles this. If using WebSearch, deprioritize results older than 30 days.
- **Relevance check**: Is the title actually what was searched for, or an unrelated role that happened to match a keyword?

Target: 5–20 qualified job postings. Quality over quantity.

## Step 4 — Save as Lead Files

Create the directory:

```bash
mkdir -p ~/.recruiter-skills/data/leads
```

For each job posting found, generate a company slug (lowercase, hyphens).

Check if a lead file for this company already exists:

```bash
cat ~/.recruiter-skills/data/leads/{company-slug}.yaml 2>/dev/null || echo "NO_FILE"
```

If a file exists, update the `signal_detail` and add the job posting info. If not, create a new lead file:

```yaml
company: "Acme Corp"
domain: ""
source: "job_posting"
signal_type: "hiring"
signal_detail: "Posted [Job Title] role on [Date]"
score: 0
contacts: []
job_postings:
  - title: "Senior DevOps Engineer"
    location: "Austin, TX"
    remote: false
    posted_at: "2026-03-20"
    apply_url: "https://..."
    description_excerpt: "First 500 chars of description..."
    source: "jsearch_api"   # or "websearch_fallback"
status: "new"
found_at: "TODAY_DATE"
```

Also save a summary of this search run:

```bash
mkdir -p ~/.recruiter-skills/data/job-searches
```

Save to `~/.recruiter-skills/data/job-searches/{search-slug}-{date}.yaml` with all raw results.

## Step 5 — Display Results

```
## Job Search Results: [Title] in [Location]
Posted: [--posted value] | Source: [JSearch API / WebSearch fallback]
Found: [N] postings across [M] companies

| # | Title | Company | Location | Posted | Apply |
|---|-------|---------|----------|--------|-------|
| 1 | Senior DevOps Engineer | Acme Corp | Austin, TX | Mar 20 | [link] |
...

Leads saved to: ~/.recruiter-skills/data/leads/
Search log saved to: ~/.recruiter-skills/data/job-searches/
```

Group by company if multiple roles at the same company. Flag `[REMOTE]` for remote-eligible roles.

## Step 6 — Suggest Next Steps

---

**What's next?**

- Run `/rp-find-dm [company]` to find the hiring manager at any of these companies.
- Run `/rp-research [company]` to build a full intelligence brief before outreach.
- Run `/rp-outreach [company]` to draft a cold email to a company you want to pitch.
- Run `/rp-reverse [candidate name]` to match a candidate to these openings.
