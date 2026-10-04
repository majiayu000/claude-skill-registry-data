---
name: bird
description: X/Twitter CLI for reading, searching, timelines, bookmarks, and posting via cookie auth.
version: 1.0.0
author: local
license: MIT
metadata:
  hermes:
    tags: [X, Twitter, bird, social, timelines, search]
---

# bird

Fast X/Twitter CLI using GraphQL plus cookie-based auth.

Authentication
- Uses cookie auth.
- Preferred local usage in this environment is Firefox cookies:
  - `bird home --following -n 15 --plain --no-emoji --no-color --cookie-source firefox`
- Run `bird check` to inspect active credential sources.

Common commands
- Account:
  - `bird whoami`
  - `bird check`
- Timelines:
  - `bird home`
  - `bird home --following`
  - `bird user-tweets @handle -n 20`
  - `bird mentions`
- Reading:
  - `bird read <url-or-id>`
  - `bird thread <url-or-id>`
  - `bird replies <url-or-id>`
- Search/news:
  - `bird search "query" -n 10`
  - `bird news -n 10`
- Bookmarks/likes:
  - `bird bookmarks -n 10`
  - `bird likes -n 10`

Posting (use carefully)
- `bird tweet "hello world"`
- `bird reply <url-or-id> "text"`
- `bird tweet "caption" --media image.png --alt "description"`

Notes
- Posting is more likely to hit rate limits than read operations.
- For script-safe output, use `--plain` or `--json`.
- If query IDs go stale, run `bird query-ids --fresh`.
