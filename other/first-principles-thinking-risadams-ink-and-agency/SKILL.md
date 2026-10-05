---
name: first-principles-thinking
category: research-analysis
description: >
  Use when the user wants to challenge assumptions, break down a complex problem from
  scratch, or approach something with first principles reasoning. Triggers on: 'first
  principles', 'challenge assumptions', 'why do we do it this way', 'rethink', 'from
  scratch', 'fundamental truths'.
codex-short-description: "Challenge assumptions and rebuild a problem from first principles"
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
related-skills:
  - idea-generate
  - clarity-council
loop-eligible: false
compatibility: claude-code codex opencode
---

# First Principles Thinking

You strip a problem back to what is actually known and rebuild from there. The value is in
finding the assumption nobody noticed they were making.

## Separate what is verified from what is inherited

List the claims the current approach rests on and mark each: physical or mathematical
constraint, verified fact, industry convention, or assumption never tested. Most of what feels
like a constraint is the fourth category. "We can't because X" is the sentence to interrogate,
and the interrogation is simply: how do we know X?

## Attack analogy-based reasoning specifically

"Everyone in this industry does it this way" explains what is, not what must be. Conventions
encode the constraints of the moment they were formed, and those constraints frequently no
longer hold. Ask what changed since this practice was established.

## Rebuild without importing the old shape

Having decomposed, construct the solution from the genuine constraints alone. The failure mode
is decomposing and then reassembling the existing answer with new justification — check whether
your conclusion could have been reached without the analysis.

## Quantify where the reasoning turns on a number

Order-of-magnitude estimates settle arguments that qualitative reasoning cannot. If a claim
rests on a cost, a rate, or a limit, put a number on it — the number frequently makes the debate
disappear in one direction or the other.

## Respect the constraints that are real

First-principles reasoning that ignores regulation, physics, existing contracts, or the
organization's actual capacity produces confident nonsense. The point is to distinguish real
constraints from imagined ones, not to deny that any exist.

## Know the cost

This is expensive thinking and most decisions do not warrant it. Reserve it for decisions that
are consequential, expensive to reverse, or where the conventional answer keeps producing bad
outcomes.

## Reporting

Present the assumptions found and their status, the constraints that survived scrutiny, the
reconstructed approach, and specifically what changed versus the conventional answer.

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/first-principles-thinking.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
