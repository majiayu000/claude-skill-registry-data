---
name: finalize-pr
description: Perform final pre-review verification for an existing PR without merging it.
argument-hint: "[pr-number]"
disable-model-invocation: true
---

Finalize PR $0 for review.

Check:
- `AGENTS.md` and the linked Issue acceptance criteria
- PR scope and diff
- focused-test evidence
- required Ruff checks and `git diff --check`
- Issue linkage and PR description
- current CI status
- unresolved review findings

Do not add speculative improvements and do not merge. If all required conditions are met, conclude `Ready for review.`
