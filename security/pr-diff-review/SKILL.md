---
name: pr-diff-review
description: Review an authorized pull request diff for security regressions. Use when changes modify trust boundaries, auth logic, data-access scope, file handling, logging, headers, or secrets.
---

# PR Diff Review

## Method

- isolate what changed
- identify new or weakened trust boundaries
- flag only issues introduced or materially affected by the diff
- note rollout risk and required follow-up tests

## Output

Keep findings tightly scoped to the diff and call out blocking vs non-blocking issues.
