---
name: perplexity-fetch-url
description: Read one or more known URLs through Perplexity Sonar Pro fetch_url_content. Use when the user wants content extracted or verified from specific pages.
---

# Perplexity Fetch URL

Use this skill for the Fetch URL mode.

1. Run `python3 perplexity-fetch-url-content/scripts/fetch_url_content.py <url> [url ...] --json`.
2. Add `--mode summary` for concise summaries or `--mode qa --question "..."` for targeted questions.
3. Add `--require-fetch` when every requested URL must be confirmed.
4. Report `fetched_urls` and `missing_requested_urls` when relevant.
