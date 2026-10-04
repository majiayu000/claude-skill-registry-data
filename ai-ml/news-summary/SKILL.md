---
name: news-summary
description: Summarize monitor and latest feeds into a concise briefing. Use when the user asks for recent AI news, trends, launches, or a daily/weekly summary.
---

# News Summary Skill

For news briefings, call these two tools simultaneously:

1. `fetch_monitor` — tracks notable AI model/lab announcements (always call first)
2. `fetch_latest_feed` — news from last 24h; add `include_hype=true` if the user wants trending community projects; use `days_back=7` for a weekly digest

Do NOT use a separate hype tool — hype is a parameter on `fetch_latest_feed`.

## Output format

Group updates by theme:
- **Model launches & updates** — new releases, capability announcements
- **Research & benchmarks** — notable papers, benchmark shifts
- **Products & integrations** — tools, APIs, partnerships
- **Community buzz** (only if include_hype=true) — trending repos, viral projects

For each item:
- One-line headline
- Why it matters (1 sentence)

End with a **Watchlist** of 2-3 items worth following up on, and a concrete recommendation for what to read/try first.

## Scope guidance

- Daily briefing: `days_back=1`
- Weekly digest: `days_back=7`
- Community focus: add `include_hype=true`
- Topic deep-dive: after the news summary, use `ask_perplexity` or `search_openrouter_models` for follow-up on specific items
