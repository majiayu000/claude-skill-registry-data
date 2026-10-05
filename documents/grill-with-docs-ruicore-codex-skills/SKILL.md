---
name: grill-with-docs
description: Deep, docs-grounded pressure-testing session for plans, domain models, workflow semantics, and architectural assumptions against repository language and implementation reality. Use when the user wants an adversarial, iterative grilling session rather than a one-shot architecture assessment. Default to read-only critique; update durable docs only with explicit user authority or an applicable repository rule requesting persistence. Route one-shot architecture assessments to architecture-review and settled-decision recording to decision-trace-writer.
---

# Grill With Docs

Use this skill to turn vague architecture or domain discussion into precise
language and evidence-tested operational semantics.

Do not use it for ordinary bug fixes, small code edits, routine PR review, or one-off code tracing unless the user explicitly wants architectural pressure-testing.

## Select The Mode

Use **Critique Mode** by default. Treat requests to grill, challenge,
pressure-test, assess, or review as read-only unless the user says otherwise.
Inspect repository evidence, challenge assumptions, surface contradictions and
decision gaps, run scenario pressure tests, and return findings, confidence,
and questions. Do not edit durable documentation in this mode; present any
useful wording as a proposed update only.

Use **Persistence Mode** only when the user explicitly authorizes documentation
updates or an applicable repository instruction explicitly requests them.
Persist only settled knowledge that survived the self-challenge pass, and write
only to the repository-approved location. Never infer write authority from the
mere existence of `.manifest`, `CONTEXT`, ADR, trace, or specification files.

Route adjacent work deliberately:

- Use `architecture-review` for a one-shot architecture assessment or review.
- Use `decision-trace-writer` to record a decision that is already settled.
- Keep `grill-with-docs` for the deep, iterative, docs-grounded adversarial
  session that resolves assumptions before conclusions.

## Core Loop

1. Discover the repository's local knowledge system before deep critique.
2. Resolve upstream concepts before downstream mechanics.
3. Ask one major question at a time unless several decisions are tightly coupled.
4. For each major question, explain why it matters, give the recommended answer, and name plausible alternative interpretations.
5. When code can answer the question, inspect the code instead of asking.
6. Pressure-test claims with concrete runtime scenarios: failure, retry, concurrency, partial success, rollback, ownership, and state transitions.
7. Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.
8. After raising objections, run the Self-Challenge Pass before turning them into conclusions or durable knowledge.
9. In Persistence Mode only, preserve stable, validated knowledge. Do not
   fossilize brainstorming.

## Repository Discovery

Do not assume fixed documentation paths.

First identify semantic roles:

- Agent/repo instructions: examples include `.manifest/AGENTS.md`, `AGENTS.md`, `.ai/*`, `CLAUDE.md`.
- Domain context or glossary: examples include `.manifest/context.md`, `CONTEXT.md`, `docs/architecture/*`, `README` sections.
- Durable knowledge or decisions: examples include `.manifest/knowledge.md`, `docs/adr/*`, `decisions/*`.
- Validation or operational constraints: examples include `.manifest/validation.md`, deployment docs, runbooks, test docs.
- PR/commit conventions: examples include `.manifest/pr.md`, contribution docs.

Prefer pointer files over broad scans. If a repo instruction file says where context belongs, follow that rule.

In Critique Mode, repository discovery remains read-only. In Persistence Mode,
use the location required by repository instructions. If the repository accepts
`.manifest` for personal agent knowledge, keep that knowledge there unless the
user explicitly requests public or team documentation.

## Documentation Writes In Persistence Mode

Create or update files only when Persistence Mode is authorized and stable
knowledge is ready to preserve.

When writing:

- Follow the repo's existing knowledge structure and naming.
- If `.manifest/AGENTS.md` exists, read it first and obey its routing rules.
- If `.manifest/context.md` exists, use it for orientation, domain language, architecture shape, and reusable implementation patterns.
- If `.manifest/knowledge.md` exists, use it for confirmed decisions, repeated wrong assumptions, and durable behavioral facts.
- If `.manifest/validation.md` exists, use it for runtime validation data, test assets, environment constraints, and verification workflows.
- If the repo instead uses `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`, use those conventions.
- If no suitable structure exists, propose the smallest repo-local structure
  and obtain explicit authority before creating it. For personal/local agent
  knowledge, prefer `.manifest/` only when the repository accepts it.

Do not update public product docs when the stable knowledge is only personal agent context. Do not create ADRs unless the repo already uses ADRs or the user accepts that convention.

## Domain Language Discipline

Treat terminology drift as architectural drift.

When the user uses vague or overloaded terms, stop and clarify. Propose canonical terms and distinguish adjacent concepts explicitly.

If existing docs define a term, compare the user's wording against that definition. Surface contradictions directly:

> Existing context defines cancellation as order-level, but this proposal implies item-level cancellation. Which model is intended?

When a term is resolved, persist it only in Persistence Mode and only if it is
domain-level and likely to help future work. Avoid implementation trivia in
glossary/context files.

## Implementation Reality

Architecture claims must survive contact with code.

When the user states how something works:

- Trace the actual runtime path.
- Name the branch conditions and ownership boundaries.
- Distinguish synchronous acknowledgements from asynchronous payloads.
- Distinguish wrapper/service objects from real external connections.
- Surface doc/code drift as a first-class finding.

If implementation and desired architecture disagree, ask whether the code is wrong, the docs are stale, or the proposal intentionally changes the model.

## Self-Challenge Pass

After raising objections, try to disprove each serious objection with repository evidence.

- Search for counter-evidence in code paths, docs, tests, runtime wiring, context files, ADRs, rollout notes, and explicit user constraints.
- Distinguish objections that survive evidence from objections that are only missing-context concerns.
- Downgrade or remove objections when repository evidence invalidates them.
- Preserve uncertainty instead of overstating doc/code drift, ownership gaps, or semantic conflicts.
- Do not manufacture criticism if the repository evidence supports the proposal.
- Avoid using the same reasoning path to both create and validate the objection without challenge.
- Persist only objections, decisions, or glossary updates that survive this pass or are explicitly accepted by the user as unresolved context.

## Scenario Pressure Tests

Do not leave claims abstract. Test them with concrete scenarios such as:

- duplicate request or duplicate webhook delivery
- timeout followed by late success
- retry after process restart
- concurrent mutation of the same workflow
- partial success and rollback
- missing external asset or unavailable runtime service
- ownership crossing frontend/backend or service boundaries

Use scenarios to force decisions about state, ownership, retries, consistency, and user-visible results.

## Decision Persistence In Persistence Mode

Use status labels when useful:

- Proposed: exploratory, not durable.
- Validated: accepted and backed by code, docs, tests, or explicit user decision.
- Deprecated: no longer preferred but historically relevant.
- Superseded: replaced by a newer decision.

Suggest an ADR only when all are true:

1. The decision is hard to reverse.
2. It would be surprising without explanation.
3. It reflects a real trade-off among alternatives.

If any condition is missing, prefer a lightweight context or knowledge note.

If Persistence Mode is authorized and the repo uses the bundled formats, use
[CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) or
[ADR-FORMAT.md](./ADR-FORMAT.md). Otherwise follow the repo's existing format.

## Portability Notes

- Specific to the author's current workflow: `.manifest/` is a preferred personal agent-knowledge location only when the target repository already defines or accepts it.
- Reusable: repo-convention discovery, evidence-backed domain pressure testing, self-challenge before preserving claims, and stable-knowledge persistence.
- Adapt before reuse: inspect the target repository's instruction files, durable documentation locations, public/private doc boundary, and ADR or context-file conventions before writing.
