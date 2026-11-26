---
name: content-quality-lord
description: Detect and remove AI slop patterns from generated content. Use when the user asks to deslop, de-AI, audit content quality, or when aiZee itself generates content that must pass a quality gate.
triggers:
  - content quality lord
  - deslop
  - de-ai
  - remove ai patterns
  - content quality
  - ai slop
  - audit writing
  - make it sound human
personas:
  - DOC
  - ARCH
  - PRODUCT
  - UX
  - DATA
tech_stack:
  - markdown
  - python

---

# Content Quality Lord

Detect and remove AI slop patterns from writing without flattening personal voice. Two modes:

**Edit (default).** The user shares a draft to fix. Make the minimum effective edit and return the edited draft plus a **What changed** section.

**Detect.** The user asks whether a piece is AI slop, or asks to audit without rewriting. Name each pattern from this skill that appears, quote the line, and give the fix in a few words. Do not rewrite, score, or guess whether AI wrote it. Named patterns are evidence the user can check.

## Banned words (remove unless quoted as examples)

delve, foster, leverage, utilize, facilitate, empower, streamline, robust, cutting-edge, paradigm shift, game changer, this is huge, this changes everything, tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.

## Often-empty adverbs (cut when they add nothing)

just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably.

## Often-empty phrases (cut when they delay the point)

it's worth noting, it's important to note, at the end of the day, when it comes to, at its core, in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in order to, going forward, in this article, let's dive in.

## Patterns to cut

1. **Binary contrasts.** "This is not X. It's Y." → State Y directly.
2. **Throat-clearing openers.** "Here's the thing," "Let me be clear" → Cut and state the point.
3. **Faux-insight setups.** "What most people get wrong," "Here's what nobody tells you" → Make the claim stand alone.
4. **Colon reveals.** Noun phrase + colon + lowercase reveal → Rewrite as a plain sentence.
5. **Superficial analysis.** Trailing `-ing` clauses: "highlighting," "underscoring" → Replace with concrete consequence.
6. **Importance puffery.** "Stands as a testament," "marks a pivotal moment" → State the fact.
7. **Interpretive metadiscourse.** "That last part matters," "The key point is" → Delete or replace with support.
8. **Weasel attribution.** "Experts agree," "studies show" → Name the source or cut.
9. **Fake-strong verbs.** "Serves as a centralized hub" → "Tracks sponsors, drafts, due dates."
10. **Synonym cycling.** Repeating terms for style → Repeat the clear word.
11. **Negative listing.** "Not a X. Not a Y. A Z." → Just say Z.
12. **Dramatic fragmentation.** "X. And Y. And Z." → Use complete sentences.
13. **Robotic rhythm.** Repeated sentence shapes → Vary the shape.
14. **Rhetorical setups.** "What if I told you," "Plot twist" → Drop and make the point.
15. **Fake-profound kickers.** Final "deep" line → Delete, end on the clearest concrete sentence.
16. **Summary-recap endings.** "In conclusion," "Ultimately" → End on the last concrete point.
17. **Formatting slop.** Emoji headings, decorative bold, bullets that should be prose → Format follows content.
18. **Em dashes.** Not a default rhythm crutch. 0 in short copy, 1-2 max in longer drafts.

## Portability test

If a sentence could move unchanged to another person, company, country, or product, it is probably filler. Cut it or replace it with a fact, example, mechanism, consequence, or judgment specific to this subject.

## Workflow

1. Read the full draft before editing.
2. Identify the core point and 3-5 voice signals to preserve. Keep this note internal.
3. For a detect request, return the findings report and stop.
4. For an edit, make the minimum effective changes, then check against `EVAL.md`.
5. If any check fails, fix and re-check.
6. Output the full edited draft and a short **What changed** section.
