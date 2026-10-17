---
name: apply
description: Canonical apply — pick from N options, validate before apply, or delete safely in one command
argument-hint: "[choose|validate|delete] [context-or-options]"
related:
  - ask-me
  - rethink
  - follow-your-suggestion
  - report
  - report-progress
  - suggest-next-action
  - manage
  - deep-validate
  - run-check
  - check-reference
  - review-devin-global-harness
  - update-references
  - scan-codebase
  - resolve-errors
  - all-this-patterns
  - continue
  - delete-cicd-fails
  - delete-git-branch
  - delete-git-submodules
  - delete-git-worktree
  - delete-projects
  - delete-project-temp
---

## Goal

Apply actions correctly and safely — the canonical skill for every apply pattern — merged from the former `choose-and-apply`, `validate-then-apply`, and `delete`

## Scope

- `choose`: several alternatives (tools, libraries, approaches) → analyze → pick → apply
- `validate`: confirm before applying — code, config, references, architecture, or a decision
- `delete`: delete files/folders safely — dry-run, confirm, backup, update references
- No mode given → detect from context/argument, then `/ask-me` if still unclear

For domain-specific deletes, call the skill directly: `/delete-cicd-fails`, `/delete-git-branch`, `/delete-git-submodules`, `/delete-git-worktree`, `/delete-projects`, `/delete-project-temp` — each skill has its own dry-run + confirm gate

## Execute

### 0. Detect Mode

> Goal: Pick the workflow that fits the context

1. argument/context specifies a mode → use that mode
2. Several options to choose from → `choose`
3. Deleting files/folders → `delete`
4. A general apply that needs confirmation first → `validate`
5. Unclear → `/ask-me`

### Mode: Choose

> Goal: Pick the best of N options and apply it

1. **Capture options** — take them from argument/context; none → `/ask-me`; a single option → `/follow-your-suggestion`
2. **Analyze** — assess scope, cost, effort, risk, compatibility, maintainability; close options/high trade-offs → `/rethink`
3. **Present and confirm** — `/report table` with columns `No. | Option | Pros | Cons | Score | Recommended`; mark the recommendation with `✅`; high-risk → `/ask-me` first
4. **Apply** — continuing from context → `/follow-your-suggestion`; a single action → `/continue`; multiple steps → `/manage`; affects many places → `/all-this-patterns`
5. **Validate and report** — `/run-check` or `/deep-validate` as appropriate → `/report table` (`No. | Option | Status | Output`) → `/suggest-next-action`

### Mode: Validate

> Goal: Always check before applying — never apply until the criteria pass

1. **Capture context** — take the action/context; unclear → `/ask-me`; define scope, dependencies, expected outcome
2. **Select validation** — code → `/run-check`; skill/rules/config → `/deep-validate`; reference/path → `/check-reference` or `/review-devin-global-harness`; architecture/design → the fitting `/review`; decision → `/rethink`
3. **Run validation** — record passed/failed, findings, warnings; order by severity; `/report table` (`No. | Check | Status | Findings`)
4. **Decide** — all pass → apply; low warnings → notify the user and apply once confirmed; error/blocker → fix until it passes; unsure → `/ask-me`
5. **Apply** — suggestion-only → `/follow-your-suggestion`; file ops in many places → `/all-this-patterns`; multiple steps → `/manage`
6. **Re-validate and report** — validate again after applying → `/report table` (`No. | Step | Validation | Apply | Status`); stuck step → `/report-progress` → `/suggest-next-action`

### Mode: Delete

> Goal: Delete safely — dry-run + confirm + backup + update references

1. **Identify targets** — take the list from the user; expand pattern/glob into concrete files; record absolute paths
2. **Assess impact** — `/report` summarizes the state; `/scan-codebase` or `/use-astgrep` to find references; check `git status` for tracked/untracked; identify broken refs; many/important references → `/ask-me` first
3. **Dry run** — show the deletion list + refs that would break + total size → ask `proceed`/`skip`/`cancel`
4. **Backup** — under git → recoverable via git, no backup needed; not in git/uncommitted → copy to `%TEMP%` or `.trash/` and record the path
5. **Delete** — `Remove-Item`/`rm`; directory → recursive once confirmed; important targets (config, keys) → double confirm; deletion fails → report the error and stop
6. **Update references** — `/update-references` fixes/removes refs pointing at the targets; `/review-devin-global-harness` checks for broken refs (fix up to 3 rounds)
7. **Validate** — confirm the deletion actually happened; `/run-check`; `/review-devin-global-harness` again; fails → `/resolve-errors` then retry
8. **Report** — deleted list + fixed refs + remaining broken refs → `/suggest-next-action`

## Rules

### 1. Confirmation Gates

- Never apply without confirmation when high-risk
- Delete: always dry-run + confirm; never delete outside scope, git history, or `.git`
- Never apply while validation blockers remain — don't skip them because the user is in a hurry

### 2. Evidence And Context

- Every option must be evaluated against the real context — no guessing
- Keep the original context throughout the apply
- Keep validation results in the report before and after applying

### 3. Safety First (Delete)

- Never delete files containing secrets, API keys, or credentials
- Target in global config (`~/.config`, `%APPDATA%`) → double confirm
- Target in use by another process → stop the process first
- Target not in git → back it up before deleting and record the backup path in the report

### 4. No Broken References

- Every broken reference must be updated or deleted
- Never leave imports, paths, or links broken

## Expected Outcome

- Mode detected/selected correctly from context
- Choose: full comparison table + recommended option with reasons + apply succeeds
- Validate: check before every apply + no apply with blockers + complete report
- Delete: targets removed + no broken refs + passes `/run-check` + rollback possible if backed up
- Next action known for every mode
