---
name: director-pass
description: An agentic, vision-driven final QA/repair pass — a Claude "director" WATCHES the finished short (a contact sheet of frames sampled across the whole clip + the transcript + the sidecar plans) and decides, in natural language, what is broken ANYWHERE (cold open, dead/rambling tail, a tonally-wrong b-roll match, a wrong-person punch-in, mistimed captions, a too-hot music bed, a flat hook) — not just the cold open, not just a fixed route vocabulary. It then APPLIES the fixes it can from a bounded, pixel-safe set (tail_trim via cut-clip; music_down via a bg-music re-mix) and SURFACES everything else as an honest edit list, re-reviewing up to DIRECTOR_MAX_ITERS times. Layered ON TOP of grade-clip (the cheap proxy floor) + fix-cold-open (the closed-vocab cold-open repair). NON-FATAL, idempotent (.dpmeta). Two modes — preventive in-chain (the pre-mix .ctaed.mp4 + clip_NN.* sidecars are co-located, so music_down can re-mix) and curative standalone/backlog (a finished output clip → tail_trim only, everything else surfaced — never fabricate a baked-in repair).
---

# director-pass

The expensive open-ended per-clip quality loop the deterministic grade→route suite (`grade-clip` + `fix-cold-open`) is the cheap floor under. `grade-clip` scores a closed set of pre-enumerated proxy signals and `fix-cold-open` repairs only the cold-open routes it knows; `director-pass` has a model actually WATCH the delivered short and judge it like a strict editor — catching the long tail of "this just feels off" issues a human would fix, anywhere in the clip, in natural language. It binds that open-ended judgment to a BOUNDED applier so it stays safe, bounded, and non-destructive.

## Usage

```bash
director-pass.sh <clip.mp4> [--pane <tmux>]     # single / in-chain (runs after speed-up, before save-local)
director-pass.sh --backlog [output_dir]          # sweep output/<src>/*.mp4 -> output/_director.json
```

- Writes `<clip-stem>.director.json` (the edit-list report) and, only when a fix actually changed pixels, `<clip-stem>.dir.mp4` (the repaired clip).
- `--pane` routes the vision call through a long-lived Claude tmux pane (same path as `verify-bookends` / `broll-pick`); without it, `claude -p`.

## How it works (per clip, looped up to `DIRECTOR_MAX_ITERS`)

1. **Watch** — `frames.py` samples `DIRECTOR_FRAMES` (12) frames evenly across the whole clip and composes ONE labelled contact sheet (4-col grid, each cell stamped with its timestamp). The burned captions, b-roll, framing, title/end cards are all visible — the reviewer judges what it sees.
2. **Review** — `build_prompt.py` assembles the sheet + the spoken script (scaled into finished-clip time, since the clip is sped 1.25× while the sidecars are pre-speed) + the fill-shot kinds, b-roll windows, cadence, title, mood, and any `grade.json` signals into one prompt. ONE Claude vision call returns a structured edit list.
3. **Validate** — `parse_reply.py normalize` extracts the JSON (tolerates fences/prose), clamps every `where`, and validates each op against the SUPPORTED set; anything unsupported or out-of-range is downgraded to `surface`.
4. **Apply** — the bounded applier runs the validated ops (music re-mix first, then tail trim), re-invoking existing atomic skills.
5. **Re-review** — with `DIRECTOR_MAX_ITERS>1`, re-watch the repaired clip and repeat until the reviewer says `ship` or an iteration applies nothing.

## The bounded applier (the safety boundary)

The review is open-ended; the APPLIER is a closed, pixel-safe vocabulary so the pass can never corrupt a clip. Everything else the reviewer flags is recorded in `surfaced[]` (for a human / a pipeline re-run), never auto-applied.

| op | when the reviewer picks it | how it's applied | mode |
|---|---|---|---|
| `tail_trim {t1}` | the clip rambles/dies after the payoff | `cut-clip` to `[0,t1]` (frame-accurate) + re-fire `end-card` so the new tail lands on the CTA beat | both (PIXEL-SAFE: trimming the end never desyncs anything earlier) |
| `music_down {volume}` | the bed drowns the speech | re-run `bg-music` on the pre-mix `.ctaed.mp4` at the lower volume → `end-card` → `speed-up` (reproduces the phase-4 tail, same timeline, quieter bed) | preventive only (needs `.ctaed.mp4`; curative → surfaced) |
| `surface` | cold-open defect, bad b-roll, wrong-person punch, mistimed caption, flat hook, anything else | NO pixel change — recorded with its `where` + `rerun_recommended` | both |

`cold_open` / `broll_wrong` / `wrong_person` / `caption_mistime` are surfaced (with `rerun_recommended`) rather than faked: their clean repair lives upstream of the whole finishing chain (b-roll re-composite, fill-vertical re-punch) — the preventive in-chain `fix-cold-open` already owns the cold-open routes earlier in the pipe, and re-deriving the rest from a finished clip would mean re-running the entire back half. `director-pass` is honest about that boundary instead of shipping a degraded re-crop.

## Report — `<clip-stem>.director.json`

```json
{
  "clip": "...", "mode": "preventive|curative", "iterations": 1,
  "verdict": "ship|revise|revised|disabled",
  "summary": "<one-line director read>",
  "applied":  [{"op":"tail_trim","t1":26.0,"result":"..."}],
  "surfaced": [{"op":"surface","kind":"cold_open","where":[0.0,1.9],"detail":"...","rerun_recommended":true}],
  "output": "<clip>.dir.mp4 | <unchanged input>",
  "rerun_recommended": false
}
```

Backlog aggregate `output/_director.json`: `{generated, n, revised:[{clip,applied}], surfaced:[{clip,issues}], clean:[clips]}`.

## Knobs

- `DIRECTOR_PASS` (1) — `0` disables (passthrough report, no review).
- `DIRECTOR_MAX_ITERS` (1) — review→apply rounds per clip.
- `DIRECTOR_FRAMES` (12) — frames sampled into the contact sheet.
- `DIRECTOR_MIN_DUR` (15) — a `tail_trim` may never leave the clip shorter than this.
- `DIRECTOR_BED_VOL` (0.17) — the current bg-music bed volume `music_down` proposes a reduction from.
- `DIRECTOR_MODE` (`auto`) — force `preventive`|`curative`.
- `DIRECTOR_REPLY_FILE` — test seam: a canned reply file stands in for the live model (offline proof of the applier).

## Guarantees

- **NON-FATAL** — missing input/sidecars, an unreadable clip, a failed sub-skill, or a malformed/empty review → input untouched, a `ship`/`disabled` report, exit 0.
- **No fabrication** — never writes `.dir.mp4` unless an op actually changed pixels; never fakes a repair it lacks the source artifacts to do cleanly (those are surfaced as `rerun_recommended`).
- **Idempotent** — `.dpmeta` over the clip + consumed-sidecar mtimes + knobs → a 2nd run is a cache hit.
- **Owns only its dir** — re-fires existing skills (`cut-clip`, `end-card`, `bg-music`, `speed-up`) by their published `.sh` contracts; never edits them.
