---
name: scout-sources
description: Deterministic source-video discovery — the clip-channel "outlier" method, keyless. Searches seed niche queries via yt-dlp ytsearch, prefilters to long-form candidates, fetches full metadata, and ranks by outlier score (views/day velocity, views-per-subscriber ratio, comment engagement, replay-heatmap peakiness). Emits a ranked candidates.json to pick the next pipeline source from. No Claude call, no API key.
allowed-tools: Bash
user-invocable: true
---

# scout-sources

Answers "what video should we clip next?" deterministically instead of by vibes.
Professional clip channels hunt **outliers** — videos performing far above their
channel's baseline. The cheap keyless proxies, all available from yt-dlp:

- **velocity** `2 * log10(1 + views/day)` — reach × freshness
- **outlier** `min(10, views/subscribers)` — 3x+ is real signal, 5–10x is strong
- **engagement** `min(5, comments per 1k views)` — talked-about-ness
- **peaky** `min(3, 10 * stdev(replay heatmap))` — a spiky most-replayed graph
  means the video CONTAINS clippable moments; flat means evenly mediocre
- **curiosity** `min(1.5, question/superlative framing in the title)` — sources
  whose own title is a curiosity hook ("how come…", "richest woman ever") yield
  the cold-open question moments the pipeline now leads with

`score = velocity + outlier + engagement + peaky + curiosity` (see `score.py`).

## Invoke

```
.claude/skills/scout-sources/scout-sources.sh [out.json] [query ...]
```

- `out.json` (optional): default `work/_scout/candidates.json`
- `query ...` (optional): seed searches; default reads `niches.txt` (channel
  analytics — humor pods + productivity/AI — plus visually-rich, question-driven
  niches: space, wealth, true-crime, nature, history)

Env knobs: `SCOUT_PER_QUERY` (12 results/query), `SCOUT_SHORTLIST` (20 full
fetches), `SCOUT_MIN_VIEWS` (100000), `SCOUT_DUR_MIN`/`SCOUT_DUR_MAX`
(900/10800s — long-form only).

## Output

`candidates.json` with ranked candidates (url, title, channel, score +
components, `seen: true` when `work/<sha1(url)[:10]>` already exists) and a
ranked table on stdout. Feed the winner straight to `start.sh <url>`.

## How

1. Parallel flat `ytsearch` per query — `view_count`/`duration`/`channel` only
   (one cheap call per niche).
2. Merge, dedup, drop live/short/low-view, keep top-N by views.
3. 4-way-parallel full `yt-dlp -J` per shortlisted id — adds `upload_date`,
   `channel_follower_count`, `comment_count`, `heatmap`.
4. `score.py` ranks and writes `candidates.json`.

NOT part of the per-video pipeline — run it before `start.sh` to decide what
to feed the pipeline. Uses plain `yt-dlp` ytsearch (NEVER `mcptube discover`,
which needs a forbidden LLM API key).
