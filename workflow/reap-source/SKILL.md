---
name: reap-source
description: Reclaim disk by deleting a PROCESSED source's heavy artifacts — the full podcast source.mp4 (re-downloadable from its saved URL), every clip_NN.* stage intermediate, the b-roll cutaway cache, and the source's mcptube ingest (via broll-cleanup). KEEPS all lightweight JSON (ingest/transcript/topics/segments/grade/broll_plan) as the on-disk memory and updates the sources-ledger registry. Manual only — never auto-runs in the pipeline. Refuses a source with no finished shorts in output/ unless --force. The "cleanup" half of the disk-hygiene pair (sources-ledger is the "memory" half). Deterministic, non-fatal, idempotent (re-reaping a reaped source is a no-op).
allowed-tools: Bash
user-invocable: true
---

# reap-source

`work/` accumulates ~25× the size of the finished shorts: the full podcast download and every per-stage `clip_NN.*.mp4` linger forever, while the deliverable is already safe in `output/`. This reaper deletes the heavy reclaimable stuff and keeps the cheap JSON that records what was done.

## Usage

```bash
reap-source.sh <id>             # reap one source (e.g. 81d2d55a40 or work/81d2d55a40)
reap-source.sh <id> --dry-run   # show what would be freed, delete nothing
reap-source.sh <id> --force     # reap even with no finished shorts in output/
reap-source.sh --backlog        # reap every source whose shorts are in output/
reap-source.sh --backlog -n     # dry-run the whole sweep (recommended first)
```

## What it deletes vs keeps

**Deletes (heavy, reclaimable):**
- `source.mp4` — the full podcast; re-downloadable any time from the URL in `ingest.json`
- `clip_*.{mp4,mov,wav,m4a,webm,mkv}` — every per-stage intermediate (the bulk of the bloat)
- `broll/` — the cutaway cache, plus the source's mcptube ingest (db/frames/chroma) via `broll-cleanup`

**Keeps (cheap, the memory):**
- all `*.json` — `ingest.json`, `transcript.json` (expensive whisper output), `topics.json`, `segments.json`, every `*.broll_plan.json`, `*.grade.json`
- all `*.txt` / `*.path` / `*meta` sidecars

After reaping it writes a `.reaped` marker (date + bytes freed), calls `sources-ledger record <id>` to flip the registry entry to `status:reaped`, then a final `sources-ledger sync`.

## Safety

- **Manual only.** Nothing in the pipeline auto-reaps. The decision is yours.
- **Gated.** Refuses a source that has no finished `output/<slug>/*.mp4` unless `--force` — so a failed/half-run source isn't reaped before it ever delivered.
- **Re-downloadable.** To restore a reaped source: `bash start.sh work/<id>` (or re-ingest from its saved URL). `transcript.json` is kept, so re-transcription is skipped on a re-run.
- **Idempotent.** Re-reaping an already-reaped source is a no-op. Non-fatal — per-file errors don't abort a `--backlog` sweep.

## Restore a reaped source

```bash
bash start.sh work/<id>     # re-ingests source.mp4 from the saved URL; transcript.json is reused
```
