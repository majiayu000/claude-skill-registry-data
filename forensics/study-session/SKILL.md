---
name: study-session
version: 2.0.0
description: "Use when the user asks for a guided comprehension/study session over existing code: '/study-session', 'study session', 'sesión de estudio', 'repasemos <subsystem>', 'help me understand <area>', or a recurring comprehension-recovery ritual. Recovers AND measures the mental model of code the user delegated to coding agents. Two modes: deep (45-60 min) and checkpoint (10-15 min). Do NOT use for implementing features, fixing bugs, or code review — nothing is modified in a study session except the comprehension tracking page."
---

# Study Session — recover and measure the theory of a subsystem

A session over **real code in the repo**. The user reads and explains; you probe and grade. The goal is Naur's "theory": the user can defend the subsystem's design, invariants, and failure modes without help. Two modes:

- **Deep** (45-60 min): learn or repair one subsystem/unit. Default for `not-assessed`, `practiced`, or `code-changed` targets.
- **Checkpoint** (10-15 min): measure retention of a due unit — one cold reconstruction + one transfer scenario. Default when the row's next-due date expired.

**Core principle: cold evidence is graded separately from learning.** What the user produces BEFORE your corrections is what gets measured; what they learn after counts as learning, never as certification.

## Finding the comprehension map

The map's schema (columns, status vocabularies, event format, spacing rule) lives in the user's knowledge wiki — this skill defers to it. To locate the map:

1. Resolve the wiki root: follow the `~/.claude/work-wiki` symlink if present; otherwise ask once and offer to create that symlink.
2. Glob `**/projects/*-comprension.md` (or the wiki's declared comprehension-map convention) with `kind: comprehension-map` frontmatter; match the current repo/workspace (git remote or basename) against each map's repo/paths column — one project may span several repos.
3. Exactly one match → use it. None → derive the path from the project name per the wiki's convention, confirm with the user, create from the wiki's schema template. Several → ask.

No wiki or schema at all → offer a minimal inline map: `| Subsystem | Repo/paths | Current evidence | Scope | Last passed | Next due | Gaps |` with outcome (`not-assessed | practiced | partial | defensible`) and validity (`current | evidence-expired | code-changed | code-currentness-unknown`) vocabularies.

## Target selection (risk-first)

Propose ONE target with a one-line reason, in this priority order — the user can override:

1. Relevant code changed since the row's last evidence SHA (`code-changed`).
2. An open gap implicated by a recent MR or incident.
3. High-blast-radius unit overdue.
4. Any other overdue unit.
5. Untested low-risk units.

Preflight: record the current `repo@sha`. If the row has prior evidence, diff the studied paths since its SHA — behavioral drift marks the row `code-changed` regardless of calendar age.

## Deep session flow

1. **Prepare the hidden rubric FIRST — before hearing any answer** (so you can't fit it to what the user says). Read the subsystem, pick 2-4 files/flows that carry its theory, and note internally: expected claims per dimension, acceptable alternatives, the evidence source for each claim, and your uncertainty. Evidence hierarchy: behavior ← code/tests/traces; contracts/invariants ← tests/schemas/API contracts; operational ← tests/logs/runbooks/incidents; design intent ← ADRs/issues/commits/the user's own remembered decision. **Undocumented intent is graded "intent unknown", never as a wrong answer.** If the subsystem is high-risk and has no study units yet, define 3-5 now (request paths, reconciliation loops, retry semantics — coherent responsibilities, not files).
2. **Cold reconstruction (5 min).** No map page, no code, no hints: the user describes from memory the boundaries, the end-to-end flow, one invariant, and the main failure mode. Grade silently against the rubric.
3. **Guided investigation (25-30 min).** Open-repo: code and tests allowed; your hints are not free. Point the user at one file/flow (`file:line`), have them read and explain it back, probe with ONE question at a time, correct with `file:line` evidence. A **substantive hint** (supplies a missing causal link, component, or failure mechanism) caps that item below solid. The user asking you to explain a concept they've never met is a question, not a failed answer — explain it anchored in the code, then hand the thread back.
4. **Novel transfer task (10-15 min).** One exercise the session hasn't rehearsed: predict the externally visible result of a dependency failure; given a symptom, name where to look first and the first three checks; trace a value across components and name where its invariant can break. Include **at least one executable prediction** when test infra is available: the user commits to an answer, then run the test/command and compare. Record only what the execution can establish — a passing test proves the exercised behavior, not the design rationale.
5. **Close.** Ask the user for a 3-5 sentence summary in their own words (reflection evidence, not the grade). Score the four dimensions from the user's INITIAL answers, resolve/open dated gaps, set the next-due date per the wiki's spacing rule, and append the event to the map (verdicts = pre-correction answers).

## Checkpoint flow

One cold reconstruction + one transfer scenario, chosen to cover the row's required dimensions. Renews `defensible` only if the two exercises together cover **every** required dimension — any required dimension left `not-tested` blocks renewal. Score, update dates/gaps, append the event. Escalate to a deep session if the checkpoint fails.

## Grading

Four dimensions, each `solid | partial | weak | not-tested`:

- **Model** — boundaries, dependencies, end-to-end data flow.
- **Invariants** — what must remain true and what enforces it.
- **Failure/debugging** — predict a failure; first useful diagnostic steps.
- **Operations** — observable signals, consumers, blast radius, recovery.

Outcomes: **defensible** — solid across the required dimensions from cold/pre-correction evidence (solid cold baseline + transfer in-session, or a delayed checkpoint); **partial** — solid on some required dimensions; **practiced** — the session was learning-heavy (substantial correction needed): schedule a checkpoint at +7 days; **not-assessed** — untouched (never downgrade to this).

Degradation by environment: tests unavailable → executable dimensions are `not-tested`. Code unavailable (e.g. travelling) → recall-only checkpoint: a pass records "memory check passed; code-currentness unknown" and cannot renew full `defensible`.

## Red flags — stop and fix

- You heard the user's answer before writing the rubric, or explained a file before they attempted it.
- Status upgraded from post-correction performance, or after a session of you lecturing.
- `defensible` awarded without a cold baseline or delayed check.
- A failed/assisted session refreshing approval dates (record it as a new event; never overwrite the historical pass).
- Flow-level evidence written as subsystem-wide status (the scope column exists for a reason).
- Covering more than one subsystem "since we're on a roll".
- The closing summary written by you instead of the user.
- Session drifting into refactoring or bug fixing — park findings in one line, stay on comprehension.

Match the conversation's language (the map's display vocabulary may be localized; keep its tokens consistent within a wiki).
