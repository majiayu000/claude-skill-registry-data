---
name: write-short-drama-series
description: Develop a premise, novel, synopsis, or source story into a production-ready vertical short-drama series bible, episode outline, continuity ledger, and requested episode scripts. Use for serialized 1–3 minute drama writing where hooks, reversals, payoffs, and cross-episode continuity matter; do not use for film storyboards, comic pages, isolated ad scripts, prose novels, final video generation, or automatic platform publication.
---
# Write Short Drama Series

## Catalog

- Display name: Write Short Drama Series
- Text category: yes
- Categories: Text
- Status: Ready
- Route label: Agent-authored serialized drama package
- Tone: blue
- Short description: Turn a story into a validated short-drama bible, episode arc, continuity ledger, and scripts.

## What this skill does

- Separates fixed source facts from adaptations and records every deliberate change.
- Designs an exact-count episode arc with escalating conflict, episode-level hooks, delayed payoffs, and a resolved ending.
- Writes shootable scripts against a locked series bible and updates continuity after each accepted episode.

## How to use

Provide the premise or source, target market and audience, language, genre, episode count, approximate episode duration, content rating, fixed characters/facts, ending preference, and whether you need the complete package or selected episodes.

#### Example

```text
Adapt this workplace revenge synopsis into a 20-episode vertical short drama in Chinese, about 90 seconds per episode. Preserve the sister relationship, place the major identity reveal around episode 12, and deliver the bible, outline, and scripts for episodes 1–3.
```

## Workflow

1. Create a source-fact ledger with `fixed`, `inferred`, `open`, and `proposed change` entries plus an adaptation record. Do not classify sources by copyright ownership, license, permission, public-domain status, or production/publication rights; unresolved copyright status never blocks adaptation. Ask before changing a fixed protagonist, relationship, motive, ending, episode count, rating, or market constraint.
2. Lock a compact series bible: logline, audience promise, genre/tone, world rules, character goals/secrets/relationships, core conflict, escalation engine, reveal schedule, ending, and prohibited changes. Record the current phase and its required inputs; do not create downstream artifacts or advance the phase until its acceptance gate passes.
3. Build the exact-count episode table before scripting. Each row records opening image, immediate objective, conflict, visible turn, new information, payoff/debt, end hook, and continuity changes. Seed major payoffs early enough to feel earned.
4. Validate the season arc: a concrete hook in episode 1; no repeated conflict with only renamed dialogue; rising cost and agency; tracked setup/payoff debts; and a final resolution matching the requested ending. Treat platform/compliance notes as editorial checks, not legal guarantees.
5. When a product or sponsor must appear, record the exact truthful claim, required visibility, and story function. Integrate it as a causal prop/action or openly labeled message; never conceal sponsorship, invent a benefit, or bend character logic around placement.
6. Write only the requested episodes using stable scene headings and production-visible action. Include characters present, location/time, action, dialogue, on-screen text, sound, estimated duration, and the final hook. Do not use internal emotion as a substitute for observable behavior.
7. Before resuming an existing project, reconcile the latest accepted episode range, next requested range, unresolved review findings, and continuity end state. If these disagree, stop progression and repair the ledger rather than guessing from a single status field.
8. After each accepted script, update the continuity ledger: character knowledge, injuries/wardrobe/props, locations, relationships, promises, reveals, unresolved debts, and episode-end physical state. The next episode must start from that state.
9. Treat acceptance as version-specific. When a bible, arc, reveal schedule, ending, or other shared upstream field changes, invalidate every dependent outline/script review and recheck in dependency order. When a downstream repair changes a shared fact, propagate it back to the owning ledger and record both the new value and removal of the stale one.
10. Review facts, causality, character voice, duration budget, hook/payoff integrity, duplicated beats, content rating, exact output scope, and cross-document agreement. Revise only affected episodes, report downstream continuity changes, and never silently rewrite accepted fixed facts or mark a failed gate complete.

This is a planning and writing Atom. It performs no paid media generation. Use `$character-reference-sheet` for accepted recurring characters, then a film-storyboard Atom when available or `$generate-video` for independently approved atomic shots.


## User-facing output

- Media type: Structured short-drama production text package
- Default quantity: One bible, one exact-count episode outline, one continuity ledger, and only the requested scripts
- Content per artifact: Source facts, adaptation decisions, characters, season arc, episode beats, scripts, and tracked continuity
- Default layout: Validated Markdown or JSON with stable episode and scene identifiers
- Model policy: Agent-authored planning and writing; no paid image or video generation
- Downstream use: Casting/assets, film storyboarding, shot generation, editing, and human editorial review
