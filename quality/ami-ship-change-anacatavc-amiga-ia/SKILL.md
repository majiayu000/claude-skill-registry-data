---
name: ami-ship-change
description: Main-session orchestrator to validate, review, fix, commit, push, and optionally open a Pull Request with numbered confirmation gates. Replaces nested push/PR orchestrator subagents.
allowed-tools: Bash, Read, Grep, Glob, Edit, Write, Agent
---
# Skill: Ship Change Orchestrator

You are the main-session orchestrator for shipping changes safely from working tree to remote push and optional Pull Request creation. Running this workflow in the main session eliminates nested subagents while keeping read-only verification isolated.

**Core Invariants:**
- Never bypass Git hooks (`--no-verify`).
- Never run `git commit`, `git push`, or `gh pr create` without explicit user confirmation at each gate.
- Never duplicate tests already executed and passed (exit code 0) by `ami-change-validator` unless files were modified afterward.

## Workflow

### 0. Scope Discovery & Repository Policy Gate
- Inspect `git rev-parse --show-toplevel`, `git branch --show-current`, `git worktree list --porcelain`, and `git status --porcelain`.
- Determine the target base branch (e.g., `origin/main` or configured PR base) and commit/diff range.
- **Read-Only / No-Commit Repo Policy:** If repository rules forbid automated commits or pushes in the current workspace, run validation and review only, then print the exact ready-to-paste `git` / `gh` commands and stop.

### 1. Parallel Validation & Self-Review (Main-Session Fan-Out)
Launch these read-only subagents **in parallel** from the main session:
1. **`ami-change-validator`:** Run in `standard` mode (or `pr` mode if the user intends to open/update a Pull Request).
2. **`ami-pr-reviewer`:** Run in **Self-Review / Findings-only mode** over the full change range (committed unpushed changes + working tree WIP), without requiring an existing PR.

Wait for both subagents to complete and consolidate their blockers, warnings, and findings.

### 2. Findings Review & Approved Fixes (Max 3 Rounds)
- Present all blockers and review findings to the user clearly, anchored to `file:line`.
- If there are no findings and all validation checks passed, proceed to Step 3.
- **CONFIRMATION 1 - Apply Fixes:** Ask the user if they want to apply fixes for the reported findings.
  - Only upon approval, apply the fixes in the working tree (in the main session, or via a platform-native write-capable worker such as `TypeName: "self"` / `define_subagent` with `EnableWriteTools: true` in Antigravity if the fixes span >3 files or require heavy test iteration).
  - **Strict Boundary:** Never run `git commit` or `git push` during this remediation loop.
  - Re-verify modified files and affected checks. Repeat at most **3 rounds**; if blockers remain after 3 rounds, stop and escalate to the user.

### 3. Adversarial Verification Gate
- On the final post-fix diff (skipping only if the diff is trivial documentation/formatting with zero logic changes), launch **`ami-adversarial-verifier`** from the main session, passing only the final diff and the stated requirement.
- If confirmed defects are returned, present them to the user and resolve them before proceeding.

### 4. Commit Confirmation
- If uncommitted changes (WIP and/or applied fixes) exist, invoke `__AMIGA_CODEX_SKILLS_DIR__/ami-plan-commits/SKILL.md` in the main session to structure the commit plan (grouping WIP + fixes cleanly, using `amend`/`fixup`/new `fix:` commit as appropriate, and **never** amending a commit authored by someone else or already pushed).
- **CONFIRMATION 2 - Execute Commit:** Present the active worktree, branch, and exact commit plan (files + Conventional Commit messages). Execute `git add` / `git commit` only after explicit user approval.

### 5. Push Confirmation
- Run `git fetch` and verify remote sync:
  - If an upstream tracking branch exists (`git rev-parse --abbrev-ref --symbolic-full-name '@{u}'`, non-zero exit means no upstream), verify `git merge-base --is-ancestor '@{u}' HEAD` so remote commits are not overwritten. If local is behind or diverged, advise `git pull --rebase` and halt.
  - If no upstream exists, prepare `git push -u origin <branch>`.
- **CONFIRMATION 3 - Execute Push:** Present the exact `git push` command and target remote branch. Execute only after explicit user approval.

### 6. Pull Request Creation (Optional)
- If the user requested a Pull Request (or `pr` mode was selected):
  - Review the `ami-change-validator` `pr` mode output: diff size/stack check (>500 lines warning), open PR conflicts, documentation sync status, and the polished PR description.
  - **CONFIRMATION 4 - Create PR:** Present the PR title, base branch, and full body description. Execute `gh pr create` (or `gh stack submit` / `gt submit --stack` for stacked PRs) from the main session only after explicit user approval.
- **Post-Push Cleanup:** If operating in a secondary linked worktree that is now clean and synced, offer `git worktree remove` as an optional cleanup step.

---
**Language Rule:** Although code, commits, and PR descriptions MUST be in English (unless the repo specifies otherwise), communicate with the user in their language.
