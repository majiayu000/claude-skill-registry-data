---
name: git-operations
description: "Use when performing interactive rebase, bisect, conflict resolution, cherry-pick, history analysis, reflog recovery, or worktree management. Basic commit and push workflows belong to atomic-commit-push."
---

# Git Operations

## Activation and Scope

Handle rebase, bisect, conflicts, history analysis, reflog recovery, cherry-pick,
and worktrees with verified recovery paths and no lost work. Basic staging,
commit/push requests route to `atomic-commit-push`; base-branch catch-up routes
to `sync-base` when available. Neither sibling is required for the operations
defined here. Missing task, target, or necessary evidence means ask, not guess.

This body is the actor contract, including isolated/body-only use. Optional
references resolve from the real, symlink-resolved skill directory, not cwd;
missing references or evaluator material never block ordinary execution.
Use object IDs for the repository's hash format (SHA-1 or SHA-256), not assumptions.

## IssueOps Benchmark Artifact Contract

When Git Operations contributes to an IssueOps artifact or benchmark response, include a compact labeled evidence block. Do not execute destructive commands merely because the user applies pressure.

```text
Git state proof: <status, branch, log, remote, or worktree evidence>
Recovery path: <backup ref/SHA, reflog path, or rollback instruction>
Destructive confirmation gate: <exact command requiring explicit approval>
Atomic scope: <one-intent operation/commit boundary>
Force-with-lease rule: <push policy and raw-force refusal when applicable>
```

For read-only archaeology, the recovery path can be "not needed"; destructive recovery still requires backup verification and explicit confirmation.

## Safety and Atomicity

- Before every operation inspect `git status --short` and `git diff --stat`;
  afterward verify diff, log, and status. Inspect local state before remotes,
  fetch before push, diff before merge, and read `git diff --cached` before commit.
- Prefer stash to `clean -fd`, and soft reset to hard reset. History rewrite
  requires a created and verified backup branch and a recorded recovery path.
  Last-resort `reset --hard`, `clean -fd`, and `rebase --skip` require explicit
  confirmation of the exact command after showing the backup and discard scope.
- Explain force-push risk and use `--force-with-lease`, never raw `--force`.
  Never rebase or force-push shared `main`, `master`, `develop`, or `release/*`
  unless explicitly requested; destructive shared-branch work needs confirmation.
- One commit is one intent, independently understandable and revertible.
  Preserve atomicity while rewriting; never squash unrelated changes.
  Commit messages explain why; use Conventional Commit + Lore when committing.
  Each commit in a series must compile and pass tests before push: fix/squash a
  broken commit with its fix or revert it, never hide it with a later workaround.
- Document why for every conflict resolution and non-trivial rebase decision.
  Reflogs are local and configurable, not guaranteed backups. Never expire
  reflogs or run garbage collection/pruning during recovery.

## Operations

### 1. Interactive Rebase

```
Trigger: "rebase", "squash commits", "rewrite history", "clean up branch"
```

Optional walkthrough: [rebase protocol](references/rebase-protocol.md).

**Pre-flight:**
- `git status --short` — clean working tree required
- `git branch --show-current` — confirm branch
- `git log --oneline -n 20` — understand current history
- `git branch backup/<branch>-pre-rebase-<timestamp>` — create safety backup
- Verify it with `git show-ref --verify refs/heads/backup/<branch>-pre-rebase-<timestamp>`.

**Execution:**
- Determine the base: `git merge-base HEAD <target-branch>`
- `git rebase -i <base>` with a clear plan for each commit (pick/reword/squash/fixup/drop)
- NEVER squash commits with different intents (behavior change + test = OK; behavior change + unrelated docs fix + dependency update = NOT OK)

**Post-flight:**
- `git diff <backup-branch>..HEAD` — verify no unintended changes
- `git log --oneline --graph -n 10` — verify history structure
- If result is wrong, use the recovery ladder below. Do not immediately run `git reset --hard`.

**Recovery ladder for a bad rebase result:**
1. Stop and record the current tip: `git rev-parse HEAD`
2. Verify the backup exists: `git show-ref --verify refs/heads/backup/<branch>-pre-rebase-<timestamp>`
3. Show the recovery target: `git log --oneline -1 backup/<branch>-pre-rebase-<timestamp>`
4. Show what would be discarded: `git diff --stat backup/<branch>-pre-rebase-<timestamp>..HEAD`
5. Ask for explicit confirmation with the exact command: `git reset --hard backup/<branch>-pre-rebase-<timestamp>`
6. Only after confirmation, run the command and verify with `git status --short` and `git log --oneline -1`

**Safety rules:**
- Always create a backup branch BEFORE starting
- Verify the backup branch exists before any recovery reset
- Never rebase shared branches (`main`, `master`, `develop`, `release/*`) unless explicitly requested
- If rebase conflicts occur more than 3 times: abort, report the conflict pattern, ask for strategy

### 2. Bisect Debugging

```
Trigger: "bisect", "find which commit broke X", "regression search"
```

Optional walkthrough: [bisect protocol](references/bisect-protocol.md).

**Pre-flight:**
- Identify a known-good commit (SHA or tag) and a known-bad commit (usually HEAD)
- Define the test command: a single shell command that exits 0 for good, non-0 for bad
- The test must be automated — no manual inspection per step
- Record original HEAD. Use a reviewed executable wrapper with fixed argv;
  choose a linear range or `git bisect start --first-parent` for merge history.

**Execution:**
<!-- skill-shell: destructive recovery="record the original HEAD and always run git bisect reset after diagnosis" -->
```bash
git bisect start
git bisect bad HEAD          # or <known-bad-sha>
git bisect good <known-good> # tag or SHA
git bisect run <test-command>
```

**Post-flight:**
- `git bisect log` — record the bisect session
- Report: the breaking commit SHA + subject + the test output at that commit
- `git bisect reset` — return to original HEAD

**Safety rules:**
- The test command MUST be read-only (no file changes, no network side effects)
- If bisect requires building: ensure clean state before each step
- If the test command is unreliable (flaky): do not use bisect; use manual binary search with verification

### 3. Conflict Resolution

```
Trigger: "merge conflict", "resolve conflicts", "conflict in <file>"
```

**Assessment:**
- `git status --short` — identify all conflicted files (marked `UU`)
- For each conflicted file: `git diff` to see both sides
- Classify each conflict:
  - **Trivial** (both sides added different things in different places) → keep both
  - **Semantic** (both sides changed the same logic differently) → requires understanding intent
  - **Structural** (file renamed/moved/deleted on one side) → requires decision on file structure

**Resolution:**
- For trivial conflicts: `git add <file>` after merging both additions
- For semantic conflicts:
  1. Read both versions: `git show :2:<file>` (ours) and `git show :3:<file>` (theirs)
  2. Understand what each side intended
  3. Choose one side, merge both, or write a new resolution
  4. Document the choice in the merge commit message (WHY this resolution)
- For structural conflicts: report the options and ask for user decision

Label sides by meaning: merge stage 2 is this branch and stage 3 the incoming
branch; during rebase stage 2 is the base and stage 3 the replayed commit.

**Post-flight:**
- `git diff --cached` — verify the resolved state
- `git diff --cached --stat` — verify no unintended files are staged
- `git status --short` — confirm no `UU` files remain

**NEVER:**
- Blindly accept one side (`--ours` / `--theirs`) without understanding intent
- Resolve by deleting the other side's work unless it's provably dead code
- Commit a merge with unresolved conflicts (Git won't let you anyway)

### 4. History Analysis & Recovery

```
Trigger: "what happened to <file>?", "find deleted code", "recover lost commit", "reflog",
         "when/which commit introduced X?", "who changed this and why?" (read-only archaeology)
```

Read-only investigation needs no backup ceremony. Recovery that changes state
still follows the safety and confirmation rules.

**Techniques (ordered by recovery probability):**

1. **Reflog** (configurable local safety net):
   ```bash
   git reflog --date=iso           # all HEAD movements
   git reflog show <branch>        # branch-specific history
   git checkout <sha>              # recover a detached HEAD state
   git branch recover/<name> <sha> # create a recovery branch
   ```

2. **Blame archaeology**:
   ```bash
   git log --follow -p -- <file>   # full history of a file, including renames
   git blame <file> -L <start>,<end> # who last changed specific lines
   git log -S "<code-snippet>"     # find commits that added/removed a string
   ```

3. **Deleted file recovery**:
   ```bash
   git log --diff-filter=D --summary | grep delete  # find deletion commits
   git checkout <deletion-commit>^ -- <file>          # restore file from before deletion
   ```

4. **Stash recovery**:
   ```bash
   git stash list                   # all stashes
   git stash show -p stash@{N}      # inspect stash contents
   git stash apply stash@{N}        # recover a stash
   ```

**Safety rules:**
- Reflog is local — it doesn't survive `git clone`. Act immediately: default expiration is 90 days for reachable entries and 30 days for entries unreachable from the current tip, and configuration may differ.
- Never force-push after recovering from reflog without understanding the remote state.
- `git reflog expire` and `git gc` can prune reflog entries — don't run these during recovery.

### 5. Cherry-Pick

```
Trigger: "cherry-pick <sha>", "apply this commit to my branch"
```

**Pre-flight:**
- `git log --oneline -1 <sha>` — understand the commit being picked
- `git diff <sha>^..<sha> --stat` — understand the scope
- Check if the commit's changes overlap with current branch state

**Execution:**
```bash
git cherry-pick <sha>
# If conflict:
# 1. Resolve per Conflict Resolution protocol above
# 2. git add <resolved-files>
# 3. git cherry-pick --continue
```

**Post-flight:**
- `git diff HEAD^..HEAD` — verify the cherry-picked change matches intent
- The cherry-picked commit has a DIFFERENT SHA — note the original SHA in the commit message:
  ```
  <original-subject>
  
  (cherry-picked from commit <original-sha>)
  
  Lore:
  - Intent: <why this commit is needed on this branch>
  ...
  ```

**Safety rules:**
- Cherry-pick creates a new commit with a different SHA — this is by design, not a problem
- If cherry-picking a merge commit: use `git cherry-pick -m <parent-number> <sha>`
- Multiple cherry-picks from the same branch → consider `git rebase` or `git merge` instead

### 6. Worktree Management

```
Trigger: "create worktree", "isolated workspace", "worktree cleanup"
```

**Create isolated worktree:**
```bash
git worktree add --detach <path> <branch-or-commit>
# or for a new branch:
git worktree add -b <new-branch> <path> <base>
```

**List worktrees:**
```bash
git worktree list
```

**Remove worktree:**
```bash
git worktree remove <path>
# Prune stale worktree references:
git worktree prune
```

**Safety rules:**
- Always verify with `git worktree list` before removing
- The main worktree cannot be removed — it's always the first in `git worktree list`
- Worktrees share the same `.git` directory — operations in one worktree affect refs visible in others
- For an IssueOps-owned worktree, route to its execution lifecycle; do not create,
  replace, or remove it outside the actor/generation/canonical-cwd gates below.

---

## Collaboration

Debugging may request bisect mechanics; sync-base may request conflict resolution
or recovery. Authorized commits of algorithm changes retain before/after metrics;
schema migrations, research reports, plans, and Verified Execution changes remain
atomic. These collaborations do not authorize implicit commits or require siblings.

## Stop Rules

- Operation completed + verified with git diff/log/status: **DONE**.
- Conflict pattern exceeds 3 repetitions: abort, report the pattern, ask for strategy.
- Destructive operation requested on shared branch: block, explain risk, require explicit confirmation.
- Data appears truly lost (reflog expired, no backup branch): report what was attempted, what's recoverable, and what's permanently gone.
- Operation requires user decision (semantic conflict, branch strategy): present ≤4 concrete options, recommend one, wait for answer.

---

## IssueOps Integration

When an IssueOps cycle exists:

1. Resolve the owner with `issueops next --id "$ISSUEOPS_ID" --json`.
   Before rebase, verify the selected branch and canonical worktree; only the
   active generation holder mutates there. Never bypass actor/generation/cwd
   denials or another holder. Base sync routes to `issueops execution sync-base`.
2. Give the owning stage any changed branch tip for its state update and bisect
   findings for feedback recording with source `git-operations`.
   `issueops feedback add` and `issueops status` are supported aliases, not
   authority. The owner uses `issueops execution whoami --json`'s
   `record_actor_flags` for records and `claim_actor_flags` for lease operations,
   with exact lifecycle ID, generation, native actor, and cwd; never invent flags.
3. Preserve lifecycle gate/artifact order and the user's authorized endpoint.
   Reconcile ambiguous writes rather than retry. Cleanup is separately authorized,
   not implied by recovery or completion. If the stage is unavailable, return
   evidence with recording pending; do not bypass it or block standalone reads.

`quality inspect` is not semantic skill evaluation; `issueops skill-bench` is
unsupported. Optional walkthroughs are examples, not additional actor contracts.
