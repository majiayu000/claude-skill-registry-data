---
name: job-scraper
description: "Searches configured job portals via web search, deduplicates against seen jobs and the tracker, quick-rates fit, and presents new matches for evaluation. Country-agnostic — all portal/geography targeting comes from the user's config. Activates on: search for jobs, find new postings, scrape job boards, /search, /scrape."
allowed-tools:
  - Read
  - Write
  - WebSearch
  - WebFetch
---

## Purpose

This file is the Plane 1 knowledge anchor for the job search workflow (ARCH-0008, ARCH-0010). As a Plane 1 skill it lives under `.claude/skills/job-scraper/` and provides the AI assistant with structured knowledge — it does not execute binaries or scrape via compiled code. The skill queries whatever job portals the user has configured, deduplicates results, performs a lightweight fit assessment, and presents new matches sorted by relevance. It covers REQ-1001 through REQ-1012.

The search core is **country-agnostic** (DEC-012, ADR-0004, NFR-0007): web search is the universal mechanism. No portal, country, locale, or `site:` string is hardcoded here — every target comes from the companion `search-queries.md` config. Pasted postings are a first-class input, never a fallback (DEC-011). The skill never fabricates postings (REQ-1012, ARCH-0007).

## Trigger Phrases

- "Search for jobs" / "Find new jobs" / "Any new postings?"
- "Scrape job boards" / "Run a job search"
- `/search` (optionally with a focus area, e.g. `/search data science`)
- `/scrape`
- "Search broadly" / "Run all my queries"
- Any phrase about discovering new job postings

## Companion Files

| File | When to Read |
|------|--------------|
| `search-queries.md` (this skill's folder) | Always — the query strategy, portals, geography, and location-filter tiers come from here (data-req §17) |
| `job_scraper/seen_jobs.json` | Always — the deduplication registry (data-req §10); create `{"seen": {}}` if missing |
| `job_search_tracker.csv` (repo root) | Always — extract already-applied company+role pairs for dedup (REQ-1002) |
| `01-candidate-profile.md` (job-application-assistant skill) | When forming the quick-fit signal — to know the user's core skills |

This skill never modifies `search-queries.md`; it only reads it.

---

## Contract — Steps by Requirement

### Invocation (REQ-1001)

- **Default** (`/search`, no argument): run the **top 3 priority categories** (Priority 1–3) from `search-queries.md`.
- **Focus argument** (e.g. `/search data science`): prioritize the query categories that match the focus term, then fill with the highest-priority remaining categories.
- **"broad"** (`/search broad`): run **all** query categories (Priority 1–4).
- Always load state (below) before issuing any search.
- No country-specific or portal-specific identifier is hardcoded in this skill; the breadth selection operates over whatever categories the user's config defines.

### State Loading (REQ-1002)

Before searching, load all three sources:

1. `job_scraper/seen_jobs.json` — the seen registry. If the file is missing, create it with exactly `{"seen": {}}` (data-req §10).
2. `job_search_tracker.csv` (repo root) — extract the set of already-applied **company + role** pairs.
3. `search-queries.md` — the query strategy: Search Sites, Date Filter Rule, Priority 1–4 query groups, and Location Filter Tiers.

If `search-queries.md` still contains `[UPPER_SNAKE_CASE]` placeholder tokens, the profile has not been set up — tell the user to run `/setup --section search` rather than searching against template text.

### Multi-Portal Web Search (REQ-1003)

- Build `WebSearch` queries by combining the user's configured **portals** (Search Sites) × **query strings** (selected priority groups) × **geography** (from the queries / location tiers).
- Constrain to postings from the **last 14 days** (per the Date Filter Rule).
- Issue multiple searches in **parallel** where useful for efficiency.
- All `site:` targeting, portal names, and country/region terms come **verbatim from the user's config** — never write a literal portal name or `site:` string into this skill. If the user configured `site:<portal>` entries, use them as-is; if they listed bare portal names, fold them into the query text.

### Deterministic Listing Tier (REQ-1013, NFR-0021)

If a configured portal has an adapter (ADR-0004) exposing a deterministic `list()` pass,
**prefer it**: it returns structured postings (title, company, location, URL, date)
**without spending tokens**, pre-filtering candidates before any LLM work. Feed its
results into the same dedup + quick-fit steps below. Adapters are optional — when none
exists, web search (above) is the universal fallback (ARCH-0005). Prefer the cheap
deterministic pass over LLM calls for the listing stage wherever available (cost-aware
search, NFR-0021).

### Fetch & Parse (REQ-1004)

- **Pre-filter before fetching** (token efficiency): inspect search-result titles and snippets, discard obvious non-matches, and only `WebFetch` the promising ones.
- For each fetched posting, extract: **{ title, company, location, posting date (or "recent"), url, key requirements (brief), application deadline (if listed) }**.
- **On a fetch failure** (gated portal, auth wall, dead link): do not error and do not abort. Prompt exactly:
  > "I couldn't fetch that posting. Paste it here and I'll use that."
  
  Pasted postings are processed **identically** to fetched ones (DEC-011) — paste is first-class input.

### Quick Fit Assessment (REQ-1005)

Assign each new job a lightweight **three-level** signal used only for sorting:

- **High** — role directly involves the user's core skills.
- **Medium** — role is adjacent to the user's experience.
- **Low** — role requires significant skills the user lacks.

This is explicitly **NOT** the full 5-dimension evaluation and **NOT** a numeric score — it is a sorting signal only. The full evaluation happens later in `/apply`.

### Quick Legitimacy Flag (REQ-8003)

Alongside the fit signal, run a **cheap** legitimacy scan of each posting's title and
snippet against the high-severity signals in `trust-safety/scam-patterns.json` (upfront
fees, personal-data/ID/banking harvesting, off-platform redirects, money-movement, offer
without process). If a strong signal appears, mark the job **⚠ Suspicious** in the
results so the user sees it **before** investing in `/apply`. This is a heuristic flag
only — the full legitimacy gate runs in `/apply` (REQ-8001). Never auto-skip a flagged
job (ARCH-0006); never invent a flag without the matching text (ARCH-0007).

### Deduplication & State Update (REQ-1006, data-req §10, business-rules §6)

- **Skip** a job if its URL is already a key in `seen_jobs.json`, **or** if its company+role pair already appears in `job_search_tracker.csv`.
- **Record every fetched job — new AND skipped** — in `seen_jobs.json` under the key `<url_or_company_title_key>` (the posting URL, or a company+title combination when no stable URL exists). Each entry has exactly these fields:

  ```json
  { "seen": { "<url_or_company_title_key>": { "title": "...", "company": "...", "url": "...", "first_seen": "YYYY-MM-DD", "fit": "high|medium|low", "status": "new|skipped|evaluated" } } }
  ```

  - `status` is `new` for a freshly surfaced match, `skipped` for a deduplicated/filtered-out job, `evaluated` once it has been handed to `/apply`.
  - `first_seen` is the ISO-8601 date the job was first recorded; do not overwrite it on later runs.
- The registry **grows monotonically** — entries are never removed. Only jobs not already in the registry or tracker are presented to the user.

### Geographic + Date Filtering (REQ-1010, REQ-1011)

Apply the **Location Filter Tiers** from `search-queries.md`:

- **Ideal / Acceptable** — include normally.
- **Borderline** — include but **flag** with a commute/relocation note; do **not** auto-skip.
- **Too far** — **skip** (unless the posting is remote).

Date rules:

- Skip jobs with **expired deadlines** and **closed postings**.
- Include jobs with **no determinable date**, but **flag** them as "date unknown".

### Presentation (REQ-1007)

Sort by fit (high → medium → low). Present:

1. Summary header: **`Found X new positions (Y high, Z medium, W low match)`**.
2. A table with columns: **`#, Fit, Title, Company, Location, Deadline, URL`**.
3. For **each high-match job**: 2–3 bullets on why it matches, the key requirements to check, and any red flags.
4. Then ask exactly:
   > "Want me to evaluate any of these in detail? Just give me the number(s)."

### Detailed Evaluation Handoff (REQ-1008)

- When the user picks a number (or numbers), pass that job's **URL or pasted posting text** to **`/apply`** for the full 5-dimension fit evaluation.
- Mark the handed-off job's `status` as `evaluated` in `seen_jobs.json` — the dedup registry must stay in sync with downstream handoffs.
- The **application tracker write stays in `/apply`** (REQ-1009) — this skill never writes to `job_search_tracker.csv`.

### Provider Resilience (NFR-0022)

If the AI provider rate-limits, errors, or becomes unavailable mid-search, stop
**gracefully** with a clear message and whatever partial results exist — never retry-spam
or spin. Keep parallelism modest; do not run high-volume headless batches that can trip
provider abuse heuristics (ARCH-0005).

### No Fabrication (REQ-1012, ARCH-0007)

- Present **only** jobs that came from real web-search results and have **real URLs** (or real pasted text the user supplied).
- Never invent a posting, company, or URL.
- If a search returns nothing, say so honestly — e.g. "No new postings matched your queries in the last 14 days." — rather than padding the list.
