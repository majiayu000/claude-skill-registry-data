---
name: prose-quality
description: Use when the deliverable is authored or edited prose whose wording matters (docs, READMEs, release notes, public copy) or when the user asks to tighten, de-AI, or review writing. Not for chat answers, code review, or explanations of current work.
---

# Prose quality

An edit succeeds only if readers draw the same conclusions from the new text, with less effort. A draft succeeds only if they draw the conclusions its source evidence supports.

## Keep meaning fixed
- Keep each claim at its original strength and scope. Carry over hedges, conditions, sample sizes, units, hardware, baselines, and "experimental" or "may not" limits. Never turn "did not measure X" into "X was unchanged."
- Add no facts, numbers, or benefits the source lacks. Ask, or leave a marked gap.
- Preserve commands, paths, flags, symbols, quotations, and normative text (MUST, SHOULD) exactly.
- When the text describes code or a tool you can read, check its behavioral claims against it. Fix or flag mismatches and say what you checked.

## Write to the reader
- Name the reader and what they must do or decide, and lead with that.
- Use words that reader would say aloud. A project term they do not use becomes what happens: "circuit breaker" becomes what stops, and when.
- On a screen, the surface sets the length. A label names the thing. Explain only where a competent user would otherwise choose wrong.

## Edit to the requested depth
- Review only: return findings ranked by reader impact, errors (wrong, ambiguous, out of order) before style. No rewrite.
- Editing: keep the author's voice, terms, structure, and the document's conventions (heading case, quote style, spelling). One name per concept.

## Remove generated-sounding patterns
Cut puffery, figurative phrasing, signposting, filler, stacked hedges, summary closers, and decorative bold, emoji, or headers. Thin out em-dash chains, "not X but Y" contrasts, and forced triplets without substituting another tic. Keep a negation that states a real limit or hazard.

## Before returning
Compare old and new for any claim that got stronger, weaker, or lost a qualifier. Name material ambiguities instead of writing around them.
