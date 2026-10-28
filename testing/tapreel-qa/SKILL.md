---
name: tapreel-qa
description: Quality rules for Tapreel narration and film. Use when judging, re-rendering or fixing voice audio, captions or timing.
---

# Tapreel audio QA rules (learned the hard way)

1. Never time-stretch narration. Choose between takes instead; stretching makes the pace wander.
2. Never cut audio to remove noise. Cutting at dips clips soft word endings ("address", "instantly", "photos"). Reject the take.
3. The voice engine can add breaths: a separate, hissy burst of 0.1-0.4 s before the first word or after the last, well below speech level. Engine settings do not remove it. Detect it and reject the take.
4. Reject takes whose first word is stalled or preceded by sound, and takes whose last 50 ms are still loud.
5. Freeze sentence lengths (`slots.json`) so re-narrating never moves recorded footage.
6. Check with a transcript match against the script, and normalise loudness to -16 LUFS.
7. The assistant cannot listen. Always tell the user which timestamps to spot-check.
8. Recording on a real account: snapshot data first and restore it after. Never leave test rows behind.
