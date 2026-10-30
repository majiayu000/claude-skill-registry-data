---
name: requirements-to-issues
description: Turn a new or changed lab requirement into a GitHub Issue with dependencies, acceptance criteria and expected evidence. Use when docs/requirements.md gains a row or a requirement changes.
---

# requirements-to-issues

## Inputs
- Requirement ID and row in `docs/requirements.md`; source section in `docs/source/README_PAD.md`.
- Status code: О (assignment), П (teacher), Р (recommendation), Н (our decision).

## Steps
1. Quote the source wording; keep the status code — never upgrade Р/Н to О.
2. Check for an existing Issue: `gh issue list --search "<ID>" --state all`.
3. Write: goal, scope/non-scope, dependencies (other IDs/Issues), acceptance criteria that
   a command or file can verify, expected evidence (file, test, trace ID, table).
4. Create with `gh issue create --label <stage>` only if the current task allows GitHub writes.
5. Put the Issue number back into `docs/requirements.md`.

## Outputs
Issue URL (real, from `gh` output) or a ready-to-paste Markdown body if GitHub is not allowed.

## Boundaries
No fake Issue numbers. No lab 2/3 scope (microservices, k8s) in lab 1 Issues.
