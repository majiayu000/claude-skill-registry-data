---
name: engineering-workflow
description: "Parent workflow: understand, inspect repo, requirements, research, design, plan, implement thin slices, test, review, secure, document, verify, ship. Scale depth to change size."
---

# engineering-workflow

Match ceremony to stakes: typo → inspect/edit/test; endpoint → design/implement/review; auth system → threat-model/design/security-tests/review; architectural change → mapping/research/ADR/migration/review.

## Activate when

- Any non-trivial change; always the entry point that routes to sub-skills.

## Do NOT activate for

- Single-step questions answerable by one specialized skill — go direct.

## Procedure

1. Understand the request; inspect the repository (`../repository-understanding/`) before changing anything.
2. Clarify requirements (`../requirements-analysis/`); research unknowns (`../../research/documentation-search/` with version detection).
3. Design, then plan small atomic tasks (`../planning/`).
4. Implement thin vertical slices (`../implementation/`); test as proof (`../testing/`).
5. Review the diff (`../code-review/`), security-review significant changes (`../../security/secure-baseline/`), document decisions (`../documentation/`).
6. Verify with evidence (tests, builds, runtime output) — never claim success without it — then ship (`../../git/git-release/`).
