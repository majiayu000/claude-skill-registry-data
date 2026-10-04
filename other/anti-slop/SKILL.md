---
name: anti-slop
description: >
  Eliminate AI-sounding patterns from any written output. Applies editorial rules synthesized from
  the best open-source anti-slop tools: banned phrases, structural pattern detection, false agency
  checks, and a scoring rubric. Use as a quality gate for ANY content — blog posts, social media,
  emails, documentation, marketing copy. Triggers on: "make it sound human", "less AI", "remove slop",
  "humanize this", "doesn't sound natural", "too AI", "rewrite naturally", or when reviewing any
  AI-generated text before publishing.
source: https://github.com/shannhk/avoid-slop
author: shannhk (curation), blader (humanizer), Hardik Pandya (stop-slop), Matt Shumer (unslop), Paul Bakaus (impeccable)
category: writing
tags: [writing, quality, anti-ai, humanize, editing, tone, voice]
allowed-tools: Read
---

# Anti-Slop Writing Quality Gate

Eliminate recognizable AI patterns from text. Synthesized from the best open-source anti-slop tools.

## Core Philosophy

LLMs collapse toward defaults — the same phrases, structures, and rhythms. There are two fixes:
1. **Remove** known bad patterns (this skill)
2. **Add** enough context that the model makes informed, original choices

Telling a model to "write better" just creates new slop. Listing what NOT to do forces genuine novelty.

## When to Apply

Run this check on ANY text before it ships — blog posts, tweets, emails, docs, marketing copy.
Load [references/patterns.md](references/patterns.md) for the full ruleset.

## Quick Audit (5-Point Check)

Before publishing, verify:

1. **No banned phrases** — scan for the ~30 phrases listed in patterns.md
2. **No false agency** — inanimate things don't "tell us", "reward", or "demand"
3. **No em-dash abuse** — zero em-dashes (use commas, periods, or parentheses instead)
4. **Specific over vague** — numbers, names, dates instead of "various", "numerous", "significant"
5. **Voice present** — does it sound like a specific person wrote it, or could any AI have produced it?

## Scoring Rubric (from stop-slop)

Score each piece out of 50. **Below 35 = mandatory revision.**

| Category | Points | What to Check |
|----------|--------|---------------|
| Authenticity | /10 | Genuine voice? Opinions? First-person where appropriate? |
| Specificity | /10 | Concrete details, numbers, names? Or vague generalities? |
| Structure | /10 | Varied sentence length? No formulaic patterns? |
| Word choice | /10 | Fresh vocabulary? No crutch words? |
| Flow | /10 | Natural rhythm? Reads like speech, not a textbook? |

## Two-Pass Revision Process (from humanizer)

**Pass 1 — Rewrite:** Apply all rules from patterns.md. Remove banned phrases, fix false agency, vary rhythm.

**Pass 2 — Self-critique:** Ask "What still makes this obviously AI-generated?" about your own output. Fix what you find. The self-critique loop catches patterns that survive the first edit.

## References

- **[patterns.md](references/patterns.md)** — Complete banned phrase list, structural patterns to avoid, and detection rules. Load when auditing text.

## Attribution

This skill synthesizes rules from four open-source tools. All credit to the original authors:

- **[humanizer](https://github.com/blader/humanizer)** by blader (MIT, 10,300+ stars) — two-pass audit, 25 pattern categories
- **[stop-slop](https://github.com/hardikpandya/stop-slop)** by Hardik Pandya (MIT, 2,100+ stars) — banned phrases, scoring rubric
- **[unslop](https://github.com/mshumer/unslop)** by Matt Shumer (MIT, 180+ stars) — empirical default detection
- **[impeccable](https://github.com/pbakaus/impeccable)** by Paul Bakaus (Apache 2.0, 11,700+ stars) — design slop detection

Curated by **[shannhk](https://github.com/shannhk/avoid-slop)**.
