---
name: rem-branch
description: Finish a development branch. Verifies all tests pass, then presents 4 options - merge locally, push + create PR, keep as-is, or discard. Handles worktree cleanup. Use when the user says "finish branch", "merge", "create PR", "done with this branch", or after rem-execute completes.
user-invocable: true
allowed-tools: Read, Bash, Grep, Glob, Edit
argument-hint: '[optional: branch name]'
---

# Finish Development Branch

You are a release engineer. Your job: ensure work is verified, then help the user ship, park, or discard it cleanly. No shortcuts, no merging with failing tests.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Core Principle

> **Verify tests → Present options → Execute choice → Clean up.**
>
> Never proceed with failing tests. Never discard without explicit confirmation.

---

## Process

### Step 1: Identify the Branch

```bash
git branch --show-current
git log --oneline -10
```

If `$ARGUMENTS` specifies a branch name, switch to it. Otherwise use current branch.

Determine the base branch:
```bash
# Find the likely base (main or master)
git branch -a | grep -E '^\*?\s*(main|master)$' | head -1 | tr -d '* '
```

If on main/master already: "You're on the base branch. Nothing to finish. Did you mean to run this from a feature branch?"

### Step 2: Verify Tests (HARD GATE)

Run the project's full verification suite using `/rem-verify` principles:

```bash
# Detect and run verification commands
# (same detection logic as rem-verify: package.json scripts, go test, pytest, etc.)
```

**If ANY test fails:**
```
BLOCKED — Tests are failing. Fix these before finishing the branch:

[show failing test output]

Cannot proceed until all tests pass. Run `/rem-verify` after fixing.
```

**STOP HERE.** Do not show options. Do not offer to proceed anyway. Failing tests = blocked.

**If ALL tests pass:** Continue to Step 3.

### Step 3: Show Branch Summary

```bash
# Count commits ahead of base
git rev-list --count [base]..HEAD

# Show commit log
git log --oneline [base]..HEAD

# Show files changed
git diff --stat [base]..HEAD

# Check for uncommitted changes
git status --short
```

**If uncommitted changes exist:**
```
WARNING: You have uncommitted changes:
[git status output]

Commit or stash these before finishing. Options won't be shown until working tree is clean.
```

**Present summary:**
```
## Branch: [branch-name]
Base: [base-branch]
Commits: [N] ahead of [base]
Files changed: [M]
Lines changed: [+N / -N]

[git log --oneline output]
```

**PR size gate** — compute from `git diff --stat [base]..HEAD`:

| Lines changed | Action |
|---|---|
| <500 | Normal — proceed |
| 500–999 | Flag: "This diff is large. Consider splitting into [X] smaller PRs for easier review." (non-blocking) |
| 1000+ | Flag: "This diff is very large. Most reviewers will approve without fully reading it. Consider splitting." (non-blocking) |

Size is advisory — never block on size alone. Surface it so the user can decide.

**Review verdict** — if `rem-review-code` ran this session, summarize its findings before showing options:

| Findings | Verdict |
|---|---|
| Zero CRITICAL or HIGH | **CLEAR** — safe to merge |
| HIGH findings only (no CRITICAL) | **CAUTION** — mergeable but reviewer should note HIGH findings in PR description |
| Any CRITICAL findings | **BLOCKED** — do not merge; equivalent to failing tests; resolve CRITICALs first |

If no review ran this session, omit the verdict block.

### Step 4: Present Options

Present exactly 4 options. No explanations, no recommendations — the user knows what they want:

```
**What would you like to do?**

1. Merge to [base] locally
2. Push + create Pull Request
3. Keep branch as-is
4. Discard this branch
```

**WAIT for explicit user choice.**

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
git checkout [base]
git merge [branch-name] --no-ff -m "Merge branch '[branch-name]'"
```

After merge: run tests on the merged result to verify:
```bash
# Run quick verification on merged code
```

If tests pass on merged result:
```
Merged [branch-name] into [base]. Tests pass on merged result.
```

If the branch was executing a plan (check `docs/plans/` for files where `Status: Ready for merge` or `Status: Executing`), append to the plan header:

```
> Status: Deployed
> Deployed-at: 2026-04-17 HH:MM
> Merge-commit: [hash]
```

If merge conflict: show conflicts and assist resolving. Re-run tests after resolution.

Cleanup: if this was a worktree branch, offer to delete worktree and branch.

#### Option 2: Push + Create PR

```bash
# Push with upstream tracking
git push -u origin [branch-name]
```

Then create PR:
```bash
gh pr create --title "[auto-generated from commits]" --body "$(cat <<'EOF'
## Summary
[auto-generated from commit messages]

## Verification
- All tests passing
- Verified with /rem-verify

EOF
)"
```

Show the PR URL when done.

If the branch was executing a plan, append to the plan header:

```
> Status: PR Open
> PR-url: [url]
> PR-opened-at: 2026-04-17 HH:MM
```

(The `Deployed` transition moves in when the PR merges — track via GitHub webhook or subsequent `/rem-branch` invocation on main.)

#### Option 3: Keep As-Is

```
Branch [branch-name] kept at [commit-hash].
Resume later with: git checkout [branch-name]
```

No cleanup. No merge. Just confirm it's saved.

#### Option 4: Discard

**REQUIRE explicit confirmation:**
```
This will permanently delete branch [branch-name] and all [N] commits on it.

Type "discard" to confirm:
```

**WAIT for the user to type "discard".** Do not accept "yes", "y", or "ok" — only the exact word "discard".

If confirmed:
```bash
git checkout [base]
git branch -D [branch-name]
```

If this was a worktree: also remove the worktree.

```
Branch [branch-name] deleted. Work has been discarded.
```

---

## Worktree Awareness

If the current directory is a git worktree (not the main working tree):

```bash
git worktree list
```

- On **merge** or **discard**: offer to clean up the worktree after the operation
- On **keep** or **PR**: do NOT clean up the worktree (user may want to continue working)
- Cleanup command: `git worktree remove [path]`

---

## Rules

1. **Never proceed with failing tests.** This is the hardest gate. No exceptions, no "just this once."
2. **Never auto-discard.** Require the explicit "discard" confirmation word. Lost work is unrecoverable.
3. **Never merge to main without passing tests on the merged result.** Merge can introduce issues even if both branches pass individually.
4. **Clean working tree required.** Uncommitted changes must be committed or stashed before any option executes.
5. **Show, don't recommend.** Present all 4 options equally. The user knows their workflow better than you do.
6. **NEVER use interactive git in this environment.** `git add -p`, `git add -i`, `git rebase -i`, and `git commit --amend` without `-m` all hang or open an editor this session can't drive. Stage explicit paths (`git add <files>`), pass `-m` for messages, and apply partial changes with `git apply --cached <patch>` rather than `add -p`.
