---
name: task-research
description: "Research a task before building: codebase prior art first, then docs and web, separating facts from assumptions, ending in a short findings brief that feeds a plan or ticket. Use for research, investigate, look into, find out how, what's the best way, compare approaches, spikes, or feasibility checks."
license: MIT
metadata:
  display-name: "Task Research"
  version: "1.1"
  platforms: "claude-code codex"
  tags: "research planning discovery"
---

# Task research

You are reducing uncertainty *before* code is written or a plan is drafted. Research is cheap now and expensive later - an hour here saves a day of building the wrong thing. Timebox it and produce a brief, not an essay.

## Rule 0 - search the codebase before the web

Most "how do I build X" questions are already answered inside this repo.

- Grep for existing utilities, patterns, and near-duplicates of what you're about to add. Reuse beats new code.
- Find the *convention*: how does this codebase already do the adjacent thing? Match it.
- Cite what you find as `path:line`. A claim without a location is a guess.
- Only reach for external sources once you've confirmed the answer isn't already here.

## External research

- **Triage sources by trust:** official docs and the library's own repo/issues > maintained examples > recent blog posts > forum answers. A 2019 Stack Overflow answer about a fast-moving library is probably wrong now.
- **Check version and date.** Pin every claim to the version it applies to. APIs drift; "the top Google result" is often two majors behind.
- **Corroborate load-bearing claims.** If a decision hinges on it, find a second independent source. For a deep, fully-cited investigation, hand off to the `deep-research` skill instead.

## Separate facts from assumptions

- Label every statement: **fact** (verified, with a source/location) vs **assumption** (plausible, unverified).
- Make unknowns explicit. "I don't know whether the API supports batching" is more useful than a confident wrong guess.
- Never launder an assumption into the plan as if it were a fact. That's how plans fail in week two.

## Output - the research brief

Keep it short and skimmable. Structure:

1. **Question** - what you set out to answer, in one line.
2. **What already exists** - prior art in this repo (`path:line`) and reusable pieces.
3. **Options** - 2 - 3 viable approaches, each with its real trade-off (not a strawman).
4. **Recommendation** - the one you'd pick, and why, in a sentence or two.
5. **Open questions / risks** - what's still unverified and what would change the answer.
6. **Sources** - links/paths, with versions/dates.

This brief is an *input* to a ticket or the Plan flow - it doesn't propose diffs.

## Scope discipline

- Timebox. When you can answer the Question and name the risks, stop.
- Don't boil the ocean: research the decision in front of you, not the whole domain.
- If the answer is "just read this one file," say that and stop - don't manufacture options.

## What this skill is *not*

- Not implementation - it precedes it.
- Not a full cited report - that's `deep-research`.
- Not architecture evaluation of existing code - that's `architect-review`.
