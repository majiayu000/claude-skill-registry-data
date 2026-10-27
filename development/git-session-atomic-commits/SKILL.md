---
name: git-session-atomic-commits
description: "Session-scoped git commit orchestrator with hard scope enforcement: commits ONLY files with evidence of belonging to the current agent session and leaves every other dirty worktree change untouched. Builds an evidence-based allowlist (user-provided scope, files the agent created/edited this session, session logs) and an ignore list of everything else; enforces a blocking pre-commit gate so unrelated files or hunks can never be staged or committed. Inherits git-atomic-commit for atomic grouping and commit message execution (constrained to the allowlist only) and git-commit-scope-constitution for scope governance and validation. Use when asked to commit this session only, isolate commits from mixed worktree state, or when the worktree contains pre-existing dirty changes that must not be committed."
argument-hint: "Optional session scope hint: feature, issue, files, or short intent"
metadata:
  version: 0.2.0
---

# Session-Scoped Atomic Commits

## The Invariant

**Commit exactly the current session's changes — and nothing else.**

Any changed file not proven to belong to this session is **OUT OF SCOPE** and must be
left completely untouched (not staged, not committed, not stashed, not reverted).
The default classification of every changed file is *out of scope* until evidence
places it in scope. When in doubt, stop and ask — never guess.

## Inherited Skills

Load and delegate to these; do not re-implement their rules here:
- **git-atomic-commit** — atomic partitioning, staging, commit execution, type/scope format
- **git-commit-scope-constitution** — scope inventory and validation

## Phase 0 — Establish the Session Boundary (Evidence, Not Inference)

Collect evidence, in order of reliability:

1. **Explicit user scope**: argument text, stated intent, linked issue/PR or branch.
2. **Session tool history**: files this agent created or edited in THIS session
   (its own `create_file` / edit calls, and terminal commands that wrote files).
3. **Session log** (when available, e.g. `VSCODE_TARGET_SESSION_LOG` in VS Code):
   file write/edit events recorded for the current session.
4. **Full worktree inventory**: `git status --short`, `git diff --name-only`,
   `git diff --cached --name-only`, plus untracked files (`git status --porcelain`).

Then:

- **Allowlist** = every changed path backed by evidence (1)–(3). Record the evidence
  for each path.
- **Ignore list** = every changed path in the inventory (4) that is NOT on the allowlist.
- If any changed path cannot be classified with confidence → **STOP and ask the user.**
  Do not proceed on a guess.

## Phase 1 — Pre-Flight Inventory and Index Audit

1. Run `git status --short` and record the complete change set.
2. **Index audit**: run `git diff --cached --name-only`. If ANY pre-staged file is not
   on the allowlist → **STOP and ask** how to handle it (unstage, commit separately,
   or exclude). Never commit on top of pre-staged unrelated files.
3. **Untracked trap check**: enumerate untracked files explicitly. Never use
   `git add .`, `git add -A`, or `git add <dir>` — these are the primary cause of
   accidental out-of-scope commits.

## Phase 2 — Verify Allowlist Completeness

For each allowlist path, confirm it shows a worktree change (`git status` / `git diff`).
If an allowlist path has no change, drop it (nothing to commit) and note it in the report.
If the user expects a change there but git shows none, report it rather than forcing it.

## Phase 3 — Constrained Delegation to git-atomic-commit

Pass **only the allowlist** to **git-atomic-commit**. State the constraint explicitly:

> Scope is limited to these files only: [list]. All other worktree changes are
> out of scope; do not analyze, stage, or commit them.

**git-atomic-commit** handles type/scope assignment, grouping, and message generation
for the allowlist. This skill retains final responsibility for scope enforcement:
if the delegated agent stages anything outside the allowlist, stop and unstage it.

## Phase 4 — Pre-Commit Verification Gate (MANDATORY, Blocking)

Before ANY `git commit`, verify all of the following. Any failure blocks the commit:

- [ ] **Staged set == allowlist**: `git diff --cached --name-only` matches the allowlist
      exactly — no more, no fewer.
- [ ] **Zero ignore-list paths staged**: intersection of `git diff --cached --name-only`
      with the ignore list is empty.
- [ ] **No pre-existing unrelated staged files** remain in the index.
- [ ] **No broad staging** was used (`git add .`, `git add -A`, `git add <dir>`,
      `git commit -a` / `-am`).
- [ ] **Scopes validated** via **git-commit-scope-constitution**.

If any check fails: unstage the offending paths (`git restore --staged <path>`),
re-verify, and only then proceed.

## Phase 5 — Commit and Post-Commit Verification

1. Execute commits via **git-atomic-commit** (interactive or autonomous per its rules).
2. After each commit, run `git status --short` and confirm every ignore-list file is
   still present and unstaged.
3. Only report completion after the post-commit check passes.

## Hard Rules (Non-Negotiable)

1. **Never stage or commit a file not on the allowlist.** Default classification of any
   changed file is OUT OF SCOPE until evidence says otherwise.
2. **Never use broad staging**: `git add .`, `git add -A`, `git add <dir>`,
   `git commit -a` / `-am`.
3. **Never commit over pre-staged unrelated files** — stop and ask.
4. **Never stash, checkout, reset, or delete unrelated changes** to "clean up" the
   worktree. Leave them exactly as-is.
5. **Never guess a file into the session.** Insufficient evidence → stop and ask.
6. **Never amend** existing commits unless explicitly requested.
7. **If the session boundary cannot be established confidently, stop and report.**
   Do not proceed, do not "do your best".
8. **Scope expansion is explicit**: if the user asks to include an ignore-list file,
   add it to the allowlist with the user's confirmation, then re-run Phase 4.
9. Prefer non-destructive git commands at all times.

## Output

Return in order:
1. Session scope identified, with an evidence summary for each allowlist file.
2. Commits created (type/scope/message).
3. Files included per commit.
4. Unrelated changes intentionally left untouched (the ignore list).
5. Any ambiguities and how they were resolved.
