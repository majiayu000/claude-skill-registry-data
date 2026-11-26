---
name: brainstorming
description: Use before spec writing when the approach is unclear, several designs or ways to build it are plausible, or the engineer wants to explore alternatives before committing.
type: skill
license: MIT
compatibility:
  - claude-code
  - cursor
  - codex
user-invocable: false
---

# Brainstorming

> **Tool discipline:** read-only — `Read`/`Grep`/`Glob` and read-only `Bash`. Never `Edit`/`Write` source, tests or config; the approved direction feeds `spec-driven-development`, which writes the spec.

## Overview

Compare 2-3 concrete approaches before committing to one, then get the engineer's pick. The default output is **three short paragraphs**; the isolated-subagent divergence mode is opt-in.

## When To Use

- The engineer asks "how should we..." / "what's the best way to...", or multiple approaches are plausible
- Before `spec-driven-development` when the design direction is not obvious

### When NOT To Use

- The approach is already agreed, or the task is a bug fix, config change, or narrow refactor

## Workflow

1. **Explore first:** the affected code, `architecture-principles.md` if present, and recent git history in the area. Ask at most one or two clarifying questions, only ones that would eliminate an approach.
2. **Write three short paragraphs:**
   - *Approaches* — 2-3 options, each one or two sentences naming the files/components it touches and its cost.
   - *Tradeoffs* — what each one is good at and where it breaks in this codebase. Honest; do not soft-sell the favourite.
   - *Recommendation* — the pick, why, and what would change it. If only one option is viable, say so and why.
3. **Wait for the engineer's direction.** No implementation until they confirm or redirect.
4. If the work continues to a spec and `docs/specs/` exists, save the decision to `docs/specs/YYYY-MM-DD-<topic>-brainstorm.md` (approaches, rationale, rejected options).

## Divergence Mode (opt-in)

Run it only when the engineer asks for wide / divergent exploration. For an architecture-shaping decision (new boundary, public contract, irreversible migration), offer it in one line with its cost (~6-10 agent calls); do not start it unasked.

1. Pick 3-5 frames from `.claude/references/divergence-frames.md`, including an adversarial one (`F-REG`, `F-FRD`, `F-AUD`) when money, auth, or audited state is involved.
2. Spawn one subagent per frame in one message, each with only the problem statement and its frame, told to ban the first three obvious answers and return JSON only: `{ "approach", "how", "load_bearing_assumption", "risk" }`. Branches never see each other.
3. Critic pass (orchestrator, not a generator): score novelty / viability / fit, cluster by angle, deepen the top 2-3 into the default format, and add a **Trap Register** — attractive-but-broken approaches with one-line reasons. The register becomes the spec's "Rejected alternatives". A divergence result without one is incomplete.

## Verification

- [ ] Context explored before proposing; at least 2 approaches (or a stated reason for one)
- [ ] Recommendation stated with reasoning; the engineer chose a direction before any implementation
- [ ] Divergence mode ran only on request, with isolated branches and a Trap Register
