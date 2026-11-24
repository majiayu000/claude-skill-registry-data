---
name: "github-sourcing"
description: "Source software engineers, open source contributors, and technical candidates via GitHub. Use when building GitHub search strings, finding engineers by language or location, mining company orgs for alumni, evaluating candidate profiles, identifying available engineers, or using GitHub as a talent intelligence tool."
---

# GitHub Sourcing Skill

You are an expert at sourcing technical talent via GitHub. Apply these workflows whenever the user needs to find engineers, evaluate technical candidates, or use GitHub as a sourcing channel.

---

## Why GitHub Works for Sourcing

GitHub is the highest-signal sourcing channel for engineers — candidates show actual work, not just claimed experience. Key advantages:
- **Proof of skill** — real code, real contributions, real projects
- **Low competition** — only 31% of tech recruiters use GitHub regularly
- **Open network** — profiles, repos, and contributions are mostly public
- **Availability signals** — many engineers explicitly mark themselves as available
- **Recency signals** — commit activity shows who is actively coding now
- **Company alumni** — org pages reveal engineers who've worked on specific codebases

**Best roles for GitHub sourcing:** Software engineers (all levels), ML/AI engineers, DevRel, open source contributors, data engineers, security researchers, blockchain/Web3 engineers.

---

## Native GitHub Search — User Search

Go to `github.com/search?type=users` for direct user search.

### Key Native Filters

| Filter | Syntax | Example |
|---|---|---|
| Language | `language:python` | Engineers who primarily code in Python |
| Location | `location:"San Francisco"` | Must match bio text — no normalisation |
| Followers | `followers:>50` | Community reputation signal |
| Repos | `repos:>10` | Active contributors |
| Recent activity | `pushed:>2025-01-01` | Committed code in 2025 |
| Topic | `topic:machine-learning` | Profile/repo tagged with topic |

### Example Native Searches

```bash
# Python engineers in London, active in 2025
language:python location:"London" followers:>25 pushed:>2025-01-01

# ML engineers in San Francisco with reputation
language:python location:"San Francisco" followers:>50 topic:machine-learning

# Rust engineers anywhere, high reputation
language:rust followers:>75

# Frontend engineers in Berlin
language:javascript location:"Berlin" OR location:"Germany" followers:>20

# Go engineers, actively committing
language:go pushed:>2025-01-01 followers:>30

# DevRel / Developer Advocates (check bios)
# Search GitHub bio text isn't directly supported natively — use Google X-Ray below
```

**Location caveat:** GitHub doesn't normalise location text. "San Francisco", "SF", "Bay Area", "San Francisco, CA" are all different entries. Run multiple location variants or use Google X-Ray (more flexible).

---

## GitHub X-Ray via Google

More flexible than native search — Google's index allows bio text searching and multi-location variants.

```bash
# Profile pages only (not repos) — use "joined on" to isolate profiles
site:github.com "joined on" "machine learning" "San Francisco" followers:>50

# Available engineers
site:github.com "available for hire" python "london"
site:github.com "open to work" react "san francisco"
site:github.com/users "available" golang -template -example

# Engineers with location variants
site:github.com "joined on" ("San Francisco" OR "SF" OR "Bay Area") python

# Engineers explicitly mentioning availability in bio or README
site:github.com "open to opportunities" ("javascript" OR "typescript") -template

# Language + seniority signal
site:github.com "joined on" "senior" (rust OR golang) "distributed systems"

# Find engineers at/from specific companies
site:github.com "formerly at Google" OR "ex-Google" engineer
site:github.com "previously at Stripe" developer

# DevRel / Developer Advocates
site:github.com "developer advocate" OR "devrel" "open source" -jobs

# Security researchers
site:github.com "security researcher" OR "pen tester" bug bounty

# Data engineers
site:github.com "data engineer" (spark OR kafka OR "airflow") "joined on"

# Blockchain / Web3
site:github.com "solidity" OR "web3" "smart contracts" ("london" OR "berlin") "joined on"
```

---

## Follower Count as Quality Signal

Follower count on GitHub is a strong proxy for community reputation and visibility:

| Followers | Signal | What it means |
|---|---|---|
| 2–10 | Good | Active contributor, solid output |
| 11–25 | Very good | Known in their niche community |
| 26–75 | Excellent | Respected practitioner, referenced by others |
| 75+ | Field leader | Community figure, likely highly sought after |

**Important:** High followers ≠ best engineer. Some engineers do deep internal work without public presence. Use follower count as a signal, not a filter — combine with repo quality and commit activity.

---

## Evaluating a GitHub Profile

When reviewing a candidate's GitHub profile, assess in this order:

1. **Pinned repositories** — what they're most proud of; check language, stars, forks, last commit
2. **Contribution graph** — consistency of commits over time; gaps may indicate job search, burnout, or life events
3. **Star count on owned repos** — others found their work useful enough to bookmark
4. **Fork count** — others built on their work
5. **README quality** — how they communicate; engineers who write clearly tend to collaborate well
6. **Languages** — breadth vs depth; check if primary language matches role requirement
7. **Bio text** — availability signals, current role/company, location, contact email
8. **Followers/following ratio** — high followers relative to following = respected, not just a networker
9. **Recent activity** — last commit date; inactive for 6+ months may indicate not currently coding

**Profile README (if present):** Many engineers include an explicit availability statement, career goals, or contact info in a profile README. Always scroll down to check for one.

---

## Mining Company GitHub Organisations

Navigate to `github.com/[company-name]` → **People tab** to see all public contributors to their repos.

```bash
# Examples
github.com/stripe → People tab → engineers who've committed to Stripe repos
github.com/airbnb → People tab
github.com/shopify → People tab
github.com/openai → People tab
```

**Why this works:**
- Shows engineers who've actually worked on the company's codebase
- Includes ex-employees who no longer list the company on LinkedIn but still have contributions
- Often surfaces engineers who haven't updated their profile elsewhere
- Click through each profile to check if they're still at the company or have moved on

**Finding alumni specifically:**
- Go to company org People tab
- Cross-reference each profile with LinkedIn to identify who has left
- Recently departed engineers from high-signal companies are prime targets

---

## GitHub Topics — Finding Specialists

GitHub's topic system lets engineers tag their repos and profiles with technology areas. Use topic search to find specialists:

```bash
# In native GitHub search
topic:machine-learning language:python
topic:kubernetes language:go
topic:react language:javascript
topic:security language:python
topic:solidity (Web3/blockchain)
topic:rust-lang

# Via Google X-Ray
site:github.com "topics" "machine-learning" "reinforcement-learning" "london"
```

---

## Finding Emails on GitHub

Many engineers list contact emails publicly. Check in order:

1. **Profile bio** — email sometimes listed directly
2. **Profile README** — longer bio where engineers often list contact info
3. **Commit metadata** — some engineers' emails appear in public commit history (use with care for GDPR contexts)
4. **Linked personal site or portfolio** — often linked in bio; may have contact email
5. **Cross-reference with Hunter.io** — if you know their employer, Hunter finds work email by domain

---

## Availability Signals on GitHub

Engineers signal availability in several ways:

| Signal | Where to find it | Strength |
|---|---|---|
| "Available for hire" in bio | Profile bio text | ★★★★★ |
| "Open to work" in bio | Profile bio text | ★★★★★ |
| Profile README with availability section | Scroll below pinned repos | ★★★★★ |
| Reduced commit frequency (then spike) | Contribution graph | ★★★ |
| New repos with portfolio-style content | Pinned repos | ★★★ |
| Following many companies on GitHub | Following list | ★★ |

---

## GitHub for Competitive Intelligence

**Find engineers at competitor companies:**
```bash
# Direct org mining
github.com/[competitor-company] → People tab

# X-Ray for company employees
site:github.com "works at [Company]" OR "engineer at [Company]"
site:github.com "[Company]" "senior engineer" "joined on"
```

**Find who recently left a competitor:**
```bash
site:github.com "formerly at [Company]" OR "ex-[Company]" engineer
site:github.com "previously at [Company]" developer
```

**Find engineers working on a competitor's open source project:**
- Go to competitor's public repo → Insights → Contributors
- Cross-reference contributor usernames with LinkedIn for contact info
- Committers to major open source projects often aren't employees — they're enthusiasts

---

## GitHub API for Advanced Sourcing

For high-volume or automated sourcing, the GitHub API provides programmatic access:

```bash
# Search users via API (no auth — 10 req/min; with token — 30 req/min)
https://api.github.com/search/users?q=language:python+location:London+followers:>50

# Get user profile
https://api.github.com/users/{username}

# Get user's repos
https://api.github.com/users/{username}/repos?sort=updated
```

**Python snippet for basic user search:**
```python
import requests

params = {
    "q": "language:python location:London followers:>50",
    "per_page": 30,
    "sort": "followers"
}
r = requests.get("https://api.github.com/search/users",
                 params=params,
                 headers={"Authorization": "token YOUR_GITHUB_TOKEN"})
users = r.json()["items"]
for u in users:
    print(u["login"], u["html_url"])
```

**Rate limits:** 10 unauthenticated requests/minute; 30 authenticated. Create a free GitHub token for sourcing scripts.

---

## Sourcing Sprint — GitHub Workflow

1. **Define target:** Language, location, seniority signal (follower count)
2. **Native search first:** Quick scan for explicit availability signals
3. **Google X-Ray second:** More flexible location/bio text matching
4. **Company org mining:** If targeting alumni from specific companies
5. **Profile evaluation:** Pinned repos → contribution graph → bio → README
6. **Contact extraction:** Bio email → personal site → Hunter.io fallback
7. **Cross-reference LinkedIn:** Confirm current role, find connection paths
8. **Log to ATS:** Name, GitHub URL, LinkedIn URL, language stack, availability signal, contact email, source date
