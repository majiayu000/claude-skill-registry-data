---
name: shot-list
description: Turn a scene, synopsis or script excerpt into a practical shot list (shot size, angle, movement, lens, action, duration). Use when the user is planning how to film or storyboard a scene, or asks for coverage, shot breakdowns or a shooting plan.
license: MIT
metadata:
  author: Benjamin Leleu
  version: "1.0.0"
---

# Shot List

Build a shot list a crew could actually shoot from the next morning.

## Before you write anything

Ask for whatever is missing. Do not guess these:

1. **Format**: aspect ratio and delivery (vertical 9:16, 16:9, 2.39:1, etc.)
2. **Tone / references**: genre, mood, any films or looks to evoke
3. **Constraints**: location, number of actors, available gear, time budget, daylight
4. **Scene text**: the scene itself, not just the title

If the user already gave some of these, do not ask again. If they say "just do it", state your assumptions in one line and proceed.

## Process

1. Read the scene and mark its **beats** (setup, turn, reveal, payoff). Each beat should earn at least one shot.
2. Pick a **master / establishing shot** first so geography is clear.
3. Add **coverage** for dialogue and action: singles, overs, inserts, reactions.
4. Vary shot size and movement with intent. A change of size should mean something (tension, intimacy, reveal), never just variety.
5. Flag shots that are expensive or risky (crane, stunt, night exterior, VFX) and offer a cheaper alternative.
6. Estimate durations only as rough screen-time targets, not shooting time.

## Output format

Start with two lines: assumptions made, and the one-sentence visual idea of the scene.

Then a table:

| # | Beat | Size | Angle | Movement | Lens (approx.) | Action / subject | Est. screen time | Notes |
|---|------|------|-------|----------|----------------|------------------|------------------|-------|

- **Size**: ECU, CU, MCU, MS, MWS, WS, EWS
- **Angle**: eye-level, low, high, Dutch, OTS, POV
- **Movement**: static, pan, tilt, dolly in/out, track, handheld, gimbal, crane
- **Lens**: focal length range (e.g. 24-35mm wide, 50mm normal, 85mm+ portrait). Say "approx."; this is guidance, not a spec.

End with:
- **Must-get shots** (the 3 shots without which the scene fails)
- **If time runs out** (what to cut first)
- **Questions** (max 3) only if something genuinely changes the plan

## Rules

- Never invent plot, dialogue or characters. Work only from the scene given.
- Do not pad. A 20-second scene does not need 25 shots.
- Respect the stated aspect ratio: vertical framing changes composition (headroom, lateral space, subtitle safe zones).
- Plain filmmaking vocabulary. No jargon the user did not use first, unless you define it once.
