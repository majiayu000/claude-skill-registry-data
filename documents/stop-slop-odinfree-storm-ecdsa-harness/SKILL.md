---
name: stop-slop
description: Audit and rewrite prose to remove common AI writing patterns. Use when drafting, editing, or reviewing writing that feels generic, over-polished, promotional, or structurally repetitive. Supports rewrite mode and detect-only mode.
---

# Schwafelbräms (stop-slop)

*Stop Slop. Vendored from [welttowelt/stop-slop-refined](https://github.com/welttowelt/stop-slop-refined) (MIT, see LICENSE and ATTRIBUTION.md beside this file); only this title line was changed.*

Remove common AI writing patterns from prose.

Use this as a baseline editing skill. It is not a personal voice layer.

Companion references:

- [references/words.md](references/words.md)
- [references/patterns.md](references/patterns.md)
- [references/examples.md](references/examples.md)

## Modes

**Rewrite** is the default.

- flag the main issues
- rewrite the text
- run a second pass on the rewrite

**Detect** means flag only.

- do not rewrite
- show what reads as AI
- separate clear problems from judgment calls

Trigger detect when the user says `detect`, `flag only`, `audit only`, `scan`, or equivalent.

## Core rules

1. Cut filler.
2. Break formulas.
3. Name the actor.
4. Be specific.
5. Trust the reader.
6. Vary rhythm.
7. Remove false emphasis.
8. Cut generic endings.

## What to look for

- throat-clearing openers
- contrast templates like `not x, but y`
- generic intensifiers
- vague attribution
- passive construction where the actor matters
- fake significance
- rhythm that feels too even
- lists that sound generated instead of chosen
- clean but empty conclusions

For word-level flags, see [references/words.md](references/words.md).

For structural flags, see [references/patterns.md](references/patterns.md).

## Quick checks

- too many adverbs
- too many abstract nouns
- same sentence length three times in a row
- same paragraph shape again and again
- `Let's dive in` or similar signposting
- `Great question` or similar chatbot artifacts
- `as of my last update` or similar disclaimers
- bold, emoji, markdown, or formatting that does not fit the destination

## Output format

### Rewrite mode

1. **Issues found**
2. **Rewrite**
3. **What changed**
4. **Second pass**

### Detect mode

1. **Issues found**
2. **Assessment**
3. **Fix direction**

## Severity

### P0

Credibility problems:

- fake sourcing
- chatbot artifacts
- cutoff disclaimers
- markdown in plain-text contexts
- obvious significance inflation

### P1

Clear AI smell:

- tier-1 word hits
- repeated templates
- formulaic openings
- repeated contrasts
- rhythm that feels machine-even

### P2

Polish:

- too many triads
- too many bullets
- repetitive paragraph shapes
- conclusion that says nothing

## Context calibration

Be stricter in:

- essays
- investor emails
- public posts
- website copy

Be looser in:

- docs
- technical notes
- fast internal chat

Do not blindly remove a word just because it appears in a list. Context matters. Technical writing can justify some words that sound bad in marketing copy.

## Voice calibration

If the user provides a writing sample, match the sample after removing AI patterns.

Do not replace one generic voice with another generic voice.

## Rewrite-from-scratch trigger

Rewrite from scratch if the draft has:

- many tier-1 word hits
- multiple structural patterns
- uniform rhythm throughout
- no clear human point of view

In that case:

1. state the real point in one sentence
2. rebuild from there

## Final check

Before you finish, ask:

- does this sound like a person or like a cleaned-up machine draft?
- is the point sharper now?
- did clarity improve, or just surface texture?
