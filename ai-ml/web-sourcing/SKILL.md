---
name: "web-google-recruiting-sourcing"
description: "Find candidates using advanced Google X-Ray sourcing, GitHub, portfolio sites, conference speaker lists, academic databases, Reddit, and other open web sources. Use when building Boolean strings for Google, sourcing outside LinkedIn, finding passive candidates on the open web, mapping talent pools, or researching candidate backgrounds in depth."
---

# Web & Google Recruiting Sourcing Skill

You are an expert at open-web talent sourcing (X-Ray searching, Boolean research, and alternative sourcing channels). Apply these workflows when the user needs to find candidates beyond LinkedIn or traditional job boards.

---

## What is X-Ray Search?

X-Ray search uses Google's indexing power to search inside a specific website using the `site:` operator combined with Boolean logic. Instead of being constrained by a platform's built-in search filters or paywalls, you use Google's massive index to surface publicly available profiles directly.

**Why it works:**
- Bypasses LinkedIn's commercial search limits and profile view restrictions for non-Recruiter users
- Finds passive candidates who will never appear on a job board
- Works on any publicly indexed site: LinkedIn, GitHub, Dribbble, Behance, personal sites, academic databases, conference sites
- Costs nothing (Google is free)

**Important limitation:** Private or non-indexed profiles won't appear. Some platforms limit how much Google indexes them. Results reflect Google's index, which may lag real-time.

---

## Google Operators for Sourcing

| Operator | What it does | Example |
|---|---|---|
| `site:` | Restrict to a specific domain | `site:linkedin.com/in` |
| `intitle:` | Term must appear in the page title | `intitle:resume` |
| `inurl:` | Term must appear in the URL | `inurl:cv` |
| `"quotes"` | Exact phrase | `"machine learning"` |
| `-` (minus) | Exclude term | `-jobs -recruiter` |
| `OR` | Either term | `Python OR Go` |
| `filetype:` | Specific file type | `filetype:pdf` |
| `..` (range) | Numeric range | `"5..10 years"` |

**Key Google rules:**
- Google's standard search has a ~32-word query limit — for very long strings, use Google's Programmable Search Engine (allows up to 500 terms)
- If Google shows "unusual traffic" warnings, you're searching too fast — slow down or use a different IP/browser session
- Results vary by logged-in vs. logged-out Google session

---

## LinkedIn X-Ray (Non-Recruiter / Recruiter Supplement)

```bash
# Basic LinkedIn X-Ray
site:linkedin.com/in/ "software engineer" "San Francisco" "machine learning"

# Refined with exclusions (removes job boards, directories, recruiters)
site:linkedin.com/in/ ("senior engineer" OR "staff engineer") (Python OR Go) "Series" -recruiter -talent -hiring -staffing -directory -intitle:"profiles"

# Data scientist with specific tools
site:linkedin.com/in/ ("data scientist" OR "ML engineer") Python "New York" -jobs -course -udemy -training

# Finding candidates at specific companies
site:linkedin.com/in/ "Google" OR "Meta" OR "OpenAI" "machine learning engineer" -recruiter

# Exec-level search
site:linkedin.com/in/ ("VP Engineering" OR "Head of Engineering" OR "Director of Engineering") "Series B" OR "Series C" -consultant -advisor
```

**Pro tips:**
- Add `-intitle:"profiles"` and `-inurl:"dir/"` to remove LinkedIn directory pages
- Add `-recruiter -talent -staffing` to exclude TA professionals from results
- Add `-jobs -hiring` to exclude job listing pages
- If results are thin, broaden the title synonyms first before loosening skills

---

## GitHub X-Ray — Engineering Sourcing

```bash
# General GitHub profile search
site:github.com "machine learning" location:"San Francisco" followers:>100

# Technology-specific with availability signal
site:github.com "Rust" "open source" bio:"available" OR bio:"open to"

# Find engineers with availability in README or bio
site:github.com/users "available for hire" Python

# Using "joined on" to isolate profile pages (not repository pages)
site:github.com "joined on" "San Francisco" (React OR Angular) "Lead" -intitle:repositories

# Company alumni sourcing
site:github.com "formerly at Google" OR "ex-Google" engineer
```

**Direct GitHub search (inside github.com):**
- Search users by location in bio: `location:Tokyo language:Python`
- Filter by language, followers, and contribution count
- Look for pinned repositories — these show what they're most proud of
- Check profile README files — many engineers explicitly post availability

---

## Resume & CV X-Ray

```bash
# Find resumes across the open web
(inurl:resume OR inurl:cv OR inurl:vitae) "software engineer" "New York" -job -jobs -sample -template -examples

# Resume with specific tech stack
inurl:resume "DevOps" "Kubernetes" "AWS" London (bachelor OR master OR degree)

# PDF resumes specifically
filetype:pdf "curriculum vitae" "data scientist" "Python" Chicago

# Portfolio + resume combo (designers)
(inurl:portfolio OR inurl:resume) "UX designer" "product design" Figma -template -wordpress
```

---

## Design Portfolio Sourcing — Dribbble & Behance

```bash
# Dribbble
site:dribbble.com "UI designer" "product design" -intitle:"jobs" -intitle:"careers"
site:dribbble.com "motion designer" "After Effects" -job

# Behance
site:behance.net "UX designer" "user research" "case study" -template

# Personal portfolio sites
intitle:portfolio "UX Designer" ("London" OR "UK") -template -jobs -wordpress -squarespace
"case study" "UX" "product design" site:*.com "available for freelance" OR "available for hire"
```

---

## Conference & Speaker Sourcing

```bash
# Conference speaker pages
site:papercall.io "distributed systems" 2024
site:sessionize.com "machine learning" "keynote" 2024

# PDF speaker lists
"[PyCon OR KubeCon OR Strange Loop OR QCon]" speakers 2024 "machine learning" filetype:pdf

# YouTube talks
site:youtube.com "talk" "distributed systems" "engineer at"

# SpeakerDeck
site:speakerdeck.com "AI" "production ML" 2024
```

---

## Academic & Research Sourcing

```bash
# Google Scholar
site:scholar.google.com "natural language processing" "PhD" 2023

# arXiv (preprints — find people working on cutting-edge problems)
site:arxiv.org "reinforcement learning from human feedback" 2024

# University lab pages
site:cs.stanford.edu "PhD student" "machine learning"
site:*.edu "PhD candidate" "computer vision" "graduating 2025"
```

---

## Community & Niche Platform Sourcing

```bash
# Stack Overflow
site:stackoverflow.com/users "Python" "distributed systems" "San Francisco"

# Reddit
site:reddit.com/r/MachineLearning "I work at" OR "at my company"
site:reddit.com/r/cscareerquestions "open to work" OR "looking for" engineer

# Dev.to / Hashnode
site:dev.to "machine learning" "tutorial" "senior engineer"
site:hashnode.com "Rust" "systems programming"

# Substack (domain experts)
site:substack.com "AI" "product" "newsletter" "formerly"

# Wellfound / AngelList
site:wellfound.com/u "product manager" "startup" "Series B"
```

---

## Alternative Sourcing Channels

| Channel | Best for | Strategy |
|---|---|---|
| **GitHub** | Engineers, open source contributors | Search by language, stars, location bio, "available" in README |
| **Dribbble** | UI/UX, motion, brand designers | Search by skill tags; check "Hire Me" profiles |
| **Behance** | Designers with case studies | Filter by "Available for work" |
| **Stack Overflow** | Developers with demonstrated technical expertise | Check top contributors in a tag |
| **Dev.to / Hashnode** | Developer bloggers and educators | Find authors writing in your stack |
| **Substack** | Domain experts, analysts, tech writers | Search topics + "formerly at" |
| **Medium** | Engineers, PMs who write about their work | Search by author + keyword |
| **Wellfound / AngelList** | Startup operators open to new roles | Filter by role, startup stage, remote preference |
| **Crunchbase** | Execs at companies with recent layoffs/pivots/acquisitions | Search by company event + filter by title |
| **YouTube** | Developer advocates, educators, speakers | Find tutorial creators in your stack |
| **Reddit** | Community members; passive candidates in niche subreddits | r/MachineLearning, r/cscareerquestions, r/forhire |
| **papercall.io / sessionize.com** | Conference speakers = domain experts who present publicly | Search by conference or topic |
| **Google Scholar / arXiv** | Researchers, PhDs, highly technical specialists | Search by topic + graduation year |
| **Product Hunt** | Product builders, founders, indie hackers | Makers tab on product launches |
| **Discord servers** | Active communities in niche technical areas | Search for relevant servers (e.g., Rust, Solidity, DevRel) |

---

## Kaggle — Data Scientist Sourcing

```bash
# Active data scientists with location in bio
site:kaggle.com "joined * ago" "python" ("amsterdam" OR "london" OR "new york")
site:kaggle.com "joined * ago" "machine learning" "senior" -course -competition

# The * wildcard covers all time variations: "joined 3 months ago", "joined 1 year ago"
# Filter for recent joiners = likely more active
```

---

## Hacker News — "Who Wants to Be Hired" Threads

HN runs monthly "Who wants to be hired?" threads (first weekday of each month) with high-quality engineers explicitly available. Low competition sourcing channel.

```bash
site:news.ycombinator.com "who wants to be hired" "machine learning" "remote"
site:news.ycombinator.com "who wants to be hired" "backend" "San Francisco" 2025
site:news.ycombinator.com "who wants to be hired" "rust" OR "golang" 2025
```

Also useful: "Who is hiring?" threads for competitive intelligence on what companies are building.

---

## Date Range Filtering

Google's **Tools menu** (below the search bar) allows date filtering — critical for finding recently updated profiles and avoiding stale results.

- **"Past year"** — filters to profiles and pages updated in the last 12 months
- **"Custom range"** — set specific windows (e.g., last 6 months for active candidates)

Use date filtering when:
- You want candidates who recently updated their profile (signals active/open)
- Finding recent papers or talks (signals current expertise)
- Avoiding outdated contact info or stale job listings in results

The `daterange:` operator (Julian dates) is cumbersome — use Google Tools instead.

---

## Iteration Discipline

Elite sourcers treat X-Ray as iterative, not one-shot. If your first results are full of recruiters or noise:
1. Identify shared terms in the bad results (e.g. "Recruiting", "Talent Acquisition", "staffing")
2. Add them to your exclusion block
3. Re-run — typically 3–5 refinement rounds to get a clean result set

**Save modular blocks, not full strings.** Keep separate blocks in a document:
- Exclusion block: `-jobs -hiring -recruiter -staffing -directory -course -training`
- Title block: `("Software Engineer" OR "Developer" OR "SWE")`
- Skill block: `(python OR golang OR rust)`
- Location block: `("San Francisco" OR "SF" OR "Bay Area")`

Combine on demand rather than rewriting from scratch.

---

## Modular Boolean String Library

Build and save a personal library of "blocks" you can mix and match:

**Title blocks (by function):**
```
# Engineering
("software engineer" OR "SWE" OR "backend engineer" OR "senior engineer" OR "staff engineer")

# Data / ML
("data scientist" OR "ML engineer" OR "machine learning engineer" OR "AI engineer" OR "MLOps")

# Design
("UX designer" OR "product designer" OR "UI designer" OR "interaction designer")

# Product
("product manager" OR "PM" OR "product lead" OR "group PM" OR "director of product")
```

**Exclusion blocks (always append):**
```
# LinkedIn X-Ray universal exclusion
-recruiter -talent -staffing -hiring -directory -jobs -course -udemy -training -intitle:"profiles" -inurl:"dir/"

# General candidate exclusion
NOT (intern OR student OR "looking to hire" OR recruiter OR HR OR consultant OR advisor)
```

**Seniority / signal blocks:**
```
("Series B" OR "Series C" OR "growth stage" OR startup OR scaleup)
("5 years" OR "7 years" OR "10 years" OR "senior" OR "lead" OR "staff" OR "principal")
```

---

## Sourcing Sprint Cadence

| Day | Activity |
|---|---|
| **Day 1** | Build Boolean strings across all relevant channels. Run X-Ray on LinkedIn, GitHub, and 2–3 alt channels. Create long list (50–100 names). |
| **Day 2–3** | Qualify long list → shortlist (15–25). Find contact info. Review public work samples, GitHub repos, writing. |
| **Day 4–5** | Send first-touch outreach across channels (LinkedIn InMail, X DM, email where available). Personalise each message with a specific observation. |
| **Day 7** | Follow up on non-responders. Adjust messaging based on response patterns so far. |
| **Day 10** | Debrief: which source/string/message performed best? Document winning strings and templates for next sprint. |

---

## Talent Intelligence & Competitive Research

When mapping a competitor org or talent market:
1. **Map the org:** LinkedIn (current employees) + Crunchbase (leadership team) + company website
2. **Track departures:** Search `"left [Company]"`, `"after [X] years at [Company]"` on LinkedIn and X
3. **Identify signals:** Recent layoff news, acquisition, funding round, pivot announcement — all drive talent mobility
4. **Find feeder companies:** Build X-Ray strings targeting specific company alumni
5. **Build a target list:** Name, LinkedIn URL, GitHub (if engineer), last known role, preferred contact method, notes
6. **Enrich with contact info tools:** ContactOut, Hunter.io, Apollo.io, Lusha, SignalHire — for email/phone when LinkedIn outreach is slow

---

## Google Alerts — Passive Signal Monitoring

Set up Google Alerts for ongoing talent intelligence:
- `"left [CompanyName]" engineer` — monitor competitor departures
- `"[niche skill] engineer" "open to"` — monitor active seekers
- `"[target candidate name]"` — for high-value prospects you're tracking
- `[industry] layoffs 2025` — catch talent availability events early
