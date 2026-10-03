---
name: codex-branch-finisher
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work — guides completion of development work by presenting structured options for merge, PR, or cleanup
load_priority: on-demand
---

## TL;DR
Verify tests → Present 4 options (merge, PR, keep, discard) → Execute choice → Clean up worktree. Never leave work in limbo.

# Finishing a Development Branch

## Activation

1. Activate on `$codex-branch-finisher`, `$finish`, or `$finish-branch`.
2. Activate when all tasks in a plan are complete.
3. Activate after `codex-subagent-execution` completes all tasks.
4. Activate after `codex-execution-quality-gate` passes.
5. Activate after `codex-workflow-autopilot` reaches `ship` mode.

**Announce at start:** "I'm using codex-branch-finisher to complete this work."

## The Iron Law

```
NO COMPLETION WITHOUT TEST VERIFICATION
NO OPEN-ENDED "WHAT NEXT?" — PRESENT STRUCTURED OPTIONS
```

## The Process

### Step 1: Verify Tests

**Before presenting options, verify tests pass:**

```bash
# Bash
npm test  # or: cargo test / pytest / go test ./...
```

```powershell
# PowerShell
npm test  # or equivalent for your stack
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

STOP. Do not proceed to Step 2.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

```powershell
git merge-base HEAD main 2>$null; if ($LASTEXITCODE -ne 0) { git merge-base HEAD master 2>$null }
```

Or ask: "This branch split from main — is that correct?"

### Step 3: Present Options

Present **exactly these 4 options** — no more, no less, no open-ended questions:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** — keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
<test command>                    # Verify on merged result
git branch -d <feature-branch>   # Only after merge success
```

Then: Cleanup worktree (Step 5).

#### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "## Summary
- <bullet 1>
- <bullet 2>

## Test Plan
- [ ] All tests pass
- [ ] Manual verification complete"
```

```powershell
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "## Summary`n- <bullet 1>`n`n## Test Plan`n- [ ] All tests pass"
```

Then: Cleanup worktree (Step 5).

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

**Don't cleanup worktree.**

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for **exact confirmation**. Then:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5).

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

```powershell
git worktree list | Select-String (git branch --show-current)
```

If yes:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep worktree.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | — | — | ✓ |
| 2. Create PR | — | ✓ | ✓ | — |
| 3. Keep as-is | — | — | ✓ | — |
| 4. Discard | — | — | — | ✓ (force) |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping test verification | Always verify tests before offering options |
| Open-ended "What should I do?" | Present exactly 4 structured options |
| Auto worktree cleanup | Only cleanup for Options 1 and 4 |
| No confirmation for discard | Require typed "discard" confirmation |
| Force-push without explicit request | Never force-push unless user explicitly asks |

## Integration

| Called By | When |
| --- | --- |
| `codex-subagent-execution` | After all tasks complete |
| `codex-workflow-autopilot` | After `ship` mode completes |
| `codex-execution-quality-gate` | After gate passes |
| Direct invocation | `$finish` or `$finish-branch` |

| Pairs With | Purpose |
| --- | --- |
| `codex-git-worktrees` | Cleans up worktree created by that skill |
| `codex-verification-discipline` | Tests must PASS before presenting options |

## Script Invocation Discipline

1. When this workflow calls helper scripts from other skills, run `--help` first.
2. Treat helper scripts as black-box tools and execute by contract before reading source.
3. Read script source only when customization or bug-fixing is required.
