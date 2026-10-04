---
name: issac-story-engine
description: "Write and revise scenes, chapters, and full novels in Issac's style using research-backed craft, canon-aware worldbuilding, and a balanced technical-plus-human narrative voice. Use when drafting fiction, sharpening scenes, adding interludes, preserving tone, or turning research and lore into readable prose."
---

# Issac Story Engine

Use this skill when the user wants fiction written or revised in Issac's style, especially for Aethermoor, Pollyoneth, Spiralverse, or related projects where wonder, humor, emotional clarity, and technical structure must coexist.

## What This Skill Owns

- scene drafting
- chapter drafting
- interlude writing
- novel and arc architecture
- voice preservation during revision
- worldbuilding insertion without lore-dump drag
- technical-to-mythic translation for system-heavy fantasy

## When To Use It

Trigger this skill for requests like:

- "write this scene"
- "turn these notes into a chapter"
- "make the novel feel more lived in"
- "add interludes"
- "keep the magic technical but fun"
- "preserve Issac's voice"
- "use research-backed writing practices"

Do not use this skill for pure coding tasks, pure copyediting with no narrative judgment, or factual research that should stay outside the fiction lane until the user asks for prose.

## Core Workflow

1. Lock the unit of work.
- Determine whether the request is a scene, chapter, interlude, outline, or full-novel problem.
- Identify POV, desired change, emotional target, and output length.

2. Gather only the canon that matters.
- For Aethermoor or Pollyoneth work, load `aethermoor-lore` first.
- For current SCBE book work, prefer the live manuscript and project notes over older archive branches.
- If the request depends on evidence or research claims, use the research lane before drafting.

3. Build a writing packet.
- Use the 5 Ws for structure.
- Add the 7-sense layer for atmosphere and meaning.
- Define one emotional beat, one technical beat, one world detail, and one warmth or humor beat.

4. Draft the minimum correct prose.
- Start with the cleanest version that satisfies the brief.
- Keep exposition pressure low.
- Let character, motion, and setting carry the information load.

5. Run the revision loop.
- Voice pass
- Clarity pass
- Structure pass
- Sensory pass
- Compression pass

6. Mirror useful notes.
- If the user is actively using Obsidian or project notes, leave a compact drafting artifact or canon note instead of burying decisions in chat.

## Style Rules

- Lead with human truth before system explanation.
- Let characters be funny, irritated, tender, wrong, and alive.
- Keep the prose readable even when the idea is technical.
- Treat magic as lived reality for natives.
- Let outsider or systems-minded characters notice structure without flattening the world.
- Prefer precise lines over swollen paragraphs.
- End major arcs on durable emotional truth, not abstract cosmology alone.

## Issac Voice Baseline

- witty
- poetic without trying too hard
- irreverent in pressure moments
- casually philosophical
- emotionally sincere
- technical when useful, not performative

If the work starts sounding generic, over-luxurious, or like a design document, pull it back toward voice, scene, and people.

## Writing Modes

### Scene Mode

Use when a single interaction, reveal, conflict, or emotional turn must land cleanly.

Read:
- `references/scene-packet.md`
- `references/issac-style.md`

### Chapter Mode

Use when the task needs pacing, chapter shape, interludes, and end-beat control.

Read:
- `references/chapter-and-interlude.md`
- `references/scene-packet.md`

### Novel Mode

Use when the user is planning long arcs, balancing cast density, or repairing structural drift.

Read:
- `references/novel-architecture.md`
- `references/chapter-and-interlude.md`

### Research-Backed Mode

Use when the user explicitly asks for research-backed practice, evidence, or theory support.

Read:
- `references/research-lane.md`

If the request is about Aethermoor or related canon, also load `aethermoor-lore`.

## Support Skill Routing

Use these support skills deliberately:

- `aethermoor-lore`
  Use for canon, characters, locations, magic systems, and continuity framing.

- `aetherbrowser-arxiv-nav`
  Use when the user explicitly wants research-backed methods or current paper evidence. Prefer abstracts, titles, authors, dates, and concise takeaways.

- `development-flow-loop`
  Use the same loop for writing work:
  Plan -> Architect -> Evaluate -> Implement -> Test -> Fix -> Test -> Improve -> Test -> Deliver.

- `skill-synthesis`
  Use when the task spans lore, research, writing, notes, and deployment artifacts in one pass.

- `scbe-claude-crosstalk-workflow`
  Use only when Codex and Claude are both active and need deterministic handoff packets.

## Project-Specific Rule For The Six Tongues Protocol

When writing `The Six Tongues Protocol`:

- the book remains Marcus's isekai
- the world remains real to its natives
- Marcus may internally translate some structures into systems language
- Clay remains a foundational moral proof
- Everweave history should deepen the world, not replace the current story

For that project, also use the Obsidian notes in:

`C:\Users\issda\Documents\Avalon Files\SCBE Research\Writing\The Six Tongues Protocol`

## Deliverable Standard

A good output from this skill should usually contain:

- clear scene or chapter movement
- character voice separation
- sensory grounding
- at least one memorable line
- technical clarity where relevant
- no unnecessary lore bloat

## Resources

- `references/issac-style.md`
  Voice, theme, and hard canon tendencies.

- `references/scene-packet.md`
  Build scenes from structure, senses, and change.

- `references/chapter-and-interlude.md`
  Chapter pacing, interlude logic, and end-beat design.

- `references/novel-architecture.md`
  Long-form planning and repair guidance.

- `references/research-lane.md`
  How to use research without drowning the prose.
