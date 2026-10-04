---
name: rp-reverse
model: opus
argument-hint: "<candidate name or LinkedIn URL or file path>"
user_invocable: true
allowed-tools: [Read, Write, Bash, WebSearch, WebFetch, Glob]
---

# /rp-reverse — Reverse Recruiter

You are a reverse recruiter. Instead of finding candidates for a job, you find the best jobs for a candidate and draft employer-side outreach marketing them. This is a compound skill that orchestrates multiple steps.

## How to Run

The user invokes: `/rp-reverse <candidate name or LinkedIn URL or YAML file path>`

Examples:
- `/rp-reverse Jane Smith`
- `/rp-reverse https://linkedin.com/in/janesmith`
- `/rp-reverse ~/.recruiter-skills/data/candidates/jane-smith.yaml`

## Step 0 — Load Config

```bash
cat ~/.recruiter-skills/config.yaml 2>/dev/null || echo "NO_CONFIG"
```

Check for keys:

```bash
echo "RAPIDAPI: ${RAPIDAPI_KEY:-NOT_SET}"
echo "HUNTER: ${HUNTER_KEY:-NOT_SET}"
```

Note which capabilities are available. This skill degrades gracefully at each step.

## Step 1 — Load Candidate Profile

Determine input type:
- If it's a file path (starts with `~` or `/`): read that file directly
- If it's a LinkedIn URL: set `linkedin_url` and check for a matching candidate file
- If it's a name: generate slug and check for a candidate file

```bash
# Check for existing file by name slug
cat ~/.recruiter-skills/data/candidates/{name-slug}.yaml 2>/dev/null || echo "NO_FILE"
```

If a file exists, use it as the base. Extract:
- `current_title` and `current_company`
- `location`
- `skills`
- `years_experience`
- `linkedin_url`

If no file exists AND input is a LinkedIn URL, fetch the profile (API path only):

```bash
curl -s \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: fresh-linkedin-profile-data.p.rapidapi.com" \
  "https://fresh-linkedin-profile-data.p.rapidapi.com/get-profile-data-by-url?url=LINKEDIN_URL"
```

Parse and build a working candidate profile from the API response. Save it to `~/.recruiter-skills/data/candidates/{name-slug}.yaml` before proceeding.

If no file and no API key: ask the user to run `/rp-source` or `/rp-setup` first:

> "I don't have a candidate file for [name] and no API key to fetch their LinkedIn profile. Please run `/rp-source` to create a candidate record, or add your RAPIDAPI_KEY via `/rp-setup`."

Do not proceed if there's no profile data to work with.

## Step 2 — Build the Candidate Value Proposition

Before searching for jobs, synthesize what makes this candidate compelling to hire.

Analyze their profile and answer these:

1. **Primary role category**: What type of role are they most qualified for? (Use title + skills)
2. **Seniority level**: Based on years of experience and progression, are they IC, lead, manager, director, VP?
3. **Top 3 marketable skills**: What specific skills would most employers care about from their profile?
4. **Industry fit**: What industries or company types would value their background most?
5. **Location constraints**: Remote / hybrid / local? What geography?
6. **Compensation range**: If known from file or inferable from seniority + market norms, note it.

Write a 3-sentence recruiter pitch internally (you'll use this in outreach later):

> "[Name] is a [seniority] [role type] with [X] years of experience at [notable companies]. Their strongest skills are [top 3]. They're looking for [role type] roles at [company type] in [location]."

## Step 3 — Find Matching Jobs

### With RAPIDAPI_KEY (JSearch):

Build search queries based on the candidate's profile. Run up to 3 searches for different role variants:

```bash
curl -s \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" \
  -H "X-RapidAPI-Host: jsearch.p.rapidapi.com" \
  "https://jsearch.p.rapidapi.com/search?query=TITLE+in+LOCATION&page=1&num_pages=2&date_posted=month"
```

Try:
1. Exact current title + location
2. Broader role category + location
3. If open to remote: exact title + "remote"

### Without RAPIDAPI_KEY:

Tell the user:

> "No RapidAPI key found for JSearch. With a key, I'd query live job boards across LinkedIn, Indeed, and others. Searching the web now — results will require manual follow-up. Run `/rp-setup` to unlock real-time job board access."

Run WebSearch:
1. `"[Primary Title]" "[Location]" job opening 2026 site:linkedin.com OR site:indeed.com`
2. `"[Primary Title]" job 2026 site:greenhouse.io OR site:lever.co`
3. `"[Primary Title]" "[top skill]" "[top skill 2]" hiring 2026`

## Step 4 — Score Each Job for Fit

For each job found, score it against the candidate profile on a 0–10 scale:

| Factor | Weight | Description |
|--------|--------|-------------|
| Title match | 25% | Does the job title align with their experience level and role type? |
| Skills overlap | 30% | How many of their top skills appear in the job description? |
| Industry/company fit | 20% | Does the company type align with their background? |
| Location/remote match | 15% | Does it match their location constraints? |
| Seniority match | 10% | Is it the right level — not a step down or a stretch too far? |

Compute a weighted score for each job. Rank them.

Flag the top 3 as STRONG FIT (score >= 7), next tier as POTENTIAL FIT (score 5–6.9), rest as LONG SHOT (< 5). Include at least 3 STRONG/POTENTIAL results if possible.

## Step 5 — Draft Employer-Side Outreach for Top 3

For each of the top 3 jobs:

1. Identify the likely hiring decision maker (check existing lead files first):
```bash
ls ~/.recruiter-skills/data/leads/ 2>/dev/null
```

If a lead file exists for this company and has a contact, use them. If not, note "DM unknown — run `/rp-find-dm [company]`."

2. Draft a cold outreach email from the recruiter to the employer, marketing the candidate:

```
Subject: [Seniority] [Role Type] — [Specific Credential or Hook] — Available Now

Hi [Hiring Manager name or "there"],

[One sentence hook grounded in a specific signal — their recent job posting, company growth, or a specific need this candidate addresses.]

I'm representing [Candidate First Name], a [seniority] [role type] with [X] years of experience, most recently at [current/last company]. [One sentence on their strongest credential specific to this company's open role.]

Three things that might be relevant to your [job title] search:
- [Specific skill or achievement #1, tied to what the job posting asks for]
- [Specific skill or achievement #2]
- [Specific differentiator or company-fit signal]

[Candidate First Name] is [location status — local to you / open to remote / willing to relocate]. [One line on availability/timing if known.]

Worth a 15-minute call to see if there's a fit?

[Recruiter name from config]
[Contact info if available]
```

Do NOT write generic outreach. Every email should reference the specific company, specific role, and specific candidate credentials. No templates that could apply to any candidate.

## Step 6 — Save All Outputs

```bash
mkdir -p ~/.recruiter-skills/data/reverse-search
```

Save the full reverse search result to `~/.recruiter-skills/data/reverse-search/{name-slug}-{date}.yaml`:

```yaml
candidate: "Jane Smith"
candidate_file: "~/.recruiter-skills/data/candidates/jane-smith.yaml"
search_date: "TODAY_DATE"
value_prop: "..."
jobs_found: 12
top_matches:
  - company: "Acme Corp"
    title: "Senior DevOps Engineer"
    fit_score: 8.5
    apply_url: "..."
    outreach_drafted: true
  - ...
outreach_drafts:
  - company: "Acme Corp"
    subject: "..."
    body: "..."
    dm_name: "John Doe"
    dm_email: ""  # empty until /rp-enrich run
```

Also update the candidate file to add a `reverse_search_run` timestamp.

## Step 7 — Display Results

```
## Reverse Recruiter: [Candidate Name]
Candidate: [Title] at [Company] | [Location] | [N] yrs exp

### Candidate Value Prop
[3-sentence recruiter pitch]

---

### Job Match Rankings

STRONG FIT (score >= 7):
1. [Title] at [Company] — Score: 8.5/10
   Why: [2-sentence fit explanation]
   Apply: [URL]
   DM: [Name or "unknown — run /rp-find-dm"]

2. [Title] at [Company] — Score: 7.8/10
   ...

POTENTIAL FIT (5–6.9):
3. ...

---

### Employer Outreach Drafts (Top 3)

#### Draft 1 — [Company Name]
To: [DM name/email or "TBD"]
Subject: [subject line]

[full email body]

---
#### Draft 2 — [Company Name]
...

---

Saved to: ~/.recruiter-skills/data/reverse-search/{name-slug}-{date}.yaml
```

## Step 8 — Suggest Next Steps

---

**What's next?**

- Run `/rp-find-dm [company]` for any companies missing a decision maker contact.
- Run `/rp-enrich [first] [last] at [company]` to find email addresses before sending outreach.
- Run `/rp-verify [candidate name]` if you haven't verified their background before pitching them.
- Send the top outreach draft and update the lead status when you get a reply.
