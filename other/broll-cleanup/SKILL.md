---
name: broll-cleanup
description: Deferred end-of-run B-roll cache eviction. For ONLY the B-roll source video_ids this run ingested (from each broll_plan.json's ingested_video_ids), runs `mcptube remove <id>` AND deletes the local work/<id>/broll/*.mp4 cache. Never touches the podcast source, unrelated library videos, or broll_plan.json (placement metadata persists for editors). Runs once at the very end of a whole pipeline run.
allowed-tools: Bash
user-invocable: true
---

# broll-cleanup

Runs ONCE at the end of a whole pipeline run, after every short is saved. Takes
one or more `broll_plan.json` paths, unions their `ingested_video_ids`, and for
each: `mcptube remove <id>` plus deletes that plan's local `broll/*.mp4` cache.

Scope is strict: only the B-roll source videos this run added to mcptube (tracked
via `ingested_video_ids`) are evicted — never the podcast source or pre-existing
library videos. `broll_plan.json` itself is left intact so editors keep the
per-cutaway placement + source metadata after the heavy mp4 cache is gone.

## Invoke

```
.claude/skills/broll-cleanup/broll-cleanup.sh <broll_plan.json> [<broll_plan.json> ...]
```

Typically called with a glob over the run's plans, e.g.
`broll-cleanup.sh work/<id>/short_*/broll_plan.json`.

## Env

- `MCPTUBE_BIN` — override mcptube path.

## Behavior

- Dedups video_ids across all supplied plans (one `mcptube remove` per id).
- A `remove` that fails (id already gone) is logged, not fatal.
- Deletes each pick's `clip_path` and any straggler `*.mp4` in the `broll/` dir.
- Never edits or deletes `broll_plan.json`.
