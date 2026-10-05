---
name: broll-overlay
metadata: {packVersion: 1.3.0}
description: >-
  Overlays silent b-roll cutaway clips onto a finished base video — the base
  audio keeps running underneath while the picture cuts away and returns, and
  the final duration always equals the base duration. Use when the user asks to
  add b-roll, add cutaways, or overlay clips on a video: "add b-roll to this",
  "cut away to a product shot here", "overlay these clips on my UGC ad". Entered
  from an approved base video plus its transcript, which comes from
  POST /v1/transcripts and needs no local install; it never generates the base
  itself and it never extends a video.
---

# B-roll overlay

Lays silent cutaway clips **over** a finished base video: the base audio runs
untouched underneath, the picture cuts away and returns, and the final duration
equals the base duration exactly. That is the whole contract — overlay, never
concatenation. A previous run concatenated: 24s for a 15s base, voice dead 12s.

Assembly mechanics live entirely in `scripts/broll_overlay.py`; this file is
judgment only — when to enter, where the windows go, what the user sees first.

## Entry condition

Two things must already exist. This skill never generates the base — if there
isn't one yet, say so and stop.

1. **A finished, approved base video with exactly one audio stream.** Approved
   means the user has watched it and signed off — b-roll is a polish pass over a
   locked cut. The script stream-copies one voice track under the picture, so a
   two-stream base is rejected: `ffmpeg -i base -map 0:v -map 0:a:0 -c copy`.
2. **Its transcript, with timings.** One call to **`POST /v1/transcripts`** with
   the base's `jobId` (or its `assetId` if it was uploaded). It returns `text`,
   word-level `words[]` and `segments[]` — **timings in SECONDS**, which is what
   the EDL below takes — plus an `srt` you can ignore here. **Price it with the
   transcript arm of `POST /v1/estimates` and quote that number**, never one from
   this file. The meter is per minute of source, rounded up from a one-minute
   minimum, and **a repeat of the same source is free**, so asking twice costs
   once. No local install.

   *(The **captions** endpoint still cannot supply this — it burns subtitles into
   a new MP4 and returns no text or timings, verified 2026-08-04 and re-checked
   when transcripts shipped. That finding is correct and is kept here so nobody
   re-discovers it and files a bug against captions.)*

   **Offline fallback:** a local whisper pass (`whisper-cli` or `openai-whisper`)
   still works and is the path when there is no API key or no network. Note
   whisper reports timings in **milliseconds** where the API reports seconds, and
   `whisper-cli` with no model downloaded returns an EMPTY transcript rather than
   an error — which reads exactly like a bad render. See README for the model
   download.

   Placement is read from the transcript, not eyeballed.

> **REST key required. A Novoads MCP connector is not a substitute.** If
> `NOVOADS_API_KEY` is missing or still the placeholder, stop before any
> generation work and tell the user: "Before continuing, create an API key at
> <https://novoads.ai/dashboard/settings?tab=api> and paste it into `.env`."
> That holds even when `mcp__novoads__*` tools are connected and authenticated in
> the session. Never call `mcp__novoads__*` tools from this repo's workflows: they
> are a different surface with different behavior, including the units they quote
> costs in. Repo installs verify with `./scripts/check-novoads-env.sh`; a solo
> install checks `NOVOADS_API_KEY` in the environment.

**Pack version.** Every `/v1` response carries `X-Novoads-Pack-Version`; mention a newer pack at <https://github.com/novoads/agent-skills> only when that header names a version NEWER than this file's `metadata.packVersion` — equal or older is nothing to say, and it is never a reason to stop.

## Workflow

1. **Read the transcript.** Note what is said and when — the words drive every
   decision below.
2. **Generate the b-roll clips, only after base approval.** One clip per moment
   you intend to cover, each rendered silent (`audioEnabled: false`). Overlay
   audio is ignored by the script regardless, and generating before approval
   spends credits on a cut that may still change.
   **Price the set live first — `POST /v1/estimates` this session, the total
   shown against the user's balance, an explicit yes.** Four cutaways is four
   charges, and a remembered price is not a price.
   **Cast the base actor in every cutaway that shows a person:** pass the same
   `referenceAssetIds` the base used — Seedance re-casts every render, and a
   stranger's hands or skin breaks the ad (observed live 2026-08-04: Black base
   actor, five white-cast cutaways). With no identity ref, keep people out of
   frame entirely — objects and environments, not "face out of frame".
3. **Propose an EDL.** JSON with `base`, `output`, and `overlays` (`file`,
   `start`, `end`, `covers`). `covers` is mandatory and **quotes the spoken line
   the window illustrates** — a window you can't quote is one you're guessing at.
4. **Show the EDL to the user and wait for approval.** Rendering before the user
   has seen the plan is precisely the failure this step prevents.
5. **Render:** `python3 scripts/broll_overlay.py edl.json`
6. **Report the script's verification output verbatim** — the measured durations,
   the audio check and the window count, not a paraphrase. Then offer 2–3 cut
   variations (different windows, fewer cutaways, a tighter opener) to react to.

## Placement judgment

Default cadence, measured 2026-08-04 frame by frame from the reference edit this
pack reproduces — ~15.5s, 10–11 shots, a cut every ~1.4s:

- **Alternate A-B-A-B: the face returns between every cutaway.** Never two
  overlay windows back to back; the talking head is the spine.
- **4–6 windows per 15s, ~1–1.5s each, ~40–45% coverage.** Short and frequent.
  This retires our older "fewer, longer windows" rule — taste, reversed by
  measurement; our own two renders ran 2 windows of 2.5s/2.0s, ~30% coverage.
- **The b-roll may travel; the base never does.** The reference visits 4
  distinct b-roll settings across 2–3 rooms; the talking head never moves.
- **Never cover the opening hook beat.** The first beat is a face making a
  claim; cutting away there spends the retention the hook just bought.
- **End on the person, not on b-roll.** The closing beat is the verdict, and it
  only lands if the viewer is looking at whoever delivers it.
- **Put product shots where the product is being spoken about.** B-roll that
  illustrates the current sentence reads as evidence; anything else is filler.

**Default shot plan.** The reference's five cutaways tell one arc: problem →
stress → product macro → dose/usage → relief — 2 product shots to 3 emotional
beats. Adapt the imagery to the script, keep the ratio.

Evidence: one measured edit (n=1) — a default, not a law; depart deliberately and
say why (evals.md OV3/OV6). Every run prints its own cadence against this
envelope; `--stats` prints it without rendering.

## Hard rule: assembly always goes through the script

Never hand-write overlay or concat ffmpeg for this task. `broll_overlay.py` owns
validation, rendering and verification, and it fails loudly on exactly what
fails silently by hand: duration drift, re-encoded audio, overlapping or
zero-frame windows, a clip shorter than its window, a rotated phone base
composited at the wrong geometry, a window that quietly composited nothing.
Improvised ffmpeg is how the founding failure happened.

**It needs ffmpeg 7.1 or newer.** The script scales each overlay against the base
branch with `scale=w=rw:h=rh`, and those reference constants arrived in 7.1. On an
older build — Ubuntu 24.04's apt ships 6.1 — the graph does not parse and the
error names `rw`, not a version. Check with `ffmpeg -version` before blaming the
EDL; on Debian/Ubuntu the fix is a static build, not `apt install ffmpeg`.

**Escape hatch:** if a request genuinely doesn't fit the EDL model — a speed
ramp, a picture-in-picture inset, audio that actually needs editing — say so and
ask the user how to proceed. Do not improvise around the script.

## Other modes

- `python3 scripts/broll_overlay.py edl.json --dry-run` — validate the EDL and
  print the plan, rendering nothing. Cheap way to check window geometry.
- `python3 scripts/broll_overlay.py edl.json --stats` — window count, lengths,
  coverage, base-return gaps, each marked against the envelope. Never an error.
- `python3 scripts/broll_overlay.py --verify-only FINAL --base BASE [--edl edl.json]`
  — re-check any output against its base, including one from an old session.
  **Pass `--edl` whenever you have it:** without it the check is duration +
  audio only, which a plain copy of the base also passes; with it each window's
  midpoint frame is compared against the base, so a window that composited
  nothing fails. A run without `--edl` says so out loud.

Exit codes: `2` validation, `3` render, `4` verification. A nonzero exit is a
real failure — surface it, don't retry blindly. Renders go to a hidden temp file
beside the output, renamed only after verification passes: a failed run never
leaves a half-written or unverified file at the output path.

## Evals

`evals.md` defines the six scenarios this skill is held to (OV1–OV6).
`scripts/test_broll_overlay.py` implements the mechanical ones against synthetic
fixtures — run it after touching the script.
