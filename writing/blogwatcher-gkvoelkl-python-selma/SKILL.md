---
name: blogwatcher
description: "Watch a list of blogs or web pages for new content and report changes. Runs automatically on every heartbeat. Trigger on: watch blog, blogwatcher, überwache diese Seite, check for new articles, new posts, blog updates."
user-invocable: true
---

# Blogwatcher

## Overview
Blogwatcher checks a list of URLs at every heartbeat for new content.
It stores a content hash per URL in a state file and reports changes since the last check.

## Configuration
Blogs to watch are listed in `skills/blogwatcher/blogs.md` in the workspace.
Format — one URL per line, optional label after a space:

```
https://example.com/blog        Example Blog
https://news.ycombinator.com    Hacker News
```

Blank lines and lines starting with `#` are ignored.

## State file
State is stored in `skills/blogwatcher/state.json` in the workspace.
Format:
```json
{
  "https://example.com/blog": {
    "last_checked": "2026-01-01T12:00:00",
    "content_hash": "a1b2c3d4"
  }
}
```

## Steps (manual trigger or heartbeat)

1. **Read config** — `read` `skills/blogwatcher/blogs.md`.
   If the file does not exist, reply with setup instructions (see Setup below).

2. **Read state** — `read` `skills/blogwatcher/state.json`.
   If missing, start with an empty state object `{}`.

3. **Check each URL** — for each URL in blogs.md:
   a. `web_fetch` the URL.
   b. Compute a short hash: take the first 4000 characters, count words, build a fingerprint string `len:<chars>|words:<n>|head:<first100chars>`.
   c. Compare with stored hash.
   d. Mark as **new** if hash differs or URL is not in state yet.

4. **Write state** — update `last_checked` and `content_hash` for every checked URL, then `write` `skills/blogwatcher/state.json`.

5. **Report**:
   - If new content found → list each changed URL with label and a 1-sentence summary of what changed.
   - If nothing changed → reply `HEARTBEAT_OK` (heartbeat mode) or "No new content since last check." (manual).
   - If a URL could not be fetched → note it but continue with the others.

## Heartbeat
On every heartbeat run, execute the full Steps 1–5 above silently.
Only send a message to the user when at least one URL has new content.
Otherwise reply `HEARTBEAT_OK`.

## Setup instructions (when blogs.md is missing)
Reply:
"Blogwatcher is not configured yet. Please create `skills/blogwatcher/blogs.md` in your workspace and add one URL per line:

```
https://your-blog.com/feed     My Blog
https://example.com/news       Example News
```

Then trigger blogwatcher again or wait for the next heartbeat."
