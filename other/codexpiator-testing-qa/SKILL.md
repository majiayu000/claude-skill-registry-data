---
name: codexpiator-testing-qa
description: General testing strategy and quality gates - testing pyramid, TDD workflow, mocking and test data, and CI quality gates. Use whenever following TDD, deciding what test level to use, or deciding what should block a merge (for frontend-specific test scope, see codexpiator-frontend/frontend-testing.md).
---

# Codexpiator Testing & QA

Single-purpose reference files for testing strategy and discipline.

| File | Read this when... |
|---|---|
| `testing-pyramid-and-strategy.md` | Deciding what level to test something at, avoiding a flaky/slow suite |
| `tdd-workflow.md` | Following red-green-refactor while building a feature |
| `mocking-and-test-data.md` | What to mock, test data setup, avoiding over-mocking |
| `ci-quality-gates.md` | What should block a merge vs. only warn (pipeline structure itself: `codexpiator-devops/ci-cd-pipelines.md`) |

## Non-negotiable baseline (applies everywhere in Codexpiator)

Every piece of frontend or backend work created or changed gets real
tests — written, run, and passing — covering edge cases and not just
the happy path, with the *full* suite run before the work is
considered done. Security-relevant behavior gets tested as explicit
attack-attempt cases, not just functional ones (see
`codexpiator-security/security-testing.md`). This isn't a suggestion
for especially important code — it's the default for anything
created. `codexpiator-frontend/SKILL.md` and
`codexpiator-backend/SKILL.md` both restate this as a mandatory
pre-completion gate; this skill is where the discipline and detail
live.

## Ask when useful; suggest an audit after significant work

See `shared/collaboration-and-audit-practice.md` — ask a targeted
clarifying question (via `AskUserQuestion` when available) when a
testing trade-off genuinely needs the user's input, and suggest
`/codexpiator-audit` after a significant batch of work.
