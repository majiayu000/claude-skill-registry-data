---
name: kpa-finalize-change
description: Run the full finalization pipeline for a completed OpenSpec change - simplify, verify, review, sync, archive, fix, update docs, commit
argument-hint: "[change name]"
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Run the full finalization pipeline for a completed OpenSpec change. Execute each step in order, fixing issues as they arise. Stop early if a step has unfixable problems. If there are no unfixable problems, continue to the next step until all steps are complete.

## Steps

### Step 0: Simplify

If you are an Anthropic Claude Code agent, run the Claude Code `/simplify` command which acts as a kind of code review for the change.

### Step 1: Verify implementation

Run the `/opsx:verify` command against the active change. If verification finds CRITICAL or WARNING issues, attempt to fix them. Re-verify after fixes. If issues remain unfixable, stop and report what's blocking.

### Step 2: Code review

Run the `/kpa-code-review` skill on uncommitted changes. If the review finds any **Critical** or **High** severity issues, attempt to fix them. Re-review after fixes. If Critical or High issues persist, **stop and report** — do not continue to later steps.

### Step 3: Sync and archive

Run the `/opsx:sync` command to sync delta specs to main specs, then run the `/opsx:archive` command to archive the change. For any prompts that arise during sync or archive (e.g., change selection, sync confirmation), proceed with the obvious/recommended choice since we already verified in Step 1.

### Step 4: Fix all

Run the `/kpa-fix-all` skill (tests, linter, CSS linter, TypeScript compiler, build). Fix any issues found. If issues remain unfixable, stop and report.

### Step 5: Update docs

- Update `CHANGELOG.md` with a summary of what changed, following the existing format. Only add user facing changes to the changelog, and keep it short and in user-facing language.
- Update `ROADMAP.md` — check off any completed features or milestones.

### Step 6: Commit and push

If all previous steps succeeded, run the `/kpa-commit-and-push` skill. The commit message should summarize the change that was finalized.

## Guardrails

- Always execute steps in order — do not skip ahead.
- If a step fails and cannot be fixed, stop immediately and report which step failed and why.
- For Steps 1 and 2, "fix issues" means making code changes — not just reporting them.
- For Step 3, auto-select the active change if there is only one; otherwise prompt.
- Keep the user informed of progress as you move through each step.
