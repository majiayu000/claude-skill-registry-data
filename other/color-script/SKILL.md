---
name: color-script
description: Build a color script (palette and grade direction per story beat) from a synopsis, scene list or edit. Use when the user wants a color palette for a film, a look-development plan, grade notes for DaVinci Resolve or similar, or emotional color mapping.
license: MIT
metadata:
  author: Benjamin Leleu
  version: "1.0.0"
---

# Color Script

A color script maps **emotion to color across the story**. Produce one that a colorist or editor can apply directly.

## Inputs to collect

Ask only for what is missing:

1. The story or scene list (required), with the emotional arc if known
2. Look references (films, photos, moods) and any colors that must not be used
3. Delivery space: SDR (Rec.709) or HDR, and whether the footage is log or already graded
4. Grading tool (DaVinci Resolve, Premiere Lumetri, After Effects, other)

## Process

1. Identify the **beats** (opening, disruption, escalation, climax, resolution) and the emotion of each.
2. Assign each beat a **dominant color family**, an **accent color**, a **contrast level** (low / medium / high) and a **saturation level**.
3. Keep **continuity logic**: a color that appears early should return, transformed, at the payoff. Name the motif.
4. Translate each beat into **grade direction**: color temperature shift, tint, contrast curve behavior, shadow/highlight color bias, saturation strategy. Use descriptive terms and relative moves, not claims about a specific proprietary LUT.
5. Check **readability**: skin tones must stay believable, subtitles must stay legible against the palette.

## Output format

Start with a one-line **color concept** (the idea in a sentence).

Then a table, one row per beat:

| Beat | Emotion | Dominant | Accent | Contrast | Saturation | Hex swatches (3-5) | Grade direction |
|------|---------|----------|--------|----------|------------|--------------------|-----------------|

- Hex swatches are suggestions for reference boards and UI mocks, not guaranteed to match on-screen skin or footage.
- **Grade direction** examples: "cool the shadows toward teal, keep highlights near neutral, lower mid-tone saturation, firm contrast"; "warm global temperature, lift blacks slightly, gentle roll-off".

Then:

- **Motif**: the color that carries meaning across the film and how it evolves
- **Continuity warnings**: where grades must match across cuts
- **Resolve starter nodes** (only if the user uses DaVinci Resolve): suggested node order such as input conversion, primary balance, look, secondary skin protection, output. Keep it generic.

## Rules

- No invented story. Work from the beats given.
- State when a choice is a taste decision versus a technical necessity.
- Do not promise exact colors: lighting, camera and display all change the result. Recommend testing on a graded still before committing.
