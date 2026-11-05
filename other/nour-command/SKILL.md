---
name: nour-command
description: Use for any non-trivial Nour task that needs context recovery, end-to-end execution, MAX EFFORT, backlog reconciliation, deep research, audit-and-fix work, or proof-backed completion. Also use when Nour says continue, finish it, figure out what is left, reconcile sessions, audit and fix, deep research, or NOUR COMMAND.
triggers: context recovery, end-to-end execution, max effort, backlog reconciliation, deep research, audit and fix, proof-backed completion, continue, finish it, what is left, reconcile sessions, nour command
---

# NOUR COMMAND

This skill is a router, not a second policy.

1. Read `../../../AGENTS.md`; it is the engineering/safety authority.
2. Read `../../../NOUR-COMMAND.md`; apply its execution framework.
3. If the task is non-trivial, read only the relevant entries in
   `../../../docs/agent-os/NOUR-COMMAND-MODES.md`.
4. Load the nearest app `AGENTS.md` before editing app code.
5. Invoke any narrower repo skill whose trigger applies; this router does not replace domain skills.
6. Define the task-specific completion contract before consequential execution.
7. Recover context before asking Nour to repeat prior work.
8. Verify current remote/production truth before trusting a prior session, plan, or local checkout.
9. Prefer finish/wire/repair/consolidate/adopt/delete before adding another implementation.
10. Execute in dependency order and run authorized work to empty.
11. Try to falsify apparent success before declaring completion.
12. Simplify after a successful change and turn material failures into regression protection.
13. Report demonstrated outcomes, exact proof, real remaining work, and exact blockers.

When `AGENTS.md` or an app-specific instruction conflicts with this skill, the canonical policy wins.

For Claude, `NOUR-COMMAND.md` is imported by root `CLAUDE.md`, so the main framework is already in context.
This skill exists to make the mode-router invocation explicit and to force loading only the relevant deep-mode details.
