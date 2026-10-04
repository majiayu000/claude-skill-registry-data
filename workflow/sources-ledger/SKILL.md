---
name: sources-ledger
description: Maintain work/sources.json — the registry of which source videos have been processed into shorts. Scans every work/<id>/ingest.json + the output/<slug>/ folder it produced, recording title, url, duration, the produced shorts (with grades/tiers), current disk footprint, and active|reaped status. Also mirrors a keyed per-source bd memory so future sessions recall what's already been clipped (and can re-ingest from the saved URL). Pure deterministic scan, idempotent, no Claude. The "memory" half of the disk-hygiene pair (reap-source is the "cleanup" half).
allowed-tools: Bash
user-invocable: true
---

# sources-ledger

The registry of what's been clipped. Answers "have I already made shorts from this video?" and "where did a reaped source come from?" without decoding opaque `work/<sha1>` hashes.

## Usage

```bash
sources-ledger.sh sync          # rebuild work/sources.json from work/ + output/
sources-ledger.sh record <id>   # upsert one source (pipeline end-of-run / reap)
sources-ledger.sh show          # print the registry
```

## Output: `work/sources.json`

An array, newest-ingested first, one entry per source that has an `ingest.json`:

```json
{
  "id": "ac3763ad4c",
  "slug": "we-broke-into-mrbeast-s-studio",
  "title": "We Broke Into MrBeast's Studio",
  "url": "https://www.youtube.com/watch?v=y8K6QazBqrY",
  "uploader": null,
  "duration_sec": 5726.174,
  "ingested": "2026-06-01",
  "shorts": [ { "name": "....mp4", "grade": 72, "tier": "GOLD", "path": "output/<slug>/....mp4" } ],
  "shorts_count": 3,
  "status": "active",
  "reaped": null,
  "work_bytes": 2782512345
}
```

- `slug` is computed identically to `start.sh` (kebab of the source title, falling back to the work id) so it maps `work/<id>` → `output/<slug>/`.
- `status` is `reaped` once `source.mp4` is gone or a `.reaped` marker exists (written by `reap-source`); otherwise `active`.
- `shorts` reads each delivered `output/<slug>/*.mp4` and its co-located `*.grade.json`.

## bd memory

`record` also upserts a keyed memory (`--key source-<id>`) summarizing the source + how to re-ingest, best-effort (skipped if `bd` is absent). Keyed, so re-runs update in place rather than duplicating.

## Where it runs

- **Pipeline end-of-run** — `start.sh` calls `sources-ledger.sh record <id>` after a source's shorts are saved, so the registry is always current.
- **`reap-source`** calls `record <id>` after reaping to flip `status` → `reaped`, then a final `sync`.
- **Standalone** — `sync` backfills the whole registry from existing `work/` dirs.
