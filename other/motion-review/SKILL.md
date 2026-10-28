---
name: motion-review
description: "Use when judging a rendered film (draft or master) from its frames alone — review pack (ffprobe, stills at 0.0/0.5/1.5 s/mid/last, one still per cut, area-weighted OKLCH planes per still, opacity-blend and drift detection, motion energy, cuts, gesture-free runs and gesture onsets per second, genre + look.md copies), hard-fails checked first (Flat F1-F11 incl. value contrast, display type, centered composition, type scale, mid-tone, full bleed, gesture-free span > 0.75 s, under-animated < 1 onset/s; Motion M1-M3 crossfade/drift/zoom yo-yo; Decorative effect D1-D9 incl. decorative blur, bouncy overshoot, ambient or unproven 3D; Legibility L1-L4; Slop X1-X4; Safety S1-S6), 9-criterion rubric (hook, one idea, motion behaviours, tempo grid, CTA hold, accent, phone legibility, sound-off, look.md consistency) with 1/5/10 anchors, symptom → cause table, and the fixed PASS/REVISE/FAIL/UNCERTAIN verdict."
versions:
  fuse-motion: "1.1.0"
  ffmpeg: "9.0.2"
user-invocable: true
references: references/review-pack.md, references/hard-fails.md, references/hard-fails-example.md, references/rubric.md, references/symptom-cause.md, references/verdict-format.md, references/templates/review-pack-script.md
related-skills: motion-art-direction, motion-method, motion-craft, motion-render, motion-assets, fuse-design:design-review
---

<objective>
The judging half of the fuse-motion pipeline. `motion-critic` uses it on every draft
(before owner gate G2) and on the master (before the "done" claim). The critic sees what
a stranger scrolling a feed would see: frames. It never sees the brief's message or the scene
source. The only non-frame inputs are the `genre:` line of the brief and the locked look
(`look.md`, `refs.md`, `board.png` from `motion-art-direction`), copied into the pack.

Richness comes from value contrast, type as a large object, composition and rhythm. Flatness is a
**hard-fail**, not a low score. A lone paper plane with small objects, display type under 180 px,
a TYPE_SCALE under 4, a centered hero, mid-tone fills, too few full-bleed fields, a span over
0.75 s with no gesture (final CTA still over 1.2 s), fewer than 1 gesture onset per second, a
drift and a crossfade each fail the film. So does any decorative effect, with no exception
(the bounded swap blur, master motion blur, ≤ 3 % overshoot and purposeful 3D are not effects). Hard-fails
come first, then 9 scored criteria. PASS = no hard-fail, every scored criterion ≥ 7 and a mean ≥ 8.0.
ffmpeg missing → UNCERTAIN. One pass only.
</objective>

# Motion Review

## Agent Workflow (MANDATORY)

1. **Builder** runs `bash .motion/review-pack.sh <video>` (template below) and hands the
   critic only: video path, `.motion/review/`, byte budget, expected pix_fmt.
2. **Critic** reads `ffprobe.json` first; ffprobe/ffmpeg missing → **UNCERTAIN**, stop.
   Then `genre.txt` (missing → `assumed ad`).
3. **Restate** the message in one sentence from the frames — before opening the rubric.
4. **Hard-fails first** ([hard-fails.md](references/hard-fails.md)): confirm or reject each
   `flags.txt` candidate on frames with the critic-safe checks
   ([review-pack.md](references/review-pack.md)). Check every F, M, D, L, X (by genre) and S row.
5. **Read the look** (`look.md`, `refs.md`, `board.png` in the pack), then **score** the
   9 criteria ([rubric.md](references/rubric.md)); map weak scores via
   [symptom-cause.md](references/symptom-cause.md).
6. **Emit** the block in [verdict-format.md](references/verdict-format.md) — hard-fails
   listed first. Stop.

---

## Overview

| Step | Input | Output | Reference |
|------|-------|--------|-----------|
| Pack | video + `.motion/brief.md` (genre line), `look.md`, `refs/` | facts, stills, beats, planes, mix, drift, energy, cuts, freezes, flags, copies | [review-pack.md](references/review-pack.md) |
| Gate | pack | F / M / D / L / X / S list | [hard-fails.md](references/hard-fails.md) |
| Score | pack + look copies | 9 scores 1-10 with frame refs | [rubric.md](references/rubric.md) |
| Diagnose | scores < 7, hard-fails | symptom → cause → fix rows | [symptom-cause.md](references/symptom-cause.md) |
| Decide | all of the above | one verdict block | [verdict-format.md](references/verdict-format.md) |

---

## Critical Rules

1. **Intake = the pack** — frames, pack text files, `genre.txt` and the look copies. Never
   the brief's body, beat map, facts, scene code or builder notes; a leak is discarded and
   reported as `intake_leak: yes`.
2. **Message before rubric** — no one-sentence restatement → FAIL.
3. **Hard-fails decide first** — any F, M, D, L, X (ad) or S row → FAIL whatever the mean.
4. **Flatness and decoration are never scored** — F2-F10 and D1-D9 are hard-fails even when
   look.md asks for them; floors equal the look.md dials, in px at 1080 wide and OKLCH L.
5. **Evidence per score** — every score and finding cites a timestamp or pack image.
6. **PASS is strict** — no hard-fail, every scored criterion ≥ 7, mean ≥ 8.0; never rounded up.
7. **One pass, no code** — name symptom, cause and fix direction; the builder fixes.

---

## Architecture

```
.motion/
├── brief.md                            ← motion-method (only its genre: line reaches the pack)
├── look.md  refs/{board.png,refs.md}   ← motion-art-direction (locked before scene code)
├── review-pack.sh + review-pack-lib.sh ← review-pack-script.md (builder runs it)
├── out/draft.mp4 | master.mp4
└── review/                             (generated, gitignore)
    ├── ffprobe.json  genre.txt         facts — read first
    ├── still-0.0|0.5|1.5|mid|last.png  hook window, middle, end card
    ├── beat-NN.png                     one still per state between cuts
    ├── contact.png  strip-01..12.png  strip.png  phone-390.png
    ├── planes.txt                      per still: planes, vc, field, mid, cx, bleed (F2 F4 F7 F9 F10)
    ├── mix.txt  drift.txt              opacity blends (M1, F1); sub-threshold motion (M2)
    ├── diff.txt  spikes.txt  spread.txt  energy.txt   motion energy, jumps, luma spread
    ├── cuts.txt  segments.txt          cut timestamps; state durations (tempo, holds, CTA)
    ├── stats.txt  freeze.txt  flags.txt  raw metadata; ≥ 0.75 s gesture-free runs; hard-fail candidates
    ├── gestures.txt                    gesture onsets + rate per second (F11)
    ├── look.md  refs.md  board.png     copies the sandboxed critic may read
    └── frames.txt                      image → frame → timestamp
```

→ See [review-pack-script.md](references/templates/review-pack-script.md) for the complete script

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Review pack** | [review-pack.md](references/review-pack.md) | Reading the pack; critic sandbox; critic-safe checks (mosaic, halves, psnr, band) |
| **Hard-fails** | [hard-fails.md](references/hard-fails.md) | Every pass, before scoring — the only place IDs are defined |
| **Worked example** | [hard-fails-example.md](references/hard-fails-example.md) | Calibrating on the rejected flat ad, before and after a cosmetic patch |
| **Rubric** | [rubric.md](references/rubric.md) | Scoring — after the restatement; genre rules; audio |
| **Symptom → cause** | [symptom-cause.md](references/symptom-cause.md) | Every score < 7 and every hard-fail |
| **Verdict format** | [verdict-format.md](references/verdict-format.md) | Writing the output |

### Templates

| Template | When to Use |
|----------|-------------|
| [review-pack-script.md](references/templates/review-pack-script.md) | `.motion/review-pack.sh` — builder runs it on draft and master |

---

## Best Practices

### DO
- Read `ffprobe.json`, `genre.txt`, then `flags.txt`, before any image
- Judge the hook on `still-0.0`, `still-0.5`, `still-1.5`; judge each state on its `beat-NN`
- Cite the dial (`VALUE_CONTRAST`, `TYPE_SCALE`, display 180 px, `HOLD`) on every F line
- Confirm F2/F9/F10 on a mosaic, F7 on the halves, F6/M2 with `psnr`, F3/F8/L2 with band tests
- Keep the findings table between rounds so a repeated row is visible

### DON'T
- Pass a white-ground film with small centered blocks because its lightest-to-darkest spread is high: F2 weighs areas
- Credit any gradient background, decorative blur, glow, shadow, grain, glass/chrome, ambient 3D, particle or bouncy overshoot — it is a D fail
- Fail 3D for being 3D: only decorative/ambient 3D, a banned material/effect, or unproven lit determinism is D7
- Accept a film that is readable but under-animated — F6 / F11
- Accept a fade-up, a crossfade or a slow camera push as "motion" — M1 / M2
- Trust a `flags.txt` number without the frames, or dismiss a flat film the flags missed
- Soften a verdict on request or run a second pass on the same file
