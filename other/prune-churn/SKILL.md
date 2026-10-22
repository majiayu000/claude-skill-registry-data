---
name: prune-churn
description: Find and remove change-amplifying tests, docs and structure — anything that must be edited whenever something else changes (mock-echo tests, broad snapshots, copy-asserting e2e, inventory docs, file/line references, hand-synced registries). Optional scope arg — diff (default), touched, branch, repo, or a path.
argument-hint: "[diff|touched|branch|repo|<path>]"
arguments: scope
---

One question decides every finding: **when something else in the repo changes, does this have to change too, without catching a bug or telling a reader anything they couldn't get from the source of truth?** If yes, it is churn. A change that touches one behaviour should touch the code for that behaviour, its tests, and little else.

This is about coupling, not verbosity. Comments and docstrings are out of scope, coupled ones included: `prune-comments` handles them.

## Scope

`$scope` selects what's in range (default `diff` when empty):

- `diff` (default) — what the uncommitted change added or modified: `git diff HEAD` plus untracked files (`git ls-files --others --exclude-standard`).
- `touched` — whole files the diff touches.
- `branch` — everything changed on this branch vs the default branch.
- `repo` — the whole repository.
- a path — that file or directory only.

For `diff`/`branch`, edit only added or changed hunks. Never touch gitignored, generated, vendored or lock files.

## What gets edited and what gets reported

| Area                                                          | Reference                 | `diff` / `touched`              | `branch` / `repo` / path |
| ------------------------------------------------------------- | ------------------------- | ------------------------------- | ------------------------ |
| Tests                                                         | `references/tests.md`     | edit                            | edit                     |
| Prose docs, agent instruction files                           | `references/docs.md`      | edit                            | edit                     |
| Code structure (duplication, registries, indirection)         | `references/structure.md` | fix what this change introduced | report                   |
| Repo and process (generated files, layout, session artifacts) | `references/repo.md`      | fix what this change introduced | report                   |

Each reference marks some findings report-only regardless of this table (cross-file duplicates, weakened tests, migrations); the reference wins. Structure and repo findings are design calls — consolidating code wrongly is its own churn — so outside a fresh change they are reported with evidence, never refactored.

## Guardrails

- **Deleting a test must not lose coverage of production code.** Delete only tests that exercise no production logic (mock-echo, tautological, restating a constant). A deletion that would leave a production line uncovered is wrong: rewrite the test, or leave it and report. Without coverage tooling, each deletion's verdict names what else covers the code, or why there is nothing to cover.
- **Brittle-but-valuable tests are rewritten, not deleted**: assert the observable outcome, not the path to it.
- **Never introduce doc tooling** or new test dependencies; use what the repo has.
- **Don't trade churn for abstraction.** Two similar copies are cheaper than one wrong abstraction.
- Never stage or commit. Leave everything as working-tree changes.

## Procedure

1. Resolve scope and list the files. Set aside generated, vendored and lock files, and files matching `repo.md`'s session-artifact tells (those go to step 4 only). If tests are in scope and the repo has coverage tooling, record coverage of the production files they reach now, as the baseline.
2. For `branch`, `repo` or a directory, mine history first: `python3 <skill-dir>/scripts/cochange.py [--branch <default-branch>] [pathspec]`. It ranks files by _tag-along_ commits — commits where the file changed but nothing near it did. High-ranked tests and docs are where the churn lives; audit them first. Hub files (registries, barrels, inventories) surface here too and feed step 4. Open a few of the counted commits before citing a number.
3. **One subagent per unit**, concurrently, each given its unit and only the matching references:
   - a test file with its own snapshot/golden files → `tests.md`
   - all agent instruction files together (`AGENTS.md`, `CLAUDE.md`, rule files) → `docs.md`
   - any other Markdown or prose doc → `docs.md`

   Under ~5 files in `diff` scope, do it inline instead. Source files get no unit; step 4 covers them. With dozens of units (`repo` scope), batch tests and small docs by directory into about 10 units; keep top-ranked step-2 files as units of their own. Subagents may read and grep the whole repo but edit only their unit. Tell them explicitly never to `git add`, and to return one line per finding: `path:line  <deleted|rewritten|edited|report|route structure|route repo> (<why>)`.

4. Then, sequentially, one cross-file pass with `structure.md` and `repo.md` over the whole scope. Give it the step-2 output, every `route` verdict from step 3, the session artifacts set aside in step 1, and the user's original request if you have it (a knob or file the request asked for is never a finding). In `diff`/`touched` fix what the change introduced; otherwise report.
5. Tests and doc rows that step 4 names as covering only code it removed: delete them now. The coverage guardrail doesn't apply, since the production code is gone.
6. Verify: run the formatter, then the test suite (tests were edited, so this is not optional); with no test suite, the repo's own build, typecheck or eval, across every target or package the edits reach, not just the local one. Then the coverage comparison against the step-1 baseline when tests were deleted. A test that newly fails means an edit was wrong; revert that edit, never the test. Tests removed in step 5 are exempt.
7. Print the edit verdicts, one line each (e.g. `deleted (mock-echo, no production lines covered)`, `rewritten (snapshot → 3 targeted assertions)`, `list → pointer to --help`). Then a **Report** section with every report and route finding from any step: sites, tag-along numbers when mined, the suggested shape. Frame each one as coupling to remove, with any drift as its evidence, not as a bug in one site; findings without evidence go in a one-line **Considered, low** list (`structure.md`, Report shape). Then any content moved out of deleted session artifacts, for the PR description. End with `review: git diff`, and suggest `prune-comments` on the same scope for comments.
