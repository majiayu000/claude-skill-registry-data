---
name: motion-method
description: "Use when starting or resuming any motion film (launch video, product promo, social ad, README GIF, social loop) — locks the six-block brief (inputs, direction, structure, build, gotchas, start = G0; genre ad|demo), builds the dense beat map (a gesture every 0.5-1 s, ≤ 0.75 s gesture-free, CTA still ≤ 1.2 s), routes the G0 art-direction board, and runs the staged pipeline (one still per beat) with its owner gates."
versions:
  fuse-motion: "1.0.0"
user-invocable: true
references: references/brief-lock.md, references/ad-genre.md, references/reference-styles.md, references/beat-map.md, references/stage-gates.md, references/exit-contract.md, references/templates/brief.md, references/templates/beats.md
related-skills: motion-art-direction, motion-craft, motion-assets, motion-render, motion-review, fuse-design:design-motion
---

<objective>
The pipeline owner for every fuse-motion film. It turns a request ("make a 15 s launch video") into a locked brief at `.motion/brief.md` with `genre: ad | demo`, a timed beat map whose beats sum to the film's DURATION, an owner-approved art direction (G0: `.motion/refs/board.png` + `.motion/look.md`), and a staged render path — stills, draft, master — with an owner gate between each stage.

The other skills point here for order and gates: `motion-art-direction` locks the visual system before any scene code, `motion-craft` decides how each beat looks and moves, `motion-assets` supplies the real screenshots, `motion-render` produces the frames and files, `motion-review` judges them. This skill decides WHEN each of them runs and WHEN to stop.

Gates G1 (stills → draft) and G2 (draft → master) are owner approvals. They are enforced by the harness `motion` scope (`hooks/hooks.json`) and specified in `references/stage-gates.md`: draft and master renders are denied until the owner types `MOTION-APPROVE stills|draft <code>`. The agent still stops at each gate on its own. G0 (board + `look.md`, before scene code) is an owner step, not a harness gate: the agent stops and waits, never self-approves.
</objective>

# Motion Method

## Agent Workflow (MANDATORY)

| Step | Who | What |
|------|-----|------|
| Before the brief | `fuse-ai-pilot:explore-codebase` | Find the product's real tokens, screens, copy, existing `.motion/` state |
| Named style unknown | `fuse-ai-pilot:research-expert` | Verify what the named reference style actually looks like (no guessing) |
| G0 tone | `fuse-ai-pilot:challenger` | Blind-locks one of 3 text tone sketches (`motion-art-direction`) |
| Draft rendered | `motion-critic` | One review pass per round via `motion-review`; at most 2 fix rounds |
| Scripts written | `fuse-ai-pilot:sniper` | Validate scene/render scripts (code only) |
| Before "done" | `fuse-ai-pilot:challenger` | Challenge the "master verified" claim |

---

## Overview

| Stage | Output | Stop? |
|-------|--------|-------|
| 1 Brief lock | `.motion/brief.md` — `genre: ad` or `demo`, `<inputs>` (with defaults), `<direction>`, `<structure>`, `<build>`, `<gotchas>`, `<start>` | Ask ONE question if an input has no default; `genre: ad` → owner confirms the message |
| 2 Beat map | `.motion/beats.md` — one row per beat (0.5-1 s), its primary gesture, details, words, 3D reason; DURATION = sum of beats; ≤ 0.75 s gesture-free, CTA still ≤ 1.2 s, ≥ 1 beat change/s; key action on the drop | — |
| 2b G0 art direction | brief → 3 text sketches (tone candidates) → `fuse-ai-pilot:challenger` locks the tone blind → reference board → `.motion/look.md` (dials) + 3 key frames → owner sees the key frames → scene code (`motion-art-direction`) | **STOP — G0**, owner approves; never self-approve |
| 3 Assets | real screenshots + `.motion/assets.json` (see `motion-assets`) | — |
| 4 Scene | Built from the `motion-art-direction` templates first — cut-rhythm, composition-grid, kinetic-type, objects.md — then `motion-render` for seek/capture/encode only (`window.seek(t)` / DURATION / FPS, `?t=` and `?capture`) | — |
| 5 `--stage stills` (default) | one still per beat + contact sheet | **STOP — G1** |
| 6 `--stage draft` (540p) | draft mp4 → `motion-critic` (≤2 fix rounds) | **STOP — G2** |
| 7 `--stage master` | master file, verified with ffprobe + frame diff vs approved stills | — |
| 8 Validate | sniper on scripts, challenger on the "done" claim | — |

---

## Critical Rules

1. **No code before the brief is locked** — every section filled, or defaulted and marked "default — owner skipped". One question at a time. Shape from field template (ultimaxbt, 2026-10-07). For `genre: ad` the agent never self-locks: the owner confirms the message.
2. **No scene code before G0** — pipeline: brief (genre ad|demo; owner confirms an ad's message) → beats (on a tempo grid) → **G0**, in this exact order: brief → 3 text sketches (tone candidates) → challenger locks the tone blind → reference board → `look.md` (dials) + 3 key frames → owner sees the key frames → scene code. Then stills (G1) → draft + critic (G2) → master. No `.motion/scene/*` file is written before `look.md` and the key frames exist; never self-approve G0. This is a prose rule — the harness does not enforce G0 yet. `genre: ad` also applies [ad-genre.md](references/ad-genre.md).
3. **A named reference style, never an adjective** — "Linear launch", not "premium/modern". See [reference-styles.md](references/reference-styles.md).
4. **Facts on screen come from a facts file only** — no invented feature, metric, or UI state.
5. **DURATION = sum of beats** — the scene's DURATION constant is derived from `beats.md`, never typed separately.
6. **Omitted `--stage` means `stills`** — the pipeline never jumps to draft or master by default.
7. **Stop at G1 and G2, never lean on the deny** — the harness enforces both; the owner approves by typing `MOTION-APPROVE`, never the agent. `.motion/project.json` is owner-managed: if missing before the first draft, STOP and give the owner its content (see [stage-gates.md](references/stage-gates.md)).
8. **Continuous purposeful motion, readable, never drifting** — a gesture in progress at every moment: no span > 0.75 s without one, the final CTA still ≤ 1.2 s, a beat change every 0.5-1 s (≥ 1 per second); ≥ 0.25 s per word on screen; long copy split into more beats — never kept alive by a drift (`motion-craft` → timing-holds).
9. **The scene step routes through `motion-art-direction` templates first** — composition-grid, kinetic-type, cut-rhythm; `motion-render` supplies only seek/capture/encode. Frame 0 shows the opening statement at full value; no opacity blends, no centered hero, entrances rotate (`motion-craft`).
10. **Verify the file, not the intent** — the master is done when ffprobe and the frame diff say so, not when the render command exits 0.
11. **Every decorative effect is banned** — gradient backgrounds, decorative blur, glow, shadow, grain, glass/chrome, ambient 3D, particles, bouncy easing; no exception via `look.md`; the list and its four bounded allowances (swap blur, master motion blur, ≤ 3 % overshoot, purposeful 3D) live in `motion-craft` → anti-slop-video.
12. **Not only type** — one recurring geometric actor and animated objects move with the words; 3D where the expert judges it serves, justified in look.md and the beat map (`motion-art-direction` → objects.md).

---

## Architecture

```
<project>/.motion/
├── brief.md          # Stage 1 — locked brief (template: brief.md)
├── facts.md          # Only source for on-screen claims
├── beats.md          # Stage 2 — beat map (template: beats.md)
├── look.md           # G0 — locked visual system (motion-art-direction)
├── refs/             # G0 — board.png + refs.md, owner-approved before scene code
├── assets.json       # Stage 3 — provenance (motion-assets)
├── scene/            # Stage 4 — index.html + timeline.js (window.seek(t))
├── stills/           # Stage 5 — still-1..N.png (one per beat) + contact.png (G1 artifact)
├── out/              # Stage 6-7 — draft.mp4 (G2 artifact), master.mp4 + master.gif
└── review/           # Review pack of the draft/master (motion-review), gitignored
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Brief lock** | [brief-lock.md](references/brief-lock.md) | Stage 1 — the six blocks of the prompt-motion prompts mapped to our gates (`<start>` = G0), defaults, one still per beat, one-question rule |
| **Ad genre** | [ad-genre.md](references/ad-genre.md) | `genre: ad` — hook (0-3 s, the pain in their words) → pain → solution → ONE CTA, 2-6 words per hero beat, tempo grid, sound-off, durations |
| **Reference styles** | [reference-styles.md](references/reference-styles.md) | Turning "make it premium" into a named, checkable style |
| **Beat map** | [beat-map.md](references/beat-map.md) | Stage 2 — timing every beat, deriving DURATION |
| **Stage gates** | [stage-gates.md](references/stage-gates.md) | G1/G2 enforcement, `project.json` contract, `MOTION-APPROVE` flow, deny messages, budget cap |
| **Exit contract** | [exit-contract.md](references/exit-contract.md) | Deciding Stop / Retry / Rollback / Ask / Escalate on a motion event |

### Templates

| Template | When to Use |
|----------|-------------|
| [brief.md](references/templates/brief.md) | Writing `.motion/brief.md` |
| [beats.md](references/templates/beats.md) | Writing `.motion/beats.md` |

### Sibling skills

| Skill | Owns |
|-------|------|
| `motion-art-direction` | G0: tone sketches, references board, `.motion/look.md` (dials) + key frames; the scene templates (composition-grid, kinetic-type, cut-rhythm) |
| `motion-craft` | Focus, holds, easing/springs, color/type, anti-slop rules |
| `motion-assets` | Real screenshots, masking, provenance |
| `motion-render` | Seek/capture/encode mechanics, determinism, stage flags — not the look of a scene |
| `motion-review` | Review pack, rubric, verdict |
| `fuse-design:design-motion` | UI motion tokens — pointed to, never copied |

---

## Best Practices

### DO
- Re-read `.motion/` on resume: an existing brief, beat map, or approval decides where the pipeline restarts.
- Show the contact sheet at G1 and the draft at G2 with the `MOTION-APPROVE <stage> <code>` line the owner must type (code from the deny message).
- Report renders per stage and wall time at every stop (see [exit-contract.md](references/exit-contract.md)).
- Keep one owner decision per question; record each answer in the brief.

### DON'T
- Start the scene before the beat map sums correctly, or before `look.md` + the 3 key frames exist and the owner approved G0.
- Start a scene from a centered starter skeleton or a generic fade helper — start from the `motion-art-direction` templates.
- Self-lock an ad brief or self-approve the G0 board.
- Render a draft "just to see" before G1, or a master before G2.
- Treat an approval as valid after the artifact changed — a new hash needs a new approval.
- Write client names or real spend figures into any `.motion/` file.
