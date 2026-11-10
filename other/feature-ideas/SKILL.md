---
name: feature-ideas
version: 0.2.0
license: MIT
metadata:
  formerly: special
description: Use when asked what to build next, what features a repo is missing, where the opportunities are, or to suggest a direction or roadmap grounded in the code. Triggers on "what should we build next", "what's missing", "suggest features", "what's the next thing". Proposes opportunities, not fixes; for finding problems use repo-audit, bug-hunt, or security-sweep. (formerly special)
---

# feature-ideas

The audit skills find problems. `feature-ideas` proposes new features based on capabilities and evidence already in the repository.

**Core principle:** every proposal is grounded in evidence already in the repo. **If you cannot cite repository evidence, omit the proposal.** No trend-chasing, no wishlist, no feature you cannot tie to something that already exists.

**Read-only.** `feature-ideas` proposes; it never builds. Choosing and implementing a feature are later steps.

## What this is not

- Not the audit trio. [repo-audit](https://github.com/escoffier-labs/skillet/blob/main/skillet/skills/repo-audit/SKILL.md), [bug-hunt](https://github.com/escoffier-labs/skillet/blob/main/skillet/skills/bug-hunt/SKILL.md), and [security-sweep](https://github.com/escoffier-labs/skillet/blob/main/skillet/skills/security-sweep/SKILL.md) find problems. `feature-ideas` finds opportunities. A bug is not a feature.
- Not `superpowers:brainstorming`. `superpowers:brainstorming` designs an idea you already have. `feature-ideas` finds the idea worth designing. A chosen proposal flows into `superpowers:brainstorming` next.

## Read the project first

Before proposing anything, read what the project says it is and is not: README, CLAUDE.md / AGENTS.md, docs, declared roadmap, stated non-goals. A proposal that contradicts a declared non-goal is cut, or flagged as a deliberate challenge to it with that called out. Understand the project's scope before proposing additions.

## The signals (where proposals come from)

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

- **Feature:** what to build, concretely, in one or two sentences.
- **Signal:** the evidence in the repo, with a file reference. Without evidence, omit the proposal.
- **Who it serves:** the concrete user or operator need. If you cannot name the need, YAGNI cuts it.
- **Fits because:** the existing abstractions, patterns, or data it reuses. Omit a proposal that requires a rewrite to exist.
- **Smallest version:** the minimum that delivers the value; note any larger ambition as later work, do not propose the mega-feature.
- **Effort:** S / M / L.
- **Leverage:** impact relative to effort, the sort key.
- **Confidence + open questions:** direction is the user's call, so flag every assumption and what they must confirm. Mark speculative proposals plainly.

## Scope

Default: the whole repo, since opportunities live in the gaps between parts. Narrow on request to a subsystem, a package, or "what does this one module want next". `feature-ideas branch` reads only what the current branch changed and proposes the natural follow-ups to that work.

## Output shape

Its own artifact, the proposal list, sorted by impact relative to effort, and audit-format-compatible so a picked item composes into the same backlog:

```markdown
## feature-ideas: <repo> (<date>)

### Overview
One paragraph: the strongest opportunity and the through-line across the proposals.

### Proposals (sorted by impact relative to effort)
#### [LEVERAGE: high/med/low] Feature
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

- A chosen proposal hands to `superpowers:brainstorming` to design, then `superpowers:writing-plans` to plan, then `superpowers:subagent-driven-development` to build. `feature-ideas` stops at the proposal list.
- Problems found along the way route to the audit trio, not into the proposal list. A missing test is a repo-audit finding, a wrong result is a bug-hunt finding.
- Direction is the user's decision. `feature-ideas` recommends and ranks; it does not commit the project to anything.

## Common mistakes

| Mistake | Reality |
|---------|---------|
| Generic ideas not tied to the repo | If you cannot cite the repository evidence, you are guessing, not proposing. |
| Proposing what the project declared a non-goal | Read the README and non-goals first. A proposal that contradicts the project's intent is noise. |
| A mega-feature wishlist | Propose the smallest slice that delivers value. Nobody builds the ten-page dream. |
| Re-proposing something that already exists | Grep before you suggest. Proposing an existing feature reads as not having read the code. |
| Dressing a bug up as a feature | Problems go to the audit trio. `feature-ideas` is opportunities only. |
| Chasing whatever is fashionable | Ecosystem fit means serving the stated goals, not bolting on the trend of the month. |
| Starting to build the proposed feature | Read-only. The proposal list is the deliverable; implementation uses `superpowers:brainstorming`, `superpowers:writing-plans`, and `superpowers:subagent-driven-development` or `superpowers:executing-plans`. |
