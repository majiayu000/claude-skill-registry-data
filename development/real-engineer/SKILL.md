---
name: real-engineer
description: "A Codex workflow router for disciplined software engineering: diagnose bugs, run TDD, clarify requirements, build throwaway prototypes, and review architecture. Use when the user asks for serious engineering help and no narrower app in the collection fits. Do not use for routine shell questions, simple explanations, document/image/spreadsheet work, PR review, issue triage, release prep, docs sync, security review, performance work, frontend polish, migrations, or repo onboarding when a more specific skill applies."
---

# Real Engineer

Choose exactly one primary mode, then work the request through that mode. This
app is the general engineering fallback in the Coolest Codex Apps collection, so
avoid stacking multiple modes unless the work naturally transitions from one to
another.

## Routing

| User intent | Mode | First move |
| --- | --- | --- |
| Broken, failing, flaky, slow, regression, crash | Diagnose | Build a reproducible pass/fail loop |
| Explicit TDD, test-first, red/green/refactor | TDD | Write one failing behavior test |
| Fuzzy feature, plan, product behavior, design tradeoff | Grill | Ask one concrete question with a recommendation |
| "Prototype", "mock up", "try variants", state-model sanity check | Prototype | State the question the prototype answers |
| Architecture, refactor opportunities, coupling, maintainability | Architecture | Map modules and find friction |

Precedence rules:

- If something is broken, use Diagnose before TDD. Add the regression test after
  the cause is understood.
- If implementation is blocked by unclear behavior, use Grill before TDD.
- If the user wants to compare possibilities before committing, use Prototype
  before production implementation.
- If the user asks for repo-wide structure, use Architecture before proposing
  code changes.

## Shared Discipline

- Prefer reading code, tests, docs, and errors before asking questions.
- Build a feedback loop before making risky changes.
- Work in small vertical slices.
- State assumptions when proceeding without user input.
- Keep durable decisions in the repo's existing docs only when that matches the
  repo's conventions.
- Finish with what changed, how it was verified, and what risk remains.

## Diagnose Mode

Debug by proving the failure before fixing it.

1. Build a fast pass/fail loop: failing test, focused CLI command, HTTP script,
   browser automation, replayed fixture, harness, fuzz loop, differential check,
   or bisection.
2. Reproduce the user's exact symptom.
3. Rank 3-5 falsifiable hypotheses for nontrivial bugs.
4. Probe one variable at a time. Tag temporary logs with a unique prefix such as
   `[DEBUG-a4f2]`.
5. Fix with regression coverage when a correct test seam exists.
6. Re-run the original loop, remove temporary instrumentation, and summarize the
   actual cause.

Do not proceed without a feedback loop unless you explicitly explain what you
tried and what artifact is needed.

## TDD Mode

Implement through red/green/refactor.

1. Identify the public behavior and existing test style.
2. Write one failing test for one behavior.
3. Implement only enough code to pass that test.
4. Repeat for the next behavior.
5. Refactor only after green, running tests after each meaningful change.

Good tests verify observable behavior through public interfaces. Avoid tests
that lock onto private methods, call order, or internal shape.

## Grill Mode

Clarify the work until implementation choices are grounded.

1. Read existing code/docs first when they can answer the question.
2. Name the uncertainty and why it matters.
3. Ask one useful question at a time, with a recommended answer.
4. Resolve user outcome, domain terms, constraints, data ownership, edge cases,
   failure modes, rollout, and verification.
5. Finish with an implementation-ready brief.

For small obvious edits, proceed with a stated assumption instead of turning the
task into an interview.

## Prototype Mode

A prototype answers one question with disposable code.

1. Pick the shape:
   - Logic/state question: tiny runnable script, terminal app, or harness.
   - UI question: 2-4 structurally different variants in a realistic route.
2. Mark prototype files/routes/comments with `PROTOTYPE`.
3. Keep state in memory unless persistence is the thing being tested.
4. Avoid destructive real mutations.
5. Capture the answer, then delete or fold the winning idea into production.

## Architecture Mode

Find refactors that improve locality and leverage.

Vocabulary:

- Module: code with an interface and implementation.
- Interface: everything callers must know, including invariants and errors.
- Deep module: small interface, substantial useful behavior.
- Shallow module: interface nearly as complex as implementation.
- Seam: a place behavior can vary without editing callers.
- Locality: related change, knowledge, and bugs stay in one place.
- Leverage: callers get more behavior while knowing less.

Process:

1. Read project docs, tests, module boundaries, `AGENTS.md`, `CONTEXT.md`,
   `docs/adr/`, or equivalents.
2. Look for pass-through wrappers, duplicated orchestration, hidden coupling,
   hard-to-test behavior, and concepts scattered across many files.
3. Apply the deletion test: if deleting a module makes complexity vanish, it was
   probably shallow; if complexity spreads across callers, it was earning its
   keep.
4. Present candidates with files, friction, direction, benefits, test impact,
   and confidence: `Strong`, `Worth exploring`, or `Speculative`.
5. Ask which candidate to pursue before designing detailed interfaces unless the
   user explicitly requested an implementation plan.
