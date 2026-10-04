---
name: research
description: Gather source material for the radio show from any content source — web, HN, GitHub, papers, or general topics.
---

# Research

Gather source material for the radio show based on the user's prompt. The research strategy is **agent-driven** — you decide how to gather content based on what the user asks for.

## Scripts

All research scripts live in `skills/research/scripts/` and output to `{workspace}/data/research/`. They use **only Python stdlib** — no dependencies.

| Script | Command | Source |
|--------|---------|--------|
| `fetch_hn.py` | `python3 skills/research/scripts/fetch_hn.py --workspace ./workspace --top 6` | Hacker News |
| `fetch_github.py` | `python3 skills/research/scripts/fetch_github.py --repo owner/repo --workspace ./workspace` | GitHub repos |
| `fetch_url.py` | `python3 skills/research/scripts/fetch_url.py --url https://... --workspace ./workspace` | Any URL |

## Script Details

### fetch_hn.py — Hacker News (two-phase)

**Phase 1: Scan** — grab top 10 story titles, scores, and comment counts (fast, no deep-diving):

```bash
python3 skills/research/scripts/fetch_hn.py --workspace ./workspace --mode scan --top 10
```

Output: `{workspace}/data/research/hn-scan.md` — a list of stories with IDs.

**You read this file, pick the 2-3 most interesting stories for radio, then run phase 2.**

When picking stories, **SKIP** anything related to politics, race, religion, international conflicts, historical controversies, gender/culture wars, or immigration. Stick to tech, programming, AI/ML, open source, science, startups, and developer culture.

**Phase 2: Deep-dive** — fetch full comment threads for the stories you picked:

```bash
python3 skills/research/scripts/fetch_hn.py --workspace ./workspace --mode deep-dive --stories 43210987,43209876
```

Output: `{workspace}/data/research/hacker-news.md` — full stories with top comments.

| Argument | Default | Description |
|----------|---------|-------------|
| `--workspace` | `workspace` | Root workspace directory |
| `--mode` | *(required)* | `scan` or `deep-dive` |
| `--top` | `10` | Number of stories to scan (scan mode only) |
| `--stories` | *(required for deep-dive)* | Comma-separated story IDs |

### fetch_github.py — GitHub Repository

```bash
python3 skills/research/scripts/fetch_github.py --repo googleapis/python-genai --workspace ./workspace
```

Accepts `owner/repo` or a full GitHub URL (`https://github.com/owner/repo`).

| Argument | Default | Description |
|----------|---------|-------------|
| `--repo` | *(required)* | GitHub repo (owner/repo or full URL) |
| `--workspace` | `workspace` | Root workspace directory |
| `--releases` | `5` | Number of releases to fetch |
| `--issues` | `8` | Number of top issues to fetch |

What it does:
1. Fetches repo metadata (stars, description, language).
2. Fetches and decodes the README.
3. Fetches recent releases with changelogs.
4. Fetches top issues by comment count, including top comments.
5. Outputs → `{workspace}/data/research/github.md`

Uses the **GitHub REST API** directly — no auth needed for public repos.

### fetch_url.py — Any URL

```bash
python3 skills/research/scripts/fetch_url.py --url https://example.com/blog-post --workspace ./workspace
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--url` | *(required)* | URL to fetch content from |
| `--workspace` | `workspace` | Root workspace directory |
| `--max-chars` | `8000` | Max chars to extract |

What it does:
1. Fetches the HTML page.
2. Strips scripts, styles, nav, footer.
3. Converts HTML to markdown-like text.
4. Extracts title and meta description.
5. Outputs → `{workspace}/data/research/url_<safe_name>.md`

Works for blog posts, documentation pages, arXiv abstracts, news articles, etc.

### General Topic (no script — agent-driven)

If the user provides a topic without a specific source:
- Use **Google Search** to find recent articles, blog posts, and discussions
- Gather multiple perspectives and opposing viewpoints
- Write the research markdown directly to `{workspace}/data/research/`

## Output

- **Directory**: `{workspace}/data/research/`
- **Format**: One or more markdown files with structured content
- All research must be saved here regardless of source — the script-writing step reads from this directory.

## What to look for

When reviewing the research output, identify:
- **Consensus**: What do most people agree on?
- **Debates**: What are the key disagreements?
- **Contrarian takes**: Any notable dissenting opinions?
- **Expert insights**: Comments or quotes from people with domain expertise.
- **Emotional stories**: Anything that would make compelling radio.
