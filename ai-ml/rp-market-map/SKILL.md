---
name: rp-market-map
model: sonnet
argument-hint: "<role title> in <location>"
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - WebFetch
  - Glob
---

# /rp-market-map — Competitive Landscape Mapper

Map the talent landscape for a specific role and market. Produces a structured brief covering: who competes for this talent, where these people currently work, what they earn, which skills are trending, and whether this is a buyer's or seller's market right now.

Uses WebSearch to pull real salary data, job posting volume, and market signals. Zero API cost beyond Claude usage.

---

## Input

Parse the user's argument to extract:
- `role_title` — the job title to map (e.g., "Senior DevOps Engineer", "Head of Product", "ML Engineer")
- `location` — city, metro, state, or "Remote US" (e.g., "Austin, TX", "New York", "Remote US")

Generate a slug from the combination: `{role-slug}-{location-slug}` (e.g., `senior-devops-engineer-austin-tx`).

If the location is missing, ask before proceeding. Location context is required for accurate comp data.

---

## Step 1: Load Config

Check if `~/.recruiter-skills/config.yaml` exists. If it does, read it. The `recruiter.specialties`, `recruiter.target_industries`, and `icp` fields provide context for which companies and candidates to prioritize in this map.

---

## Step 2: Research Phase (WebSearch)

Run the following searches in sequence. For each, extract the most relevant data points. Do not include raw search result text in the output — synthesize and attribute.

### 2a. Compensation Data
Search queries (run 2-3 of these, pick the most data-rich results):
- `"{role_title}" salary "{location}" 2025 site:levels.fyi OR site:glassdoor.com OR site:linkedin.com/salary OR site:salary.com`
- `"{role_title}" compensation range "{location}" 2025`
- `"{role_title}" pay "{location}" percentile`

Extract: base salary range (25th/50th/75th percentile if available), total comp if relevant (for tech roles), equity/bonus norms.

### 2b. Job Posting Volume and Demand
Search queries:
- `"{role_title}" jobs "{location}" site:linkedin.com/jobs OR site:indeed.com OR site:greenhouse.io`
- `"{role_title}" "{location}" hiring 2025`

Extract: approximate number of active postings, which companies are actively hiring, how long postings have been up (proxy for difficulty to fill).

### 2c. Competitor Companies (Who Hires This Role)
Search queries:
- `companies hiring "{role_title}" "{location}"`
- `"{role_title}" "{location}" team site:linkedin.com`
- top employers `{role_title}` `{location}` OR remote

Extract: 8-15 specific companies that hire this exact role in this market. Categorize by type: (a) direct competitors for talent, (b) feeder companies (where candidates come from), (c) destination companies (where candidates want to go).

### 2d. Talent Pool Locations (Where These People Currently Work)
Search queries:
- `"{role_title}" "{location}" linkedin.com/in`
- `"{role_title}" professionals "{location}"`
- `where do "{role_title}" work "{location}"`

Extract: The top 5-8 companies where this role concentration is highest right now. These are the hunting grounds.

### 2e. Skills Trends
Search queries:
- `"{role_title}" required skills 2025`
- `"{role_title}" job description requirements 2025`
- `what skills does a "{role_title}" need 2025`

Extract: must-have skills (appearing in >70% of postings), nice-to-have skills, and skills that are declining in relevance (being replaced by newer tools/tech).

### 2f. Supply/Demand Signals
Search queries:
- `"{role_title}" talent shortage 2025 OR "{role_title}" oversupply 2025`
- `"{role_title}" hiring market 2025`

Extract: Is this role in shortage (hard to fill, candidates have leverage) or surplus (many qualified applicants, clients have leverage)? Any recent layoffs or hiring freezes in this category?

---

## Step 3: Synthesize and Write the Market Map

Format the output as a structured brief. Use these exact section headers with the separator style shown:

```
MARKET MAP: {Role Title} — {Location}
Generated: {today's date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


MARKET VERDICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Supply/Demand:    CANDIDATE MARKET / BALANCED / CLIENT MARKET
Difficulty:       EASY (1-2 wks) / MODERATE (3-5 wks) / HARD (6+ wks) to fill
Comp Pressure:    RISING / STABLE / SOFTENING
[2-3 sentence summary of the market right now]


COMPENSATION RANGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Base Salary (25th pct):  $X
Base Salary (median):    $X
Base Salary (75th pct):  $X
Total Comp (if relevant): $X - $X
Equity:   [typical range or "uncommon in this market"]
Bonus:    [typical % or "not standard"]

Notes: [any caveats — remote premium, startup vs enterprise delta, etc.]


WHO COMPETES FOR THIS TALENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tier A (Top-pay, hardest to pull from):
  - [Company] — [why they're a strong retainer]
  - ...

Tier B (Reachable — realistic sourcing targets):
  - [Company] — [brief note]
  - ...

Feeder Companies (Where talent comes from before going to Tier A):
  - [Company] — [note]
  - ...


WHERE THEY CURRENTLY WORK (Sourcing Targets)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Highest concentration of this title:
  1. [Company] — [estimated count or confidence level]
  2. ...

Search tips:
  - LinkedIn search: title:"{role_title}" company:[top companies]
  - GitHub search (for technical roles): [specific language/tool] contributors in [location]


REQUIRED SKILLS (what every JD asks for)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Must-have:   [comma-separated list]
Nice-to-have: [comma-separated list]
Fading out:  [skills that were standard but are being replaced]
Emerging:    [skills starting to appear in job postings that will be standard by 2026]


ACTIVE HIRING (companies posting right now)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Company] — [role variant they're hiring] — [number of postings if found]
...

Observations: [any patterns — e.g., "3 companies posted in last 2 weeks, suggesting a wave"]


RECRUITER NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[3-5 practical bullets a recruiter needs to know before working this market.
Examples: candidate leverage, common objections, title inflation patterns,
remote vs in-office norms, red flags to probe in screening,
things clients consistently underestimate about this role.]
```

---

## Step 4: Save Output

Target path: `~/.recruiter-skills/data/research/market-map-{slug}.md`

Ensure the directory exists:
```bash
mkdir -p ~/.recruiter-skills/data/research
```

Write the full formatted brief to that file. Confirm the path at the end of your output.

---

## Step 5: Suggest Next Step

After delivering the map, suggest ONE action based on what the data showed:

- If active job postings were found at specific companies: "Run `/rp-signals {company}` to check for fresh hiring signals at [top company from the active hiring list]."
- If the role looks hard to fill (candidate market, HARD difficulty): "Run `/rp-source {role} in {location}` (requires RapidAPI key) to begin candidate sourcing with the talent pools identified above."
- If the recruiter doesn't have candidates yet for this role: "Run `/rp-resume-screen` with any resumes you have to quickly identify who fits the comp and skills profile above."

---

## Output Format Rules

- Use plain text with the separator and header style shown above. No markdown `##` headers.
- Attribute data sources inline when relevant ("per Glassdoor data", "based on LinkedIn job postings").
- If data wasn't findable for a section, say so explicitly: "[Could not find reliable comp data for this location/title — suggest using Levels.fyi manually for this one]"
- Do not fabricate salary figures. If search results are thin, give a range with explicit low confidence note.
- Keep the brief scannable — a recruiter should absorb it in under 5 minutes.
