---
name: hoa-repo-reckoning
description: >-
  Explicit shortcut for a read-only review of one whole repository: find work
  that should stop and overlooked facts that would change the work. Not for a
  diff, PR, or skill catalog audit.
disable-model-invocation: true
metadata:
  revision: "3"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "explicit shortcut for a read-only repository review: what should stop and what the owner needs to know"
  summary_zh: "仅显式调用的只读仓库审查提示词：哪些事该停止，哪些未知会改变工作"
  kind: "entry"
  produces: "repository-reckoning-report"
---

# hoa-repo-reckoning

The repository path is required; ask for it if missing. Read the subject's
`AGENTS.md` and `CLAUDE.md` first, if present. Never edit the subject.

Deep-review the whole repository's practices and machinery. Find what it costs
its owner that nobody notices any more (things still being done that should
stop), and what the owner does not know that would change the work. Rank the
findings and give each a severity and the evidence.

Use read-only `gh`, web search, and host/runtime inventory when available and
permitted. Mark each unused capability `not run` and explain the coverage gap.

Write the free-form report to the user-supplied path outside the subject.
If no path is supplied or the path is inside the subject, reply inline.
