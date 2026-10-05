---
name: gha-failure-taxonomy
description: This skill should be used when the user mentions "github actions failing", "CI failure", "workflow failed", "actions permission denied", "secret not found", "matrix", "cache miss", "GITHUB_TOKEN", "pipeline red", or is diagnosing a red GitHub Actions run. It provides a taxonomy of failure classes with log signals, root causes, and exact YAML fixes.
---

# GitHub Actions Failure Taxonomy

## Purpose
A consistent way to classify a failing (or non-running) GitHub Actions workflow into one root-cause class, so triage goes straight from a log line to the exact YAML fix instead of trial-and-error re-runs. This is domain knowledge about how Actions actually breaks, not generic YAML advice.

## First split: did it FAIL or never RUN?
- **Never ran** (no run appears, or the job count is 0): almost always the `on:` trigger, `paths`/`paths-ignore`, `branches`/`tags` filter, or a `matrix` that expanded to nothing. Do not look for a step error.
- **Ran and failed**: anchor on the platform's error string, then classify below.

## Classification matrix

| Class | Fastest log signal | Root cause | Fix direction |
|-------|--------------------|-----------|---------------|
| Permissions / token scope | `Resource not accessible by integration`, HTTP 403 | `GITHUB_TOKEN` lacks a scope | add least-privilege `permissions:` |
| Missing / misnamed secret | `secret ... not found`, empty var, auth 401 | secret undefined, wrong name, or wrong scope (repo vs env) | define/rename secret; check environment |
| Matrix expansion | 0 jobs, or siblings cancelled | `matrix` typo or `fail-fast: true` | fix matrix keys; `fail-fast: false` |
| Cache miss | `Cache not found for input keys` | cache key drift / never saved | stabilize `key`, add `restore-keys` |
| Trigger mismatch | workflow absent from runs | `on:` / paths / branch filter | widen or correct the filter |
| Checkout depth | `shallow`, missing tags, `git describe` fails | default `fetch-depth: 1` | `fetch-depth: 0` |
| Concurrency cancellation | `Canceling since a higher priority` | `concurrency` with cancel | expected; scope the group |
| Runner / tool drift | `command not found`, version mismatch | runner image or tool changed | pin `setup-*` version / runner image |
| OIDC / cloud auth | `sts:AssumeRoleWithWebIdentity` denied | missing `id-token: write` or trust policy | add permission; fix cloud trust |
| Flaky / network | timeout, ECONNRESET, passes on re-run | external instability | retry/backoff, pin mirrors |

## Triage checklist
1. Read the failing workflow file; find the failing job/step by name.
2. Quote the exact error line, it is the classifier.
3. Map to one primary class (secondary classes noted separately).
4. Cite the offending `file:line`.
5. Give the minimal corrected YAML with just the changed keys.

## Additional Resources
### Reference Files
For the full symptom → cause → fix catalog across every class, consult:
- **`references/failure-catalog.md`**: each failure class expanded as log symptom → root cause → corrected YAML, covering permissions, secrets, matrix, caching, triggers, checkout depth, concurrency, runner/tool versions, and OIDC.

For the token and secret model in depth, consult:
- **`references/permissions-and-secrets.md`**: the `GITHUB_TOKEN` permission model, least-privilege `permissions:` blocks, OIDC vs long-lived secrets, environment protection rules, and how secrets get masked or leaked.
