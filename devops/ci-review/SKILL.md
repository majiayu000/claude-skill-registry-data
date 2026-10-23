---
name: ci-review
description: Audit CI workflow design and effectiveness without modifying it. Use when triggers, jobs, commands, quality gates, caches, artifacts, matrices, permissions, release paths, or deployment automation may be stale, redundant, unsafe, or unjustified.
---

# CI Review

Show which CI components protect a real contract, and which are stale, redundant, unsafe, or ineffective.

## Workflow

1. Confirm the repository, the comparison target if there is one, the supported platforms, and the checks required for merge.
2. Map the triggers, jobs, called commands, environments, token permissions, secrets, caches, artifacts, release paths, deployment paths, and required checks. Note each trigger that runs code from forks or untrusted contributors, and the secrets and permissions that code receives.
3. For each component, name its consumer and the contract it enforces. Read the repository, and, when the host allows it, bounded read-only run history such as `gh run list --workflow <file> --limit 20`, to see whether a check actually runs, fails, or is skipped.
4. Look for duplicated logic, mismatched tool versions, path filters that skip required checks, unused matrix entries, ignored results such as `continue-on-error` or `|| true`, retries that hide flaky tests, dead paths, permissions broader than the job needs, third-party actions referenced by a mutable tag or branch, and caches or artifacts that nothing reads.
5. Classify each actionable item as `keep`, `simplify`, `merge`, `fix`, `remove`, or `owner decision`.
6. Delegate tool provenance to `dependency-review`, exploit paths to `security-review`, infrastructure semantics to `infra-review`, runtime readiness to `rollout-readiness-review`, and test sufficiency to `test-gap-review`.

Do not edit workflows, rerun jobs, or change repository settings. Do not remove a safety gate on speculation, recommend scanners for appearance, or propose a broad rewrite.

## Result

For each finding, report the location, the affected contract, the evidence, the consequence, the recommended disposition, the risk of making the change, and how to verify it. Order findings by consequence. State the scope, the evidence limits, and the smallest sequence of cleanup steps, or state that nothing is actionable. Recommendations do not authorize implementation.
