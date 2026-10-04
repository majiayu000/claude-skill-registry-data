---
name: first-span-feedback
description: The pre-fanout LEARNING GATE. start.sh finishes SPAN 0 alone (through the normal edit/captions/completion chain) before any lane launches, then this skill records a shot-scraper `video` demo of a generated per-span REVIEW PAGE (the 9:16 player + the grade/tier + the retention signals with the failing one flagged), has a Claude reviewer WATCH it via a contact sheet (like director-pass), and — when the reviewer names a SYSTEMIC defect that clears a hard three-gate re-verify (re-render span 0, grade≥prev + flagged signal cleared, re-record + re-review defect-gone) — makes a PERMANENT codebase change and commits only the fixer's paths, so every later span in the run and every future run inherits the fix. NON-FATAL everywhere (missing shot-scraper / record fail / parse fail / rejected gate / push fail all leave span 0 and the code untouched, exit 0). Idempotent via .fsfmeta. Gated by FIRST_SPAN_FEEDBACK (default 1), bounded by FSF_MAX_ITERS (default 1). Wired into start.sh / shorts.sh; autopilot.sh inherits it.
---

# first-span-feedback

The one moment a run STOPS on its first delivered span, shows it to a reviewer, and lets that feedback steer the rest of the run — the only pipeline step that can change a skill's *code or default* so a defect caught on span 0 never recurs. `grade-clip`/`director-pass`/`fix-cold-open` only ever patch one clip's pixels in place; this loop makes the correction stick.

## Usage

```bash
first-span-feedback.sh <work_id> <clip_stem> <slug> <saved_mp4> [--pane <tmux>]
```

Invoked by the entrypoint at the Phase 1 → fan-out seam, right after span 0 is saved and before the lanes claim spans 1…N.

## How it works

1. **Record** — `build_page.py` fills `page-template.html` from `clip_00.grade.json` (grade/tier + retention signals, failing signal flagged) into `work/<id>/_preview/span0-review.html`; `storyboard.py` emits a `shot-scraper video` storyboard that serves the page over a throwaway `python -m http.server` (a real `http://127.0.0.1` origin so `<video>` autoplays) and plays span 0 through once; `uvx shot-scraper video` records `span0-demo.mp4`.
2. **Review** — the demo is sampled into ONE labelled contact sheet (reusing `director-pass/frames.py`), `build_prompt.py` assembles the sheet + `grade.json` signals + the transcript, and ONE Claude vision call returns a verdict: `{defect, defect_class, signal, where, rationale}`. `parse_reply.py` extracts it with a deterministic `{"defect": false}` fail-safe.
3. **Fix + three-gate re-verify + commit** *(Phases 2-3 — not in this slice)* — a flagged systemic defect drives an agentic fixer, a hard re-render → re-grade → re-review accept, and a fixer-path-scoped commit + push.

**Phase 1 status:** record → review → write `span0-feedback.json` + `.fsfmeta`, exit 0. A flagged defect is *surfaced only* (`action: fix_pending`); no fixer, no git, no commit yet.

## Artifacts — `work/<id>/_preview/`

- `span0-review.html` — the generated review page.
- `storyboard.yml` — the shot-scraper storyboard (server + play scene).
- `span0.mp4` / `span0-demo.webm` / `span0-demo.mp4` — the served clip copy + the recorded demo.
- `review/sheet.png` + `prompt.txt` + `reply.txt` — the contact sheet, reviewer prompt, and raw reply.
- `span0-feedback.json` — the persisted verdict `{work_id, clip, demo, reviewed, verdict{…}, action, phase}`.

## Knobs

- `FIRST_SPAN_FEEDBACK` (1) — `0` disables the gate entirely (no `_preview/`, no review).
- `FSF_MAX_ITERS` (1) — fixer review→apply rounds *(Phase 2)*.
- `FSF_FRAMES` (12) — frames sampled into the contact sheet.
- `FSF_PORT` (8917) — port for the throwaway http.server that serves the review page.
- `FSF_REPLY_FILE` — test seam: a canned verdict file stands in for the live reviewer (mirrors `DIRECTOR_REPLY_FILE`).
- `FSF_RERENDER_CMD` — entrypoint-injected span-0 re-render command; unset ⇒ surface-only, never a code change *(Phase 2)*.

## Guarantees

- **NON-FATAL** — a missing `shot-scraper`, a record failure, a parse failure — all leave span 0 and the code untouched and exit 0, so fan-out proceeds on unchanged code.
- **Idempotent** — `.fsfmeta` = `mtime(span0.mp4)|mtime(grade.json)|FIRST_SPAN_FEEDBACK|v1`; a resumed run skips a loop that already ran.
- **Isolated dependency** — `shot-scraper` runs through `uvx` in an ephemeral env (`playwright ≥ 1.61`), never touching the vendored 1.60 Node Playwright in `like-subscribe-overlay`.
- **Reuses, never edits** — `director-pass/frames.py` for the contact sheet, `_lib/pane.sh` for the reviewer dispatch, `grade-clip`'s `grade.json` as the gate oracle.
