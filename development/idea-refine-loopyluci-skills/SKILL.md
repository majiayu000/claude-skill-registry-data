---
name: idea-refine
description: Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one.
version: 2.0.0
author: LoopyLuci Community
license: MIT
platforms: [any]
metadata:
  hermes:
    tags: [software-development, engineering, agent-skills]
    source: addyosmani/agent-skills
    adapted: true
---

# Idea Refine

> **Adapted for the LoopyLuci Skills collection** from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills). The guidance below is rewritten and condensed for this repo; commands, paths, and reference tables are preserved.

## Trigger

- An idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one

## When NOT to Use

- Don't generate 20+ ideas. Quality over quantity. 5-8 well-considered variations beat 20 shallow ones.
- Don't be a yes-machine. Push back on weak ideas with specificity and kindness.
- Don't skip "who is this for." Every good idea starts with a person and their problem.
- Don't produce a plan without surfacing assumptions. Untested assumptions are the #1 killer of good ideas.
- Don't over-engineer the process. Three phases, each doing one thing well. Resist adding steps.
- Don't just list ideas — tell a story. Each variation should have a reason it exists, not just be a bullet point.
- Don't ignore the codebase. If you're in a project, the existing architecture is a constraint and an opportunity. Use it.
- Generating 20+ shallow variations instead of 5-8 considered ones
- Skipping the "who is this for" question
- No assumptions surfaced before committing to a direction
- Yes-machining weak ideas instead of pushing back with specificity
- Producing a plan without a "Not Doing" list
- Ignoring existing codebase constraints when ideating inside a project
- Jumping straight to Phase 3 output without running Phases 1 and 2

## Overview

Turn a raw idea into a sharp, actionable concept through three phases of structured divergent and convergent thinking, ending in a one-pager worth building.

## The three phases

1. **Understand and expand (divergent).** Restate the idea as a "How Might We" problem, ask sharpening questions, and generate variations.
2. **Evaluate and converge.** Cluster what resonated, stress-test each direction, and surface hidden assumptions.
3. **Sharpen and ship.** Write a concrete markdown one-pager that moves the work forward.

This is a dialogue, not a template — adapt to what the user says.

## Phase 1: understand and expand

Restate the idea as a crisp "How Might We" statement; that forces clarity about what is actually being solved.

Ask 3–5 sharpening questions, no more: who this is for specifically; what success looks like; the real constraints (time, technology, resources); what has been tried before; why now. Do not continue until you know who it is for and what success means.

Generate 5–8 variations through these lenses: inversion ("what if we did the opposite?"); constraint removal ("what if budget, time, or technology were not factors?"); audience shift ("what if this were for a different user?"); combination ("what if we merged this with an adjacent idea?"); simplification ("what is the version that is 10x simpler?"); the 10x version ("what does this look like at massive scale?"); and the expert lens ("what would domain experts find obvious that outsiders would not?"). Push past the initial ask — the goal is options the user did not know they needed.

Inside a codebase, scan with glob, grep, and read for existing architecture, patterns, constraints, and prior art, and ground variations in specific files. `frameworks.md` holds further ideation frameworks — use the lens that fits rather than running every framework mechanically.

## Phase 2: evaluate and converge

Once the user reacts, cluster the resonant ideas into 2–3 genuinely distinct directions. Stress-test each against three criteria: user value (who benefits, how much, painkiller or vitamin); feasibility (technical and resource cost, and the hardest part); differentiation (what makes it different, and whether anyone would switch). `refinement-criteria.md` carries the full rubric.

Then surface hidden assumptions for each direction: what you are betting is true but have not validated; what could kill the idea; what you are choosing to ignore, and why that is acceptable for now. This is where most ideation fails, so do not skip it.

Be honest rather than supportive. A good ideation partner is not a yes-machine: push back on complexity, question real value, and say when the emperor has no clothes.

## Phase 3: sharpen and ship

Produce a one-pager:

```markdown
# [Idea Name]

## Problem Statement
[One-sentence "How Might We" framing]

## Recommended Direction
[The chosen direction and why — at most 2–3 paragraphs]

## Key Assumptions to Validate
- [ ] [Assumption — how to test it]

## MVP Scope
[The smallest version that tests the core assumption: what is in, what is out]

## Not Doing (and Why)
- [Thing] — [reason]

## Open Questions
- [Question that must be answered before building]
```

The "Not Doing" list is the most valuable part: focus means saying no to good ideas, so make the trade-offs explicit. Ask before saving the file (default `docs/ideas/[idea-name].md`); save only on confirmation.

## Anti-patterns

- Generating 20+ ideas — 5–8 considered variations beat 20 shallow ones.
- Yes-machining weak ideas instead of pushing back with specificity and kindness.
- Skipping "who is this for"; every good idea starts with a person and a problem.
- Producing a plan without surfacing assumptions; untested assumptions are the top killer of good ideas.
- Over-engineering the process — three phases, each doing one thing well.
- Listing ideas without a reason each exists; tell a story.
- Ignoring the codebase when ideating inside a project; existing architecture is both a constraint and an opportunity.
- Jumping straight to the Phase 3 artifact without running Phases 1 and 2.

## Tone

Direct, thoughtful, slightly provocative — a sharp thinking partner, not a facilitator reading a script. The register is "that is interesting, but what if…", always pushing one step further without becoming exhausting.

## Verification

- [ ] A clear "How Might We" statement exists.
- [ ] Target user and success criteria are defined.
- [ ] Multiple directions were explored, not just the first idea.
- [ ] Hidden assumptions listed with validation strategies.
- [ ] A "Not Doing" list makes trade-offs explicit.
- [ ] The output is a concrete one-pager, not just conversation.
- [ ] The user confirmed the direction before implementation.

## Related Skills in This Repo

- [code-review-and-quality](../code-review-and-quality/SKILL.md) — Use when reviewing code written by yourself, another agent, or a human; you need to assess...
- [ci-cd-and-automation](../ci-cd-and-automation/SKILL.md) — Use when setting up or modifying build and deployment pipelines; you need to automate qual...
- [api-and-interface-design](../api-and-interface-design/SKILL.md) — Use when designing APIs, module boundaries, or any public interface; creating REST or Grap...
- [git-workflow-and-versioning](../git-workflow-and-versioning/SKILL.md) — Use when making any code change; committing, branching, resolving conflicts, splitting unc...

## Adaptation Notes

- Description rewritten into this repo's trigger form.
- Trigger and When-NOT-to-Use sections derived from the upstream guidance.
- Body condensed and restructured; commands, file paths, and tables preserved.
- Upstream anti-patterns retained as the When-NOT-to-Use list.
- Related skills linked from this repo.
- Upstream branding and attribution lines removed (attribution below).

## Source & Attribution

- Upstream: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)
- Path: `_sources/addyosmani_agent-skills/skills/idea-refine/SKILL.md`
- License: MIT — Copyright (c) 2025 Addy Osmani
- Retrieved: 2026-11-14; rewritten and condensed by LoopyLuci Community.
