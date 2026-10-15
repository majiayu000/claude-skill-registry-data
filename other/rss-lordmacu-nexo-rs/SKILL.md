---
name: RSS / Atom
description: Fetch and parse RSS, Atom, and JSON feeds.
requires:
  bins: []
  env: []
---

# RSS / Atom

Fetch news / blog / podcast feeds. Backed by the `rss` extension using `feed-rs`
(handles RSS 2.0, Atom 1.0, JSON Feed).

## Use when

- "What's new on Hacker News / this blog / this podcast?"
- Heartbeat digest: "what happened today in my feeds"
- Monitoring release notes / changelog feeds

## Do not use when

- Real-time Twitter / Discord / Slack — different channels
- Free-form HTML scraping — use `fetch-url`

## Tools

- `status` — extension info
- `fetch_feed` — `url` + optional `limit` (default 20, max 100), `include_content` (default false)

Entries are normalized to `{id, title, link, published, summary, content, authors}`,
sorted newest first.

## Tips

- `include_content: false` by default — keeps responses small. Flip it when you
  need the body text (e.g. to pass into `summarize`).
- Combine with `rss` + `summarize` + heartbeat to give kate a daily digest.
