---
name: import-old-photos
description: Turn a folder of old geotagged photos into a browsable retroactive trip with just import-photos (photo import, backfill a past trip from the camera roll).
---
# Import old photos

`just import-photos` reads each file's EXIF capture time and GPS position and
posts compressed copies (2048 px long-edge JPEG — originals never leave your
machine) to the live API as photo events, forming a retroactive trip.

## Read first
- tools/README.md — "import-photos — retroactive trips" section.
- flink/README.md — "Retro trips" note, if the imported trip should get stays.

## Commands
```bash
just import-photos ~/Photos/iceland --name "Iceland · Sep 2023" \
  --endpoint https://api.travel.michaelwheeler.ai/v1/produce --token <owner-token>
```
- `--endpoint` / `--token` default to `WOS_PRODUCE_URL` / `WOS_OWNER_TOKEN`.
- `--dry-run` prints the plan without uploading; `--concurrency 3` controls parallel uploads.

## Gotchas
- Idempotent by construction: event ids derive from file content hashes and the trip id from the set of hashes — re-running the same import is a no-op, not a duplicate trip.
- Photos without a usable EXIF timestamp are skipped with a warning; file modification time is never trusted as capture time.
- This goes through the live `/v1/produce` API (owner token required), so imported events flow through Kafka to every consumer like any capture.
- Imports arrive out of order relative to live capture — the graph-writer's splice path handles that; no manual ordering needed.
- Stays (the dwell segments the Flink job derives) are not generated for imports unless you replay the trip while the job runs: `just live-up`, `just replay --trip <id>`, wait, `just live-down`.
