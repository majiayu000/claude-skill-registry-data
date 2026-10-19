---
name: git-merge-conflicts
description: >
  Detect, analyze, and resolve three-way Git merge and rebase conflicts without
  discarding code changes. Use when merge or rebase operations stop with conflict
  markers (<<<<<<<, =======, >>>>>>>), resolving divergence between branches,
  verifying post-conflict test suites, or safely aborting failed merges.
compatibility: >
  Agent Skills-compatible coding agents operating in a Git repository environment.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "git, merge-conflicts, rebase, three-way-merge, diff3, conflict-resolution"
  topics: "version-control, devtools"
---

# Git Merge Conflict Resolution

Merge and rebase conflicts occur when two concurrent branches modify the same lines of code or when one branch modifies a file that another branch moved or deleted. Resolving conflicts safely requires understanding the three-way merge context, preserving valid logic from both branches, and never silently discarding modifications.

## Core Rules

1. **Never discard changes blindly**: Inspect both sides of the conflict. Understand the architectural intent of the incoming and target branches before deciding.
2. **Use `diff3` or `zdiff3` conflict style**: Shows the common ancestor base, revealing *why* the conflict occurred rather than just the two conflicting outcomes.
3. **Always verify compilation and tests after resolution**: Resolving conflict markers is only step one; syntactic resolution can still introduce semantic bugs. Run test suites before completing the merge or rebase.
4. **Never commit unfinished conflict markers**: Search for `<<<<<<<`, `=======`, and `>>>>>>>` across all files before staging.
5. **Abort safely if lost**: When a rebase or merge goes wrong, use `git merge --abort` or `git rebase --abort` to return cleanly to the pre-merge state.

---

## 1. Enabling Informative Conflict Markers (`zdiff3`)

Configure Git to display the common merge-base ancestor:

```bash
git config --global merge.conflictstyle zdiff3
```

A standard conflict vs a `zdiff3` conflict:

```text
<<<<<<< HEAD (ours - current branch)
const TIMEOUT_MS = 5000;
||||||| 3a8f1b2 (base - common ancestor)
const TIMEOUT_MS = 1000;
=======
const TIMEOUT_MS = 3000;
>>>>>>> feature/shorter-timeout (theirs - incoming branch)
```
With the common ancestor visible, you can see that both branches intentionally altered the initial 1000ms baseline.

---

## 2. Step-by-Step Resolution Workflow

### Step 1: Identify Conflicted Files
```bash
# Display unmerged files with 'UU' status
git status --short

# List conflicted filenames directly
git diff --name-only --diff-filter=U
```

### Step 2: Inspect Context & History
```bash
# View the incoming commit messages that caused the conflict
git log --merge -p <conflicted_file>
```

### Step 3: Resolve the Conflict in Code
Edit the conflicted file:
- Remove marker lines (`<<<<<<<`, `|||||||`, `=======`, `>>>>>>>`).
- Synthesize the correct combined logic (e.g., keeping imports from both branches, combining list elements, or preserving newer API signatures).

### Step 4: Verify and Complete
```bash
# 1. Search for any forgotten markers
grep -rnE "^<{7}|^={7}|^>{7}" .

# 2. Stage resolved file
git add <conflicted_file>

# 3. If in a merge:
git commit -m "merge: resolve conflict between main and feature/timeout"

# 4. If in a rebase:
git rebase --continue
```

---

## 3. Aborting Failed Merges Safely

If resolution is ambiguous or risky, abort cleanly:

```bash
# Abort an active merge: restores pre-merge working tree
git merge --abort

# Abort an active rebase: returns to original branch HEAD
git rebase --abort
```

---

## 4. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `git checkout --ours <file>` without reading | Silently drops legitimate new features from incoming branch | Inspect diff first; merge changes deliberately |
| Leaving stray conflict markers in code | Syntax error in production builds | Search with `grep -rn "^<{7}" .` before committing |
| Staging files before running tests | Semantic regressions committed to history | Run full test suite (`pytest`, `cargo test`) before completing merge |
| Force-pushing over conflict | Erases colleague's work on shared remote | Rebase or merge cleanly, test, and push safely |

---

## 5. Verification Checklist

- [ ] `git diff --check` reports zero remaining conflict marker artifacts.
- [ ] Logic from both branches has been reviewed and properly reconciled.
- [ ] Application compiles and all unit/integration tests pass cleanly.
- [ ] Merge or rebase completed cleanly without detached HEAD.
