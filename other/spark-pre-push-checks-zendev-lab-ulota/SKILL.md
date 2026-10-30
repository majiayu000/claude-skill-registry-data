---
name: spark-pre-push-checks
description: Use when a Spark branch or pull request needs final diff hygiene, validation selection, commit scope, remote topology, and readiness checked before publication.
---

# Spark pre-push checks

Treat repository and remote state as evidence. The upstream Session retains publication authority.

## Procedure

1. Read `CONTRIBUTING.md`, the validation matrix, PR template, and applicable subtree instructions.
2. Inspect status, staged and unstaged diffs, commit range, generated output, secrets, runtime state, and unrelated edits.
3. Map changed owners to focused tests, static checks, documentation checks, and compatibility gates. Run missing non-publishing checks when authorized.
4. Compare every acceptance criterion with concrete code or command evidence.
5. For an existing PR or stack, read back exact head/base SHAs, topology, mergeability, and current checks. Mark pending checks as pending.

Never push, force-push, create, ready, merge, or close a PR. Never claim a check passed from an old SHA. Reject when intended commit scope is ambiguous or required evidence is absent.

Return `diffScope`, `commands`, `acceptanceEvidence`, `remoteState`, `pending`, `verdict`, and `blockingReasons`.
