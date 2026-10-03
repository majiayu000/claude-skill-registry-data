---
name: issue-sherpa
description: Triage GitHub issues, bug reports, feature requests, and vague tasks into reproducible, scoped engineering work. Use when Codex needs to classify an issue, extract acceptance criteria, propose labels, draft a maintainer reply, or turn an issue into an implementation plan. Do not use for reviewing already-written PR diffs or publishing comments unless the user asks.
---

# Issue Sherpa

Turn fuzzy issue text into work a maintainer can trust.

## Workflow

1. Read the issue, linked discussion, screenshots, logs, and relevant repo docs.
2. Classify the request: `bug`, `feature`, `docs`, `maintenance`, `question`, or `needs reproduction`.
3. Extract facts separately from assumptions.
4. Build a reproduction or discovery plan for bugs. If a repro is impossible, name the missing artifact.
5. Write acceptance criteria as observable outcomes.
6. Propose the smallest useful implementation slice and verification command.

## Draft Maintainer Reply

When asked to reply, produce a draft unless the user explicitly asks to post it.
Include:

- Summary of the issue in one sentence.
- What is known.
- What is needed, if anything.
- Next action and verification.

## Triage Checklist

- Environment/version present?
- Expected and actual behavior distinct?
- Reproduction steps concrete?
- Logs or screenshots actionable?
- Duplicates or related issues checked?
- User impact and severity clear?
- Scope small enough for one PR?

## Output

Prefer:

```text
Classification:
Impact:
Repro plan:
Acceptance criteria:
Implementation slice:
Verification:
Suggested labels:
Draft reply:
```
