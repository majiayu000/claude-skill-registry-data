---
name: code-review
description: >-
  Multi-axis review of diffs before merge. Use when reviewing a PR, branch, or
  local changes; when asking if a change is safe; or before marking code tasks
  complete. Do not use for CI babysitting loops or live incidents.
---

# Code Review

Review for correctness, readability, architecture fit, security, and performance. Approve when the change improves code health — not only when it is perfect.

## Workflow

1. **Context** — intent, acceptance criteria, `git diff <base>...HEAD` (three-dot).
2. **Tests first** — do tests exist, assert behavior, cover the risk?
3. **Five axes** — correctness, readability, architecture, security, performance. Details: `references/review-axes.md`.
4. **Contract surface** — does the diff touch anything consumed outside this repo (public APIs, endpoints, schemas, events, package exports)? If yes, apply the `contract-guard` skill: classify the change, require a compatibility strategy for breaking changes, demand contract evidence. An unflagged breaking change is always `Critical:`.
5. **Scope** — ticket-sized? refactor mixed with feature? secrets? verification story present?
6. **Severity labels** — `Critical:` / required / `Nit:` / `Optional:` / `FYI`.
7. **Verdict** — Approve | Request changes. List blockers only.

## Constraints

- Do not rubber-stamp. Do not bury Critical under nits.
- Prefer structural remedies (extract, reuse canonical helper, explicit types) over vague “make it cleaner”.
- Split advice: large mixed refactor+feature PRs should be split when review needs unrelated context.

## Verification

- [ ] Intent understood
- [ ] Tests reviewed for the change
- [ ] Findings severity-labeled
- [ ] Verdict + required follow-ups stated
