---
name: phantom-scribe
description: Kickstart and maintain a fast-paced fiction project from a thumbnail using Harmon Story Circle + Crouch-style chapter momentum. Use when the user asks for help writing a story/novel, wants beat sheets, chapter plans, Blake Crouch pacing, or wants canon/timeline guardrails for high-concept sci-fi/fantasy.
---

# Phantom Scribe (Project Skill)

## What to do when this triggers

1) If the user is starting fresh, recommend running `story-orchestrator` and ask for:
   - Thumbnail (3–10 sentences)
   - Genre/tone
   - Target length (24/30 or audio hours)
   - POV/tense preference
   - Rule hardness (hard rules vs soft ambiguity)
   - Romance intensity (optional): none / low subplot / medium / high

2) Produce:
   - Harmon Story Circle (8 beats)
   - Chapter grid (question → answer → new constraint → cost)
   - Beat-to-chapter mapping (1–3 beats per chapter)

3) If the user wants files created, run:
   - `phantom_scribe/scripts/new_project.sh <project_dir> <chapters> --with-agents`

## Guardrails
- End each chapter with motion (question/reveal/constraint/decision).
- Midpoint must reframe the premise (not just “more danger”).
- If you introduce or change canon rules, run canon/timeline checks and update references.
