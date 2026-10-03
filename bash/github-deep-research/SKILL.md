---
name: github-deep-research
description: "Multi-round deep research on any GitHub repo via API."
allowed-tools:
  - bash
  - web_search
  - browse_page
  - write_file
enabled: true
related-skills: [deep-research]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# GitHub Deep Research

Multi-round research combining GitHub API, `web_search`, and `browse_page` to
produce comprehensive markdown reports on any GitHub repository.

> **Poirot note:** The original deer-flow skill uses a bundled
> `scripts/github_api.py` helper. Poirot doesn't bundle that script, so this
> version uses `bash` with `curl` to the GitHub API directly + `gh` CLI when
> available.

## When to Use

- User provides a GitHub repository URL
- User asks for comprehensive analysis, timeline reconstruction, competitive
  analysis, or in-depth investigation of an open source project
- User wants to understand a project's architecture, history, or community

## Research Workflow

- Round 1: GitHub API (repo metadata, README, file tree, contributors, commits)
- Round 2: Discovery (web search for overview, competitors)
- Round 3: Deep Investigation (architecture, timeline, community sentiment)
- Round 4: Deep Dive (commit history, issues/PRs for feature evolution)

## Round 1 — GitHub API

### Setup

```bash
# Resolve owner/repo from remote URL
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
# Or user provides owner/repo directly
OWNER="owner"
REPO="repo"
```

### Repo metadata via curl

```bash
# Repo summary
curl -s "https://api.github.com/repos/$OWNER/$REPO" | python3 -c "
import sys, json
r = json.load(sys.stdin)
print(f'Name: {r[\"full_name\"]}')
print(f'Description: {r[\"description\"]}')
print(f'Stars: {r[\"stargazers_count\"]}')
print(f'Forks: {r[\"forks_count\"]}')
print(f'Language: {r[\"language\"]}')
print(f'License: {r.get(\"license\",{}).get(\"spdx_id\",\"N/A\")}')
print(f'Created: {r[\"created_at\"][:10]}')
print(f'Updated: {r[\"updated_at\"][:10]}')
"

# README
curl -s "https://api.github.com/repos/$OWNER/$REPO/readme" | python3 -c "
import sys, json, base64
r = json.load(sys.stdin)
print(base64.b64decode(r['content']).decode('utf-8'))
"

# Recent commits
curl -s "https://api.github.com/repos/$OWNER/$REPO/commits?per_page=10" | python3 -c "
import sys, json
for c in json.load(sys.stdin):
    print(f'{c[\"sha\"][:7]} {c[\"commit\"][\"author\"][\"date\"][:10]} {c[\"commit\"][\"message\"].splitlines()[0][:80]}')
"

# Languages
curl -s "https://api.github.com/repos/$OWNER/$REPO/languages"

# Contributors
curl -s "https://api.github.com/repos/$OWNER/$REPO/contributors?per_page=10" | python3 -c "
import sys, json
for c in json.load(sys.stdin):
    print(f'{c[\"login\"]:20s} {c[\"contributions\"]} commits')
"
```

### Via gh CLI (if available)

```bash
gh repo view $OWNER/$REPO
gh api repos/$OWNER/$REPO/commits --paginate | head -50
```

## Round 2 — Discovery (3-5 web_search)

- Get overview and identify key terms
- Find official website/docs
- Identify main players/competitors

## Round 3 — Deep Investigation (5-10 web_search + browse_page)

- Technical architecture details
- Timeline of key events
- Community sentiment
- Use `browse_page` on valuable URLs for full content

## Round 4 — Deep Dive

- Analyze commit history for timeline
- Review issues/PRs for feature evolution
- Check contributor activity

## Report Structure

1. **Metadata Block** — Date, confidence level, subject
2. **Executive Summary** — 2-3 sentence overview with key metrics
3. **Chronological Timeline** — Phased breakdown with dates
4. **Key Analysis Sections** — Topic-specific deep dives
5. **Metrics & Comparisons** — Tables, growth charts
6. **Strengths & Weaknesses** — Balanced assessment
7. **Sources** — Categorized references
8. **Confidence Assessment** — Claims by confidence level

## Confidence Scoring

| Confidence | Criteria |
|------------|----------|
| High (90%+) | Official docs, GitHub data, multiple corroborating sources |
| Medium (70-89%) | Single reliable source, recent articles |
| Low (50-69%) | Social media, unverified claims, outdated info |

## Citation Format

Always include inline citations: `[citation:Title](URL)` immediately after each
claim from external sources.

## Output

Save report as: `.poirot/outputs/research_{topic}_{YYYYMMDD}.md`

## Best Practices

1. **Start with official sources** — Repo, docs, company blog
2. **Verify dates from commits/PRs** — More reliable than articles
3. **Triangulate claims** — 2+ independent sources
4. **Note conflicting info** — Don't hide contradictions
5. **Distinguish fact vs opinion** — Label speculation clearly
6. **Always include inline citations**
