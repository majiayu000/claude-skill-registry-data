---
name: fix-cold-open
description: Deterministic, grade.json-routed repair of a short's cold open (the first ~2s swipe gate). Reads a clip's grade.json fix_routes and runs gated ops in order — broll_open_truncate (drop any b-roll cutaway overlapping [0,FIXCO_OPEN_GUARD_SEC] and re-composite so frame 1 is the speaker), shot0_repunch (re-run fill-vertical face detection on the 16:9 source when fillplan shot0.kind != face), credit_rerender / card_rerender (re-fire brand-overlays / title-transition). Two modes — PREVENTIVE in-chain (the 16:9 source + .vert.fillplan.json + .broll_plan.json all live in work/<id>/, so every op is clean) and CURATIVE standalone (a finished output clip whose defect is baked into pixels with no recoverable source → emits rerun_recommended, NEVER a fake degraded re-crop). NON-FATAL — any error leaves the input untouched and exits 0. Idempotent (.fixmeta).
---

# fix-cold-open

Deduction-targeted repair of the cold-open swipe-gate defect, driven by `grade-clip`'s `grade.json`. The single highest-ROI move on the backlog: converts a `face_withheld` / cold-open-b-roll FIXABLE clip to uploadable without a 30-step re-pipe.

## Usage

```bash
fix-cold-open.sh <clip.mp4> [grade.json]
```

- `grade.json` is auto-found if omitted: `<clip>.grade.json`, then (for in-chain `clip_NN.*` inputs) `clip_NN.final.grade.json` / `clip_NN.grade.json`.
- Reads `grade.json`'s `fix_routes` (the EXACT vocabulary from `SELECTION-SUITE-CONTRACT.md`) and dispatches the gated ops.
- Writes a repaired `.mp4` only when an op actually changed pixels, a `.fixmeta` signature, and a `<clip>.fix.json` report: `{mode, ran:[routes], skipped:[{route,reason}], output, rerun_recommended:bool}`.

## Modes (`FIXCO_MODE=preventive|curative`, default `auto`)

**PREVENTIVE (in-chain, primary deliverable)** — runs on `clip_NN.broll.mp4` / `.brolled.mp4` where the 16:9 source (`clip_NN.src16.path`), `.vert.fillplan.json`, `.broll_plan.json`, and the clean pre-b-roll vertical (`.sw.mp4` / `.zoom.mp4` / `.jc.mp4` / `.vert.mp4`) all live in `work/<id>/`. Here every op is clean. Output: `clip_NN.fixed.mp4`.

**CURATIVE (standalone backlog)** — a finished `output/<src>/x.mp4` usually has NO co-located sidecars and the face is already BAKED into pixels inside a b-roll cutaway. It cannot be recovered without the 16:9 source. When the source/plans are NOT co-located, fix-cold-open emits `rerun_recommended` and makes NO pixel change — it never fabricates a fake repair (re-cropping the already-vertical frame toward a face that isn't there would just zoom into the b-roll, a regression). If `work/<id>` artifacts ARE co-located (e.g. an in-chain stem), it repairs in place. `letterbox` is always `rerun_recommended` (old render, structurally non-repairable).

## The gated ops (in order)

1. **`shot0_repunch`** — `fillplan.shots[0].kind != "face"` (the face-withheld defect). Re-runs `fill-vertical` on the 16:9 source (`src16.path`). This RE-RUNS face detection — identity clusters are NOT persisted, a real per-clip cost, flagged in logs. Adopted only when the new shot0 comes back `kind == "face"`; the re-punched vertical becomes the clean base for the b-roll re-composite that follows.
2. **`broll_open_truncate`** — drops every `broll_plan.picks` window overlapping `[0, FIXCO_OPEN_GUARD_SEC]` (default 2.2s) and re-runs `broll-composite` onto the clean pre-b-roll vertical so frame 1 is the speaker, not a cutaway. (Also the carrier for a `shot0_repunch` result.)
3. **`credit_rerender`** — re-fires `brand-overlays` (`ingest.json` co-located) for the credit-lit-at-open defect.
4. **`card_rerender`** — re-fires `title-transition` (`title.txt` co-located) for the centered-blocking-card defect.

If `shot0_repunch` succeeds but there is no b-roll carrier to re-composite onto (so the new framing exists but lacks the downstream caption/title/brand chain), the skill surfaces `rerun_recommended` rather than ship a caption-less clip — honest about what a standalone pass can and can't finish.

## Knobs

- `FIXCO_OPEN_GUARD_SEC` (default 2.2) — a b-roll pick overlapping `[0, this]` is a cold-open cutaway → truncated.
- `FIXCO_MODE` = `preventive|curative` (default `auto`: preventive when source/plans co-located, else curative).

## Guarantees

- **NON-FATAL** — missing input, missing grade, unreadable video, or any sub-skill failure → input untouched, exit 0, honest report.
- **No fabrication** — never produces a `fixed.mp4` unless an op actually changed pixels; never re-crops toward a face that isn't in the pixels.
- **Idempotent** — `.fixmeta` (mtime of clip+grade, guard, mode, routes) → 2nd run is a cache hit.
- **Owns only its dir** — re-fires existing skills (`fill-vertical`, `broll-composite`, `brand-overlays`, `title-transition`) by their published `.sh` contracts; never edits them.
