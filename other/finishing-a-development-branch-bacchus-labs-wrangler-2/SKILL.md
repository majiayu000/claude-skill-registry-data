---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by verifying work is complete (tests, requirements, code review, TDD compliance) and presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify completeness (tests, requirements, code review, TDD) → Present options → Execute choice → Clean up.

## The Process

### Step 1: Verify Completeness

BEFORE presenting options, verify work is ACTUALLY complete:

#### 1.1: Tests Pass

Run full test suite:

```bash
npm test
# or
pytest
# or
cargo test
# or
go test ./...
```

**Required output**:
- All tests pass (0 failures)
- No errors or warnings
- Exit code: 0

**If tests fail**: STOP. Fix tests. Cannot proceed with incomplete work.

#### 1.2: Requirements Met

Check verifying-before-completion requirements checklist:

- [ ] All planned features implemented
- [ ] All edge cases handled
- [ ] All error paths tested
- [ ] Documentation updated (if applicable)
- [ ] No TODOs or FIXMEs added

**If ANY unchecked**: Work is NOT complete. Finish requirements first.

#### 1.3: Code Review Obtained (MANDATORY)

Check verifying-before-completion code review gate:

- [ ] Code review completed (or valid exception 1, 2, or 3 documented)
- [ ] Critical issues: 0 (MUST be zero)
- [ ] Important issues: 0 OR converted to tracked issue with ID

**Valid exceptions (ONLY these):**

1. **Pure documentation**: *.md files in docs/ directory only (ZERO code/config changes)
2. **Configuration-only**: Dependency updates in package.json, tsconfig.json (NO logic changes)
3. **Emergency hotfix**: Production completely down, active security breach (MUST be reviewed within 24 hours)

**If code review required but not obtained**: STOP. Request code review first.

**If claiming exception**: Document which exception (1, 2, or 3) and provide evidence.

#### 1.4: TDD Compliance

Check verifying-before-completion TDD certification:

- [ ] TDD compliance certification completed
- [ ] All new functions have tests written first
- [ ] All functions watched fail → watched pass

**If TDD violated**: Work is NOT complete. Violations must be fixed.

#### 1.5: Pristine Output

Verify no errors, warnings, or deprecations:

- [ ] Test output is clean (no errors/warnings)
- [ ] Linter passes (if applicable)
- [ ] Build succeeds (if applicable)
- [ ] No console.log/print statements in production code

**If output not pristine**: Clean up before proceeding.

### Completeness Verification Result:

**ONLY if ALL sections (1.1-1.5) are complete**: Continue to Step 2.

**If ANY section incomplete**:
- STOP immediately
- Fix the incomplete section
- Do NOT proceed to Step 2
- Do NOT present merge/PR options

This is a GATE. You cannot proceed without complete verification.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

**Prerequisites verified** (from Step 1):
- ✓ All tests pass
- ✓ All requirements met
- ✓ Code review obtained
- ✓ TDD compliance certified
- ✓ Output is pristine

Since work is VERIFIED complete, you have these options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** - keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then: Cleanup worktree (Step 5)

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then: Cleanup worktree (Step 5)

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

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

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then: Cleanup worktree (Step 5)

### Step 5: Cleanup Worktree (if applicable)

**For Options 1, 2, 4:**

Check if in worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

**If in worktree:**
```bash
git worktree remove <worktree-path>
```

**If NOT in worktree (main branch):**
- Skip worktree cleanup (no action needed)

**For Option 3:** Keep worktree (if one exists).

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | ✓ | - | - | ✓ |
| 2. Create PR | - | ✓ | ✓ | - |
| 3. Keep as-is | - | - | ✓ | - |
| 4. Discard | - | - | - | ✓ (force) |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 4 structured options

**Automatic worktree cleanup**
- **Problem:** Remove worktree when might need it (Option 2, 3)
- **Fix:** Only cleanup for Options 1 and 4

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Red Flags - STOP IMMEDIATELY

If you find yourself:

- Skipping Step 1 verification ("tests pass, that's good enough")
- Presenting options before ALL Step 1 checks complete
- Claiming exception to code review without documenting which (1, 2, or 3) and providing evidence
- Proceeding with unfixed TDD violations
- Saying "work is done" without requirements verification
- Claiming Important issues are "acknowledged" without tracked issue ID

THEN:
- STOP immediately
- Go back to Step 1
- Complete ALL verification steps
- This is not optional

Proceeding without complete Step 1 verification violates verifying-before-completion.

## Integration

**Called by:**
- **implementing-issue** - After all tasks complete and final verification passes

**Pairs with:**
- **using-git-worktrees** - Cleans up worktree if one was created (optional)
