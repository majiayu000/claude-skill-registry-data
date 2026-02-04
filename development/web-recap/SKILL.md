---
name: web-recap
description: Extract browser history for finding URLs by topic or getting visit stats. Use when user asks about their browsing history, visited websites, or what they were doing online.
---

# web-recap

Extracts browser history from Chrome, Chromium, Brave, Firefox, Safari, Edge. Run `web-recap --help` for all flags.

## Key Flags

```
--date YYYY-MM-DD        Specific date (local timezone)
--start-date YYYY-MM-DD  Start of range
--end-date YYYY-MM-DD    End of range
--time HH                Specific hour (e.g., --time 14 for 2pm-3pm)
--browser NAME           chrome|firefox|safari|edge|brave|auto
```

## Output Format

JSON with `entries` array. Each entry has: `timestamp`, `url`, `title`, `domain`, `visit_count`, `browser`.

## Usage Patterns

**Never dump raw output.** Use jq to reduce tokens.

### Search (find URLs by topic)

```bash
# Find entries matching a topic (searches title, domain, url)
web-recap | jq '[.entries[] | select(.title + .domain + .url | test("KEYWORD"; "i"))] | unique_by(.url) | map({title, url, domain})'
```

### Stats (visit overview)

```bash
# Domain counts, sorted by visits
web-recap | jq '[.entries[].domain] | group_by(.) | map({domain: .[0], count: length}) | sort_by(-.count)'
```

### Quick metadata

```bash
web-recap | jq '{start: .start_date, end: .end_date, total: .total_entries}'
```
