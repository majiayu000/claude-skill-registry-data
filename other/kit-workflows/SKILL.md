---
name: kit-workflows
description: >-
  Portable playbooks for a bug fix, a named-data-shape feature, or a
  behavior-preserving refactor. Apply when the user asks to reproduce and
  fix a defect, ship a small feature, or reshape code without changing
  behavior. Use unmatched-workflow when no playbook fits. Use deep-deliberation
  for a consequential design fork. Use dissect for an existing-system audit.
user-invocable: true
disable-model-invocation: false
version: "1.1.0"
author: "Ali Farahat"
tags: ["playbook", "bug-fix", "feature", "refactor"]
when_to_use: |
  USE WHEN:
  - The user wants a bug reproduced and fixed, a small feature shipped, or
    a behavior-preserving refactor.
  DO NOT USE WHEN:
  - No playbook fits (use unmatched-workflow).
  - The work is an existing-system audit (use dissect).
---

# Kit workflows

> **Leading words:** match a playbook, copy steps, skip with reason, prove
> on the real path.

Not a sticky mode. Match the task to one playbook. Copy that file's steps
into the todo list verbatim. Skipped steps stay with `skip:` / `n/a:`.

| Playbook | When |
|---|---|
| [playbooks/bug-fix.md](playbooks/bug-fix.md) | A defect: reproduce, root-cause, fix with evidence |
| [playbooks/feature.md](playbooks/feature.md) | New or changed behavior from a named data shape |
| [playbooks/refactor.md](playbooks/refactor.md) | Behavior-preserving reshape |

If none match, stop and use `unmatched-workflow`.

## Reply contract

First line: `Playbook: bug-fix`, `Playbook: feature`, or `Playbook: refactor`.
Then what was verified, and any `skip:` lines.
