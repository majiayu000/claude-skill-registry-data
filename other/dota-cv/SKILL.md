---
name: dota-cv
description: >
  Governs computer vision in Dota AI Coach — extracting information from
  the player's own screen via Windows Graphics Capture, ROI extraction,
  preprocessing, recognition, confidence scoring, temporal smoothing, and
  ObservableState output. Use whenever implementing, modifying, or
  reviewing screen capture, region-of-interest handling, image
  recognition for HUD/portrait/scoreboard/minimap elements, or any code
  that reads pixels from the game client. CV in this project may only
  read what's actually rendered on screen — never infer hidden
  information — so this is a fair-play boundary as much as a technical
  guide; consult it and `dota-fairplay` together before shipping any new
  CV feature.
---

# Dota Computer Vision

## Allowed purpose

CV exists in this project to **extract information already visible on
the player's own screen** — nothing more. This is a narrower mandate than
"extract useful information about the game": if a fact isn't actually
rendered in the current frame, CV has no legitimate way to know it, full
stop. This mirrors `dota-fairplay`'s `VISIBLE_SCREEN` classification
directly — CV is, definitionally, the system component that produces
`VISIBLE_SCREEN`-classified data, and only that.

## Potential sources

All of the following are legitimate CV targets *because* they're
rendered on the player's own screen during normal play — not because
they're generically "visible" in some looser sense:

- **draft portraits** — hero picks/bans shown during the draft phase.
- **top hero bar** — the row of hero portraits/status shown during the
  match.
- **selected unit HUD** — stats/abilities/items for whatever unit is
  currently selected/inspected.
- **visible inventory** — item slots for a hero currently shown (the
  player's own, or an enemy's when their portrait/HUD is on-screen
  during a fight — see `references/allowed-sources.md` for the exact
  boundary this implies).
- **scoreboard** — the tab/score-panel view, when open.
- **kill feed** — the on-screen kill notification log.
- **visible minimap state** — only what the minimap actually renders
  (visible units/wards), never a fog-of-war-reconstructed view.

See `references/allowed-sources.md` for per-source detail on exactly what
"visible" means for each — several of these have a real, non-obvious
boundary (e.g. the top hero bar shows some info about heroes regardless
of current vision, which needs careful handling — see that file).

## Architecture

```
Windows Graphics Capture
→ ROI (region-of-interest extraction)
→ preprocessing
→ recognition
→ confidence
→ temporal smoothing
→ ObservableState
```

Each stage's job, in brief (full detail in `references/pipeline.md`):

1. **Windows Graphics Capture** — captures the actual rendered frame
   from the game window. This is the only legitimate input to the whole
   pipeline — everything downstream must trace back to an actual
   captured frame, never a substituted or cached "equivalent" value from
   another source (see the fair-play rule below).
2. **ROI** — crops the captured frame down to the specific screen
   regions each recognition target needs (draft portraits, HUD, etc.),
   using known UI geometry.
3. **Preprocessing** — normalizes a cropped region for recognition
   (scaling, color normalization, etc.) — see
   `references/resolution-and-scaling.md` for why this stage carries
   more weight in this project than in a typical CV pipeline.
4. **Recognition** — extracts the actual structured value from a
   preprocessed region (which hero portrait is this, what does this
   HUD text say).
5. **Confidence** — every recognition result carries a confidence score;
   see the confidence-threshold rule below.
6. **Temporal smoothing** — combines recognition results across frames
   to reduce jitter/noise before producing a stable observation.
7. **ObservableState** — the CV pipeline's final output: structured,
   confidence-scored observations, in the shape `dota-architecture`'s
   State Merger expects as CV's contribution to `MatchState`.

Full detail: `references/pipeline.md`.

## Rules

- **Process only visible information.** Every recognition target must
  correspond to something the player's own client actually renders —
  see "Potential sources" above and `references/allowed-sources.md`.
- **No hidden information inference.** CV must never attempt to
  reconstruct or estimate something not actually on screen (e.g. an
  enemy's likely inventory based on gold/time heuristics rather than an
  actually-visible portrait) — that's not a CV task at all, it's a
  strategic inference task that belongs (if it belongs anywhere) in a
  clearly-labeled, non-live-classified analysis layer, never disguised as
  a CV observation. See `references/fairplay-coordination.md`.
- **No screenshots stored by default.** Captured frames/ROIs are
  transient processing input, not a persisted artifact — see
  `references/privacy-and-storage.md` for the narrow, explicit-opt-in
  exceptions (e.g. debugging a misrecognition) and how to handle them
  safely.
- **Prefer fixed-region classification over heavyweight detection when
  geometry is known.** Dota's UI has fixed, known layouts (the HUD,
  portrait rows, scoreboard) — use that geometry directly (crop known
  regions, classify a small fixed set of possibilities) rather than
  reaching for general-purpose object detection where a much simpler,
  faster, more reliable approach works. See
  `references/recognition-approach.md` for when detection is actually
  warranted (e.g. minimap unit positions, which aren't fixed-region).
- **Account for resolution, aspect ratio, DPI, and UI scaling.** Fixed-
  region geometry is only fixed *relative to the game's own UI
  coordinate space* — translating that to actual captured pixels requires
  handling all four of these correctly, or ROI extraction silently
  breaks on any player whose setup differs from whatever was used to
  define the regions. See `references/resolution-and-scaling.md`.
- **Require confidence thresholds.** No recognition result reaches
  `ObservableState` (or anything downstream) without clearing an
  explicit confidence threshold — see `references/confidence-and-smoothing.md`
  for how thresholds should be set per recognition target and how
  temporal smoothing interacts with them.

## Coordinate with dota-fairplay

Every new CV feature — a new recognition target, a new source region —
is exactly the kind of change `dota-fairplay` requires classification
and documentation for (`source`/`availability`/`visibility`/
`fairPlayClassification`/`justification`) before it's considered done.
For CV specifically:
- `fairPlayClassification` should be `VISIBLE_SCREEN` for essentially
  everything this skill covers — if a proposed CV feature seems to need
  a different (less restrictive) classification, that's a strong signal
  something has gone wrong in the design, not a reason to relax the
  classification.
- `visibility` must cite the actual screen element concretely (which
  region, under what condition it's rendered) — "the player can probably
  see this" is not sufficient per `dota-fairplay`'s own guidance.
- A FairPlay test (per `dota-testing`) should assert the CV pipeline
  reports "unavailable," not a stale/substituted value, when the
  relevant region isn't actually visible in the current frame — see
  `references/fairplay-coordination.md` and `dota-testing`'s CV-testing
  guidance for exactly this "unavailable" case.

## Relationship to other skills

- `dota-fairplay` — the classification system CV output must satisfy;
  read together with this skill for any new CV feature, not after the
  fact.
- `dota-architecture` — CV is a sibling observation source to GSI,
  reconciled by the State Merger; "Computer Vision must not contain Dota
  strategy" is that skill's rule, restated and expanded here as "no
  hidden information inference."
- `dota-gsi` — the parallel observation pipeline; CV and GSI don't
  depend on each other, but both feed the same State Merger and both
  produce `MatchState`-bound observations.
- `dota-testing` — CV test requirements (known-capture test library,
  explicit "unavailable" case testing) are defined there; this skill
  defines what correct CV behavior *is*, `dota-testing` defines how it's
  verified.
