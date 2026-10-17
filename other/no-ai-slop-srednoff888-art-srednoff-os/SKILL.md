---
name: no-ai-slop
description: Use this skill to edit prose into clearer, more human writing while preserving the author's voice, or to audit a draft for AI-slop patterns without rewriting it. Use for READMEs, PR descriptions, docs, posts, and emails; do not use for UI or visual critique.
---

# No AI Slop

Use this skill when a draft reads as generic AI output, or when the user asks whether writing sounds like AI.

## Two Modes

1. **Edit (default).** Make the minimum effective change and return the full edited draft plus a short **What changed** list.
2. **Audit.** Name each pattern found, quote the offending line, give the fix in a few words. Do not rewrite, do not score, and never claim a text was AI-written - detectors guess, named patterns are checkable evidence. Offer to edit afterwards.

## Workflow

1. Read the whole draft first. If none was provided, ask for it.
2. Identify the core point and the voice traits worth keeping: vocabulary, cadence, bluntness, humour, admitted uncertainty, digressions.
3. Ask at most one blocking question - who is the reader and where does this publish - then state assumptions and continue.
4. Cut the patterns below, leaving strong human sentences untouched, then re-check against the checklist until it passes.
5. Return the edited draft and the **What changed** list, saying why if you reordered anything.

## Patterns To Cut

- **Empty vocabulary:** delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, paradigm shift, game changer, tapestry, realm, multifaceted, meticulous, transformative, elevate, embark, harness, ever-evolving.
- **Filler openers and closers:** "it's worth noting", "at the end of the day", "in today's world", "let's dive in", "in conclusion", "ultimately", and any final paragraph that recaps what the reader just read.
- **Binary contrasts and negative lists:** "not X, it's Y", "not a X. Not a Y. A Z." State Y or Z directly.
- **Faux insight and puffery:** "what nobody tells you", "marks a pivotal moment", "stands as a testament", colon reveals used for drama, trailing `-ing` clauses that explain the significance instead of the mechanism.
- **Metadiscourse:** lines telling the reader what to notice or how much a point matters. If the prose shows it, delete the aside.
- **Weasel attribution:** "experts agree", "studies show". Name the source or ask the user for it; never invent one.
- **Texture slop:** synonym cycling, repeated sentence shapes, stacked punchy fragments, emoji headings, decorative mid-sentence bold, bullets where two sentences would read better, em dashes used as a rhythm crutch.

## Checklist

- The author's point, claims, numbers, and examples are unchanged - nothing was invented.
- Distinctive voice survived: edge, humour, profanity, self-interruption, spoken cadence, honest admissions.
- Every remaining generic sentence passes the portability test: if it could move unchanged to another company or product, it was cut or made specific.
- Vague claims became facts: names, numbers, dates, mechanisms; active voice with human subjects.
- Cutting was proportional to the actual slop, not a compression pass.
- Audit mode produced quoted findings only - no rewrite, no score, no authorship claim.

## Guardrails

- Return the edited draft unless the user has requested saving, committing, publishing, or sending it. Perform only the requested actions.
- Do not add facts, statistics, quotes, or sources that are not already in the draft or supplied by the user.
- Do not flatten legal, medical, financial, or safety wording where precision is the point - flag it and ask.
