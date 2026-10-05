---
name: context-anchor
description: 'Interviews the team once and writes a single GTM_CONTEXT.md (ICP, positioning, voice, proof, competitors) that every other GTM skill reads, then scores how fresh and complete it is. Use when: set up gtm context, company context file, shared positioning file, brand context, icp file, onboard the gtm skills, context is stale, refresh positioning.'
---

# Context Anchor (CANVAS Framework)

Most GTM skills share one gap: each one re-asks who the buyer is, what the product does, and why it wins, and gets a slightly different answer every time. Context Anchor captures those answers once in a versioned file, then keeps the file honest with a freshness and completeness score so downstream skills never run on stale positioning.

## Core Principle

**One source of truth, dated and scored.** A context file nobody has touched in a quarter quietly spreads outdated positioning, because every skill downstream repeats it.

## The CANVAS Framework

| Letter | Section | The Question |
|---|---|---|
| **C** | Claim | What do we say we do better, in one sentence a buyer would repeat? |
| **A** | Audience | Who buys, who uses, who signs? (ICP firmographics + personas) |
| **N** | Need | Which job or pain triggers a purchase right now? |
| **V** | Voice | How we sound: words we use, words we never use, reading level |
| **A** | Alternatives | What else the buyer considers, including doing nothing |
| **S** | Substantiation | Which numbers, logos, and quotes back the claim? |

## Process

1. **Interview** - ask one CANVAS section at a time; accept "unknown" rather than guessing
2. **Draft** - write `GTM_CONTEXT.md` with one H2 per CANVAS section and a `last_reviewed` date per section
3. **Score completeness** - each section scores 0 (missing), 1 (asserted), or 2 (asserted + evidence); completeness = total / 12
4. **Score freshness** - per section, `freshness = max(0, 1 - days_since_review / 90)`
5. **Gate** - context health = completeness × average freshness; below 0.6, downstream skills should warn before running
6. **Hand off** - list which sections each paired skill reads so owners know what to update

## Output

Save to `GTM_CONTEXT.md` at the repo root, plus `outputs/context-anchor-health-[YYYY-MM-DD].md`

| Artifact | Description |
|---|---|
| **GTM_CONTEXT.md** | Six CANVAS sections, each with an owner and `last_reviewed` date |
| **Health table** | Completeness (0-2) and freshness (0-1) per section, plus overall health |
| **Refresh list** | Sections below 0.5 freshness or missing evidence, with the owner to ping |

## Tips

1. **Evidence or it didn't happen** - a claim without proof scores 1, not 2
2. **Name the do-nothing option** - it wins more deals than any competitor
3. **Keep Voice short** - ten "use" words and ten "avoid" words beat a style guide nobody reads

## Pairs With

- **position-lock** - reads Claim, Alternatives; writes back a sharper Claim
- **competitive-battlecard** - reads Alternatives and Substantiation
- **product-announcement**, **demand-engine** - read Audience, Voice
