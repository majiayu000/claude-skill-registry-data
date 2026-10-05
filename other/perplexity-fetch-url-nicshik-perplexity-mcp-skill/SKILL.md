---
name: perplexity-fetch-url
description: Fetch URL mode through Perplexity Sonar Pro fetch_url_content. Use when the user provides one or more URLs and wants page content extracted or answered from those URLs.
---

# Perplexity Fetch URL

Use this skill for Fetch URL mode when the user wants Perplexity to read known URLs through a local script path that works both in a global Windsurf install and from the repository root.

Rules:

- Run `python3 ~/.codeium/windsurf/skills/perplexity-fetch-url/fetch_url_content.py <url> [url ...] --json` for a global Windsurf install, or `python3 perplexity-fetch-url-content/scripts/fetch_url_content.py <url> [url ...] --json` from the repository root.
- Use `--mode summary` for short summaries, `--mode qa --question "..."` for a focused question, and default max-text when the user asks to extract as much useful content as possible.
- Use `--require-fetch` when the user needs confirmation that every URL was actually fetched.
- Report `fetched_urls`, `missing_requested_urls`, and `usage.cost.total_cost` when present.
- Do not claim this returns raw HTML or a guaranteed complete verbatim page dump.
