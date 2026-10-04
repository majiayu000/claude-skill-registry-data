---
name: special
version: 0.1.0
license: MIT
description: Use when asked what to build next, what features a repo is missing, where the opportunities are, or to suggest a direction or roadmap grounded in the code. Triggers on "what should we build next", "what's missing", "suggest features", "what's the next thing". Proposes opportunities, not fixes; for finding problems use line-check, bug-hunt, or security-sweep.
---

# special

The audit skills walk the line looking for what is broken. `special` walks the walk-in looking for what is possible. The chef sees what is fresh and plentiful on the shelves and proposes the dish worth adding to the board tonight, the one that uses what is already in the kitchen. A special is not invented out of nothing; it is the obvious next thing made from what you already have.

**Core principle:** every proposal is grounded in evidence already in the repo. **If you cannot point to the signal in the walk-in, it is not a special, it is a daydream.** No trend-chasing, no wishlist, no feature you cannot tie to something that already exists.

**Read-only.** `special` proposes; it never builds. Picking the dish and cooking it are later steps.

## What this is not

- Not the audit trio. [line-check](../line-check/SKILL.md), [bug-hunt](../bug-hunt/SKILL.md), and [security-sweep](../security-sweep/SKILL.md) find problems. `special` finds opportunities. A bug is not a feature.
- Not [mise](../mise/SKILL.md). mise designs an idea you already have. `special` finds the idea worth designing. A chosen special flows into mise next.

## Read the kitchen first

Before proposing anything, read what the project says it is and is not: README, CLAUDE.md / AGENTS.md, docs, declared roadmap, stated non-goals. A proposal that contradicts a declared non-goal is cut, or flagged as a deliberate challenge to it with that called out. Know the dish before you suggest the next course.

## The signals (where specials come from)

Each lens reads the existing repo for evidence of an obvious next step. With parallel subagents, one finder per lens; otherwise sequential.

| Lens | The signal |
|------|------------|
| Unfinished work | TODO/FIXME, stubbed functions, disabled tests, commented-out code that hints at intent, "coming soon" in docs |
| Asymmetry | Supports X for A but not B; read path with no write path; create/update with no delete; one integration where the shape implies two |
| Adjacent capability | One small step from something that exists: you parse it, so you could validate it; you have the data, so you could export it |
| Friction | Manual runbook steps that beg automation, repeated operator actions, a known-limitations or FAQ section describing recurring pain |
| Ecosystem fit | A capability comparable tools in this exact niche have that this lacks AND that serves the project's stated goals, not a fashionable add-on |

A proposal with no lens behind it does not get written down.

## Each proposal earns its place

For every candidate that survives, write a card:

- **The dish:** what to build, concretely, in one or two sentences.
- **Signal:** the evidence in the repo, with a file reference. This is the load-bearing field; no signal, no card.
- **Who it serves:** the concrete user or operator need. If you cannot name the need, YAGNI cuts it.
- **Fits because:** the existing abstractions, patterns, or data it reuses. A special that needs a rewrite to exist is not a special.
- **Smallest version:** the minimum that delivers the value; note any larger ambition as a later course, do not propose the mega-feature.
- **Effort:** S / M / L.
- **Leverage:** impact relative to effort, the sort key.
- **Confidence + open questions:** direction is the user's call, so flag every assumption and what they must confirm. Mark speculative proposals plainly.

## Scope

Default: the whole repo, since opportunities live in the gaps between parts. Narrow on request to a subsystem, a package, or "what does this one module want next". `special branch` reads only what the current branch changed and proposes the natural follow-ups to that work.

## Output shape

Its own artifact, the specials board, leverage-sorted, and audit-format-compatible so a picked item composes into the same backlog:

```markdown
## special: <repo> (<date>)

### The board
One paragraph: the strongest opportunity and the through-line across the proposals.

### Specials (leverage-sorted)
#### [LEVERAGE: high/med/low] The dish
- **Signal:** evidence + file:line
- **Who it serves:** the need
- **Fits because:** existing abstractions reused
- **Smallest version:** the minimum slice
- **Effort:** S / M / L
- **Confidence:** high/med/low + open questions for the user

### Considered and cut
- idea - why it was cut (ungrounded / contradicts a non-goal / already exists)
```

## Boundaries

- A chosen special hands to [mise](../mise/SKILL.md) to design, then [recipe](../recipe/SKILL.md) to plan, then [fire](../fire/SKILL.md) to build. `special` stops at the board.
- Problems found along the way route to the audit trio, not into the board. A missing test is a line-check finding, a wrong result is a bug-hunt finding.
- Direction is the user's decision. `special` recommends and ranks; it does not commit the project to anything.

## Common mistakes

| Mistake | Reality |
|---------|---------|
| Generic ideas not tied to the repo | If you cannot cite the signal in the walk-in, you are guessing, not proposing. |
| Proposing what the project declared a non-goal | Read the README and non-goals first. A special that fights the project's intent is noise. |
| A mega-feature wishlist | Propose the smallest slice that delivers value. Nobody builds the ten-page dream. |
| Re-proposing something that already exists | Grep before you suggest. Proposing an existing feature reads as not having read the code. |
| Dressing a bug up as a feature | Problems go to the audit trio. `special` is opportunities only. |
| Chasing whatever is fashionable | Ecosystem fit means serving the stated goals, not bolting on the trend of the month. |
| Starting to build the special | Read-only. The board is the deliverable; cooking is mise, recipe, fire. |
