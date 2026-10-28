---
name: housekeeper
description: "Run a conservative code-project housekeeping pass: one proven low-risk cleanup at a time."
disable-model-invocation: true
---

# Housekeeper

## Goal

Find and apply one proven, low-risk cleanup at a time while preserving existing behavior and protecting unrelated work.

## Loop Prompt

```text
Review [repository or code project] for dead code, meaning unreachable or unused code; stale files or comments; unused dependencies; duplication; broken links; inconsistent names; and confusing structure. Protect unrelated, active, uncommitted, generated, and uncertain work. Prove one low-risk cleanup, make the smallest coherent change, then rerun the build, tests, runtime checks, and diff review. Keep only verified improvements. Stop when none remain, progress stalls, verification is unavailable, or approval is required. Return changes, evidence, and deferred candidates.
```

Stop when no confirmed low-risk cleanup remains and existing behavior still passes.

## When To Use

Use this when a code project has accumulated small maintenance problems, such as unused code, stale files, duplicated logic, broken links, old comments, inconsistent names, or confusing organization, but broad deletion would be risky.

This loop cleans source and project structure. It is not a Git branch, pull request, commit, or worktree cleanup workflow.

## Workflow

1. Inspect the current project state before changing anything.
2. Identify active branches, uncommitted edits, generated files, configuration, build artifacts, and other work that must not be disturbed.
3. Collect possible cleanup candidates.
4. Pick one candidate that can be proven low risk from code references, configuration, documentation, tests, or runtime behavior.
5. Make the smallest coherent change that removes or improves that candidate.
6. Run the relevant existing checks: build, tests, lint/type checks, runtime smoke checks, link checks, or project-specific verification.
7. Review the diff and keep the change only if behavior stays intact and unrelated work is untouched.
8. Repeat until no proven low-risk cleanup remains, progress stalls, verification is unavailable, or the next candidate needs approval.
9. When stopping on candidates that need approval, ask the user to pick which to apply, in one question (`AskUserQuestion` where available: `multiSelect: true`, one option per deferred candidate, at most 4 per question and further questions for the rest; otherwise a numbered list in chat). Continue the loop in the same run on every approved candidate, one at a time.

## Candidate Types

Look for:

- Unreachable or unused code.
- Stale files or stale comments.
- Unused dependencies.
- Duplicated logic.
- Broken links.
- Inconsistent names.
- Confusing project structure.

Treat generated files, unclear files, active work, and user changes as protected until there is direct evidence and approval.

## Report

End with:

- Cleanup candidates reviewed.
- Changes made.
- Evidence supporting each retained cleanup.
- Verification commands run and their results.
- Deferred candidates and why they were not changed.
- Any approval still needed, and the candidates the user declined.

Start each item that needs the user (a risk, a deferral, an approval) with ⚠️, and each failed check with ❌. No other marks.

## Guardrails

- Do not delete code merely because its purpose is not immediately obvious.
- Do not touch unrelated, active, uncommitted, generated, or uncertain work.
- Do not combine unrelated cleanups into one large change.
- Do not keep a cleanup if checks fail or behavior cannot be verified.
- Ask for approval before removing dependencies, deleting broad file sets, or changing public interfaces when risk is unclear (workflow step 9).
