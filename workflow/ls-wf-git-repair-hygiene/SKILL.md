---
name: ls-wf-git-repair-hygiene
description: Use when recovering broken Git state and enforcing follow-up workflow hygiene checks.
metadata:
  version: "1.0"
---

Use this pipeline package for broken Git state recovery plus compliance hardening.
Use `ls-git-broken-state-recovery` for repair, then `ls-git-merge-rebase` and
`ls-localsetup-framework-changes` for Git hygiene and compliance checks. These skills own
the procedures; use [Git traceability](../../docs/GIT_TRACEABILITY.md) for
immutable artifact references.
