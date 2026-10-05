---
name: develop-story
description: Develop a story idea, weak premise, outline, or draft into a structured foundation with premise options, story core, ending direction, protagonist engine, world pressure, causal beats, scene briefs, and prioritized revision. Use before adapting a general story into comics, film, short drama, or prose; do not use for final screenplay formatting, complete novel prose by default, film storyboards, comic-page planning, or media generation.
---
# Develop Story

## Catalog

- Display name: Develop Story
- Text category: yes
- Categories: Text
- Status: Ready
- Route label: Agent-authored story development package
- Tone: blue
- Short description: Build or repair a story foundation before medium-specific production.

- Similar skills: plan-comic-storyboard, render-comic-page, plan-film-storyboard
## What this skill does

- Diagnoses whether the current need is foundation, story-relevant world pressure, causal beats, scenes, or structural revision.
- Builds a protagonist whose want, need, false belief, history, pressure, choices, and stakes drive the plot.
- Produces stage outputs that can hand off cleanly to prose, short drama, comics, or film planning.

## How to use

Provide the idea or draft, audience, genre, target medium/length, fixed facts, desired emotional effect, ending constraints, and whether you want development only or selected scene drafts.

#### Example

```text
Develop this sci-fi premise for a feature: a climate archivist discovers tomorrow's weather records are being rewritten. Give me three premise directions, select the strongest, then build the protagonist, ending direction, causal beats, and scene briefs.
```

## Workflow

1. Diagnose what already exists: premise, story core, ending, protagonist, world rules, causal beats, scenes, and draft. Preserve fixed facts and label proposed changes.
2. When the foundation is missing, offer three genuinely different premise seeds with audience hook, contradiction, conflict engine, stakes, and ending potential. Select one only when the user has delegated that choice; otherwise pause for selection.
3. Lock the story core and ending direction early: underlying tension, audience promise, climax test, final choice/cost, and earned emotional resolution.
4. Build the protagonist engine: conscious want, deeper need, false belief, formative wound/history, action spine, comfort pattern, opposing pressure, personal/external stakes, and capacity for consequential choice.
5. Add only world details that create pressure, choices, consequences, conflict, values, or risk. Reject lore that never affects character or plot.
6. Create a causal beat chain using therefore/but logic. Each beat must arise from prior action, change the situation, intensify cost, and move toward the climax; eliminate passive drift, repeated functions, coincidence rescues, and “and then” sequences.
7. When scenes are requested, give each an objective, opposition, tactic, turn, outcome, new pressure, and handoff. Draft prose only to the requested depth.
8. For revision, diagnose in order: story core/ending, protagonist, causality/structure, scenes, then dialogue and sentences. Repair the highest-level defect first and report downstream effects.

This Atom performs no paid generation. Hand its accepted package to `write-short-drama-series`, `plan-comic-storyboard`, or `plan-film-storyboard` for medium-specific production.


## User-facing output

- Media type: Structured story-development text package
- Default quantity: One package at the requested development stage
- Content per artifact: Diagnosis, decisions, core, ending, protagonist, world pressure, causal beats, scene briefs, and revision priorities
- Default layout: Concise Markdown or JSON with stable beat/scene IDs
- Model policy: Agent-authored; no paid media generation
- Downstream use: Prose drafting, short drama, comics, film storyboards, and adaptation
