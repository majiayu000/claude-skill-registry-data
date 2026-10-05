---
name: resolve-conflicts
description: Resolve git conflicts from any operation (merge, rebase, cherry-pick, stash, revert). Use when encountering conflicted files during git operations.
argument-hint: '[file path]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Resolve Conflicts

Resolve git conflicts from any operation with proper continuation workflow.

## Usage

```
/resolve-conflicts              # Resolve all conflicts
/resolve-conflicts path/to/file # Focus on specific file
```

## Gotchas
- A conflicted tree with **no sentinel file** is not automatically a stash/manual conflict. The most common trap is a `git pull --rebase` (autostash) whose re-apply conflicted: the rebase already finished, so no `rebase-merge/` exists, but the markers are real. Read the reflog + stash list before classifying — see Step 1.
- During rebase, ours/theirs semantics are INVERTED. "Ours" is the branch being rebased onto (the target), not your working branch. This causes wrong-direction resolutions if you forget.
- Lock file conflicts (package-lock.json, yarn.lock, Podfile.lock) must NEVER be manually resolved. Delete the lock file and regenerate it — manual merging produces corrupt files.

## Workflow

### Step 1: Detect State

Never infer the state from the conflict markers alone, and never assume "no
sentinel file" means a simple manual conflict. Gather the full picture first
with one command, then classify:

```bash
git status; echo "=== STASH ==="; git stash list; echo "=== REFLOG ==="; git reflog -n 6
```

Then use Glob to check for sentinel files in `.git/`:
- `.git/MERGE_HEAD` → **Merge**
- `.git/rebase-merge` or `.git/rebase-apply` → **Rebase**
- `.git/CHERRY_PICK_HEAD` → **Cherry-pick**
- `.git/REVERT_HEAD` → **Revert**
- **None of the above → do NOT stop at "stash/manual".** Disambiguate using the
  reflog + stash list you already gathered (see below).

| Operation | Detection | Continue | Abort |
|-----------|-----------|----------|-------|
| Merge | `MERGE_HEAD` exists | `git commit` | `git merge --abort` |
| Rebase | `rebase-merge/` or `rebase-apply/` | `git rebase --continue` | `git rebase --abort` |
| Cherry-pick | `CHERRY_PICK_HEAD` exists | `git cherry-pick --continue` | `git cherry-pick --abort` |
| Revert | `REVERT_HEAD` exists | `git revert --continue` | `git revert --abort` |
| Stash apply | No sentinel; reflog shows manual `stash pop`/`apply` | `git stash drop` | `git checkout --merge` or restore from stash |
| Autostash re-apply | No sentinel; reflog shows `pull --rebase`/`rebase (finish)` + an `autostash` stash entry | nothing to continue — just `git add` (the rebase already finished — do **not** `git rebase --continue`) | `git checkout --merge .` |
| Manual / committed | No sentinel, no stash entry, no recent operation | nothing to continue — just `git add` | `git checkout --merge <file>` |

**Disambiguating the no-sentinel case (this is where detection usually goes wrong):**

A `git pull --rebase` (or any `rebase --autostash`) stashes your dirty tree,
replays/fast-forwards, then re-applies the autostash. If that re-apply
conflicts, the rebase has **already completed** — so there is no `rebase-merge/`
sentinel, yet the working tree has real conflict markers. This looks identical
to a plain stash conflict until you read the reflog. The tells:
- The reflog's top entries show the finished rebase/pull (`rebase (finish)`,
  `pull --rebase`, a fast-forward) and a `stash` push labeled `autostash`.
- `git stash list` still contains the autostash entry (git keeps it on a failed
  apply — it is not auto-dropped). It is a harmless leftover backup; leave it.

In this case the only remaining work is to resolve the markers and `git add`. Do
**not** attempt `git rebase --continue` — it will fail because no rebase is in
progress.

### Step 2: List Conflicted Files

```bash
git diff --name-only --diff-filter=U
```

Then run `git status` to see the full conflict status for each file.

Conflict markers in `git status`:
- `UU` - Both modified (most common)
- `AA` - Both added
- `DD` - Both deleted
- `AU`/`UA` - Added by us/them, modified by other
- `DU`/`UD` - Deleted by us/them, modified by other

### Step 3: Analyze Each Conflict

Read the conflicted file and identify:

```
<<<<<<< HEAD (or ours)
Current branch changes
=======
Incoming changes
>>>>>>> branch-name (or theirs)
```

**For rebase conflicts:** "Ours" is the branch being rebased onto, "theirs" is the commit being replayed. This is inverted from merge!

### Step 4: Apply Resolution

Edit the file to:
1. Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. Keep the correct code
3. Ensure the result is syntactically valid

### Step 5: Complete the Resolution

The user invoked this skill to resolve **and** finish an in-progress git
operation, so complete it yourself:

1. Stage the files you resolved: `git add <resolved-files>`.
2. Run the continue command for the detected operation, using a non-interactive
   flag so no editor opens and hangs:

   | Operation | Continue command |
   |-----------|------------------|
   | Merge | `git commit --no-edit` |
   | Rebase | `GIT_EDITOR=true git rebase --continue` |
   | Cherry-pick | `git cherry-pick --continue --no-edit` |
   | Revert | `git revert --continue --no-edit` |
   | Stash apply | `git stash drop` |
   | Autostash re-apply | nothing to run — the `git add` is the completion (rebase already finished — never `git rebase --continue` here) |
   | Manual / committed | nothing to run — the `git add` is the completion |

### Step 6: Loop Until the Operation Finishes

A rebase, or a cherry-pick or revert of a range, replays commits one at a time,
and **any later commit can stop on its own conflict**. When that happens the
continue command exits non-zero and prints `CONFLICT (...)` and
`could not apply <sha>...`. This is a normal stop, not a failure. The user asked
for the whole operation to be finished, so keep going:

1. After every continue command, check the state again:
   ```bash
   git status; echo "=== UNMERGED ==="; git diff --name-only --diff-filter=U
   ```
2. **Sentinel gone** (no `rebase-merge/`, `rebase-apply/`, `CHERRY_PICK_HEAD`,
   `REVERT_HEAD`) → the operation is done. Go to the output.
3. **Still in progress with unmerged paths from a new commit** → go back to
   Step 2 and resolve this round. Check which commit is being replayed now
   (`git show --stat REBASE_HEAD`, or `CHERRY_PICK_HEAD` / `REVERT_HEAD`). Each
   round has a different "theirs", so work out its intent again before you
   resolve anything. For a rebase, `git status` shows progress
   ("Last commands done" / "Next commands to do").
4. Repeat until step 2 applies. Do not stop to ask between rounds unless a
   round needs a decision you can't make (see guardrails).

**Empty after resolution:** sometimes your resolution leaves the replayed commit
with no changes, because its change is already upstream. A default
(`rebase-merge/`) rebase drops that commit on its own and keeps going. Cherry-pick
and revert stop with "The previous cherry-pick is now empty", and a
`rebase-apply/` rebase stops with "No changes". Once `git diff --cached HEAD` is
confirmed empty, run `git cherry-pick --skip` / `git revert --skip` /
`git rebase --skip` and continue the loop. A commit that still has changes must
never be skipped.

**Guardrails — do not run these automatically:**
- **Aborts** (`git merge/rebase/cherry-pick/revert --abort`) discard work. If
  resolution isn't viable, stop and tell the user the abort command to run.
- **`git reset --hard`** (the stash abort path) discards work and nothing blocks
  it — the user must run it themselves.
- If a continue command fails for any reason other than a new conflict stop or
  an empty commit, surface the error and stop. Examples: the *same* files are
  still unmerged, a pre-commit hook rejected the commit, or a rebase `exec` step
  failed. Do not force it through.
- If a later round's conflict is genuinely ambiguous (you can't tell which
  side's intent should win), stop mid-operation and report which commit it is
  and the options. Leave the operation in progress for the user.

## Output Format

```markdown
## Conflict Resolution: {MERGE|REBASE|CHERRY-PICK|REVERT}

### Situation
- Operation: {type}
- Current branch: {branch}
- Incoming: {branch/commit}

### Conflicted Files ({count})
| File | Type | Complexity |
|------|------|------------|
| {path} | UU | {simple/moderate/complex} |

### Rounds (one per stop; a single row for merge/stash)
| # | Replayed commit | Files resolved | Result |
|---|-----------------|----------------|--------|
| 1 | {sha} {subject} | {paths} | {continued / next conflict / skipped empty / finished} |

### Completion
- Final state: {operation finished | stopped at round N: reason}

If resolution wasn't viable, abort manually:
- `{abort_command}`
```

## Examples

**Merge conflict on auth logic -- merge both sides:**
> /resolve-conflicts src/auth/session.ts

Detects a merge operation, reads the conflict markers in the session file, and determines that both sides added complementary validation checks. Recommends merging both changes together and produces a clean resolution that includes both validations.

**Rebase conflict with inverted ours/theirs:**
> /resolve-conflicts

Detects a rebase operation and reminds that ours/theirs semantics are inverted during rebase. Walks through each conflicted file, explains what the rebased commit intended versus the target branch state, resolves the conflicts in the files, stages them, and runs `GIT_EDITOR=true git rebase --continue`. When the next commit stops on its own conflict (`could not apply <sha>`), it resolves that round the same way and keeps going until the rebase finishes. It then reports every round.

**Autostash re-apply conflict after `git pull --rebase`:**
> /resolve-conflicts

Finds UU conflicts but no `.git/rebase-merge` sentinel. Instead of guessing, the gathering command's reflog shows `pull --rebase` finishing with a fast-forward and an `autostash` push, and `git stash list` still holds the autostash. Classifies this as an autostash re-apply conflict (rebase already complete), resolves the markers, runs `git add` — and does **not** try `git rebase --continue`.

## Guidelines

- **Understand both sides** before resolving - don't blindly pick one
- **Check for semantic conflicts** - code may compile but logic is broken
- **Review the full file** - changes outside markers may be affected
- **Test after resolving** - run tests if available
- **For rebase:** remember ours/theirs are inverted from merge

## Common Patterns

### Lock File Conflicts (package-lock.json, yarn.lock)

Regenerate rather than manually resolve. Run:
```
git checkout --theirs package-lock.json  # or --ours
npm install  # regenerates lock file
git add package-lock.json
```

### Auto-generated Files

Accept one version and regenerate. Run:
```
git checkout --theirs <file>
# Run generation command
git add <file>
```

### Both Added Same File Differently

Usually keep one and incorporate changes from other manually.

### Deleted vs Modified

Decide: should file exist or not? If yes, keep modified. If no, remove. Run the appropriate command:
```
# Keep the file (accept modification)
git add <file>

# Delete the file
git rm <file>
```
