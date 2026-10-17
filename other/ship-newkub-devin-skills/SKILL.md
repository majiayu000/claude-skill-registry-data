---
name: ship
description: Canonical ship — verify gate (review, validate, tests, dev, usage), push, PR gate, merge main
argument-hint: "[scope] [verify-only|run|@issue-number-or-title|dont-ask-me]"
triggers:
  - user
  - model
related:
  - follow-agents-md
  - update-agents-md
  - deep-review-codebase
  - deep-review-codebase-then-fix
  - deep-validate
  - update-tests
  - run-test
  - run-dev
  - git-commit-and-push
  - create-github-pr
  - review-github-pr
  - merge-all-branch-by-me-to-main
  - resolve-merge-conflicts
  - release-new-version
  - watch-browser
  - resolve-errors
  - resolve-cicd
  - suggest-next-action
  - report
  - refactor
  - update-project
  - improve
  - optimize
  - dont-ask-me
---

## Goal

The single ship command — run every verification gate first, then commit/push, pass the PR review gate, and merge into `main` only when everything is genuinely green

## Scope

- Use as the final ship path for any work — verify, push, PR gate, and merge into `main` in one skill
- `verify-only` argument → run steps 1–6 and report readiness only — no push, no merge
- `run` argument → after verify, run step 6 (sync project), then keep the dev server running for real use (merged `/ship-run`) — no push, no merge
- The canonical home of every verify step — other skills (e.g. `/update-agents-md`, `/new-skills`) reference here; never duplicate the verify workflow
- Releasing a new version → `/release-new-version`
- `dont-ask-me` argument or a session with `/dont-ask-me` active → confirmation gates are replaced by `/follow-your-suggestion` + safe defaults

## Execute

### 1. Follow AGENTS.md

> Goal: `AGENTS.md` is fresh and the source of truth before verify

1. Run `/follow-agents-md` — if `AGENTS.md` is missing or stale → always run `/update-agents-md` first
2. Read any additional ship/validate rules the project's `AGENTS.md` defines

### 2. Review Changes

> Goal: changes and `AGENTS.md` pass review before ship

1. Run `/deep-review-codebase` on the changed scope + `AGENTS.md` only
2. If there are findings → run `/deep-review-codebase-then-fix` until they all pass
3. Add `/review-devin-global-harness` when changing the devin skills repo

### 3. Validate

> Goal: correctness passes on every dimension

1. Run `/deep-validate` — cross-reference, type safety, conventions
2. Run the project's lint + typecheck (via `/run-check`) — they must pass

### 4. Tests

> Goal: tests are complete and genuinely passing

1. Run `/update-tests` — test specs cover every layer of the changes
2. Run `/run-test all` — all suites must pass; on failure → fix the root cause and rerun

### 5. Runtime And Usage

> Goal: the app really runs and the docs match reality

1. Run `/run-dev` — the dev server must be healthy with no errors
2. Run `/deep-test usage` — usage examples from README/docs/`AGENTS.md` must actually work
3. `run` argument → leave the `/run-dev` server up, not just the health check: web project → open the browser at the dev URL and continue `/watch-browser fix` per the `/run-dev` workflow; errors found while watching → `/resolve-errors` immediately — then run step 6 (sync project), stop with the report (steps 7–10 never run)

### 6. Update Project

> Goal: sync docs, config, rules, and tooling with the verified changes before push

1. Run `/update-project` — reads git log, restores changed info into root `AGENTS.md`, `README.md`, syncs config, `.devin/`, rules, GitHub metadata, and all project files to match the current codebase
2. The sync must reflect reality: no stale docs, no missing config entries, no orphan references

### 7. Commit And Push

> Goal: validated + synced work is on the remote with green CI

1. If verification failed at any gate → fix the blockers and verify again — never skip ahead to push
2. Run `/git-commit-and-push` — commit changes + push the working branch + resolve CI/CD until green (`verify-only`/`run` → stop after step 6 with the report — steps 7–9 never run)

### 8. PR Review Gate

> Goal: the → `main` PR passes review + all checks before merge

1. Create/find the PR into `main` with `/create-github-pr` (if none exists)
2. Run `/review-github-pr` — full gate: all CI checks pass + `/deep-validate` + `/deep-review-codebase` + PR metadata/diff clean
3. If the gate fails → fix the findings on the branch, re-run `/git-commit-and-push` — never merge

### 9. Merge To Main

> Goal: merge into main + cleanup branches

1. User confirmation before merging into `main` (except `dont-ask-me` → safe default)
2. Run `/merge-all-branch-by-me-to-main` — merge user branches into `main` + cleanup
3. If conflicts → `/resolve-merge-conflicts`; if complex → `/ask-me`
4. `git switch main` + `git pull` — verify the merge succeeded and remote main has the new commits

### 10. Report

> Goal: summarize the ship result — merged or blocked

1. Run `/report` — table: `No. | Gate | Result | Evidence` + verdict `merged`/`blocked` (+ dev server status — URL, port, watch state — when the `run` argument was used)
2. If a release is needed → suggest `/release-new-version`
3. Run `/suggest-next-action`

## Rules

- Every gate must genuinely pass — never skip a failing gate; fix loop up to 3 rounds, then stop + report
- Skip a non-applicable gate only when the project truly lacks that artifact (e.g. no dev server → skip `/run-dev`) — state the reason in the report
- Never duplicate verify steps in other skills — reference `/ship` only
- Use `/deep-test smoke` as a post-build sanity gate on critical paths
- Never push work that failed verification; never merge while CI is failing/pending or the PR review has blockers
- Merging into `main` → always user-confirmed (except `dont-ask-me` mode)
- Never force-push `main` — roll back with `git revert` only
- `dont-ask-me` mode: no `ask_user_question`, no `/ask-me`; irreversible actions → safe default or stop+report

## Expected Outcome

- `AGENTS.md` fresh, review/validate/check passed, tests green, dev run works, usage matches reality
- Code pushed to remote with green CI/CD, PR review gate passed (checks + deep-validate + deep-review-codebase)
- Branches merged into `main` successfully + cleanup done, with a rollback path
- A clear report with the verdict and the next action (`/release-new-version` if a release is needed)
