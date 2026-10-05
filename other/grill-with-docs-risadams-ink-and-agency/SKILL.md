---
name: grill-with-docs
category: research-analysis
description: Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.
codex-short-description: "Stress-test a plan against the domain model, updating CONTEXT.md and ADRs"
related-skills:
  - grill-me
  - domain-modeling
  - clarity-council
loop-eligible: false

compatibility: claude-code codex opencode
---
<what-to-do>

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.

If a question can be answered by exploring the codebase, explore the codebase instead.

</what-to-do>

<supporting-info>

## Domain awareness

This is the grilling half. The domain-model half — where `CONTEXT.md` and `docs/adr/` live, how to challenge terms against the glossary, and when a decision earns an ADR — is the [domain-modeling](../domain-modeling/) skill.

**Invoke `domain-modeling` by name at the start of the session**, before the first question. This pointer is the reliability weak spot: an agent told to load "the grilling skills" reliably loads the interview half and silently skips the modelling half, and the tell is a session that ends with `CONTEXT.md` untouched. Load it explicitly, then run its discipline **inline** as the interview goes:

- **Look for the artifacts during codebase exploration.** A root `CONTEXT.md` (single context) or a `CONTEXT-MAP.md` pointing at several; ADRs under `docs/adr/`. Create either lazily — only when you have something to write.
- **Challenge every term against the glossary**, sharpen fuzzy language, and stress-test relationships with concrete edge-case scenarios.
- **Cross-reference claims with the code**, and surface contradictions the moment you find one.
- **Write resolved terms to `CONTEXT.md` right there** — never batched — using [CONTEXT-FORMAT.md](../domain-modeling/CONTEXT-FORMAT.md).
- **Offer an ADR only when all three gates hold** (hard to reverse, surprising without context, a real trade-off), using [ADR-FORMAT.md](../domain-modeling/ADR-FORMAT.md).

## Closing the session

Most of what gets settled here lands in **neither** artifact: the glossary takes terms, ADRs take the rare three-gate decision, and everything else — ordering guarantees, negative requirements, numeric defaults, the reasoning behind each choice — exists only in this conversation. A session that produces a sharper glossary and zero ADRs worked as designed, but the bulk of the value is still in the context window.

So don't end on "let me know what you'd like next". Close with the state and the next move:

1. What landed on disk — terms written, ADRs offered and taken.
2. What was settled but written nowhere, listed explicitly.
3. **The next step, in this same conversation**: `plan-to-spec` synthesises what's here into a spec without re-interviewing. Small enough to build now? `implement`. Blocked on someone else's knowledge? `plan-to-questionnaire`.

Clearing this conversation without doing one of those loses the decisions.

</supporting-info>

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/grill-with-docs.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
