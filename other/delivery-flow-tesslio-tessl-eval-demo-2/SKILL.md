---
name: delivery-flow
description: "Use when an engineering task must be carried to a verified, reviewed, PR-ready local change: an approved ticket or requirements, a feature, or a bug fix, including a failing test, a crash, or a bug a user reported."
---

# Delivery Flow Router

Route one approved engineering task through the installed delivery skills. This router selects and sequences specialists; it does not replace their instructions.

## Required stage loading

Before acting on a stage, load the named skill through the agent's skill mechanism and follow its full instructions. Mentioning a skill or paraphrasing it is not equivalent to loading it. Do not continue using only this router when a stage skill is available.

1. Load `writing-plans` when the task spans multiple meaningful implementation units. For a narrow task, record a concise working plan instead.
2. Load `executing-plans` when working from a written plan, and load `test-driven-development` before implementing any behavior change or bug fix.
3. Load `systematic-debugging` before fixing any defect: a failing test, a crash or error, a reported bug, or wrong behavior, even when the cause looks clear from the code.
4. Load `verification-before-completion` before claiming completion or recording final verification evidence.
5. Load `requesting-code-review` for a requirements-driven review of the final diff. If it returns valid findings, load `receiving-code-review`, address them, and return to verification.
6. Load `finishing-a-development-branch` only when the user explicitly asks to integrate, push, or create a pull request. Otherwise leave a reviewed, PR-ready local change.

## Routing contract

- Treat supplied acceptance criteria as authorization for the local implementation. Pause only for a missing decision that materially changes scope, behavior, or safety.
- Preserve repository instructions and existing conventions, and keep unrelated changes out of the diff.
- Continue between ordinary stages without asking the user to choose a process.
- Never push, merge, open a pull request, or delete a worktree without explicit authorization.
- Retain observable evidence for planning, red/green testing, verification, review, and any review fixes.
- For explanation-only requests, describe the routed sequence without claiming that unperformed work occurred.
