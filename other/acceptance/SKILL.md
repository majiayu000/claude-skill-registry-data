---
name: acceptance
description: "Plan, execute, or review Mikka acceptance evidence before a PR or batch merge; use separate runner and checker roles."
---

# Mikka acceptance

Read `.agents/acceptance/PROCESS.md` for the two plan reviews, execution handoff,
and final `pass` / `fail` / `uncertain` verdict. Read
`.agents/acceptance/PROJECT.md` for actual commands, isolated identities,
fake boundaries, and device/E2B evidence.

Name separate runner and checker agents. As runner, operate the environment
and provide the accepted plans plus source-bound evidence. As checker, review
the scope plan, executable plan, and final evidence without performing the
execution or changing its implementation. Missing `requiredEvidence` is
`uncertain`, never a pass.

Use `.agents/acceptance/common-mistakes.md` for demonstrated integration
lessons and `.agents/acceptance/probe-mock-patterns.md` when choosing a probe
or fake. Publish the final evidence and independent verdict in the PR's
`Acceptance` section, reusing still-applicable results through their Git/CI
association.
