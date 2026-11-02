---
name: audio-mix-loudness-budget
description: Review game audio mix levels, bus headroom, dynamic range, and priority rules so critical feedback stays audible without clipping.
---

# audio mix loudness budget

## Goal

Keep dialogue, gameplay cues, ambience, and music intelligible across scenes, devices, and accessibility settings.

## Inputs to inspect

Audio buses, loudness/peak captures, dynamic range/compression settings, priority rules, sample assets, and target playback contexts.

## Workflow

1. Inventory buses and classify sounds by communication priority, repetition rate, intended distance, and whether the player must react to them.
2. Capture representative mixes for quiet exploration, combat, dialogue, overlapping effects, pause/menu, and low-volume playback using consistent measurement settings.
3. Check peak headroom, clipping, bus gain staging, compression/ducking recovery, and whether multiple layers accumulate into an excessive transient.
4. Test priority/voice limiting so critical gameplay cues are not evicted by ambience or repeated cosmetic sounds; inspect subtitle/caption behavior where relevant.
5. Compare default and accessibility mix options using speakers/headphones and document platform or measurement-tool limitations.

## Validation checklist

- [ ] Master/bus headroom is measured and not based only on subjective listening.
- [ ] Critical cues remain perceptible during dense mixes and do not become dangerously startling by default.
- [ ] Ducking and compression recover smoothly rather than pumping or masking dialogue.
- [ ] Voice limits preserve high-priority cues with predictable behavior.
- [ ] Loudness measurement settings and target contexts are recorded for repeatability.

## Required output

Deliver bus/gain observations, clipping and masking defects, priority-rule recommendations, sample-scene measurements, and a repeatable mix test plan.

## Boundaries and failure handling

Do not prescribe one absolute loudness number without the game's delivery target; do not use excessive master compression as a substitute for balanced source levels.

When repository evidence is incomplete, label the gap explicitly and request only the missing information that changes the decision. Do not claim commands, benchmarks, tests, or runtime checks passed unless their outputs were observed.
