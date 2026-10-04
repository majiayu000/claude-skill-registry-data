---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work — guides completion of development work by presenting structured options for merge, PR, or cleanup
tags: [meta, workflow, git, completion]
applies-to: [antigravity, cursor, copilot, gemini]
level: project
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

**Before presenting options, run full verification:**

```bash
# Regenerate all generated code
dart run build_runner build --delete-conflicting-outputs

# Static analysis
flutter analyze

# Run all tests
flutter test

# Quick build check (optional but recommended)
flutter build apk --debug 2>&1 | tail -5
```

**If any verification fails:**
```
Verification failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until all checks pass.
```

Stop. Don't proceed to Step 2.

**If all pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
# Try common base branches
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null || git merge-base HEAD develop 2>/dev/null
```

Or ask: "This branch split from main — is that correct?"

### Step 3: Present Options

Present exactly these 5 options:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally (includes deleting plan/spec/task files)
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
5. Just cleanup artifacts (delete plan/spec/task files)

Which option?
```

**Don't add explanation** — keep options concise.

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
flutter test

# If tests pass
git branch -d <feature-branch>

# Cleanup artifacts (if any)
rm -f docs/plans/*.md docs/specs/*.md task.md
```

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR (if gh CLI available)
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Verification
- [ ] `flutter analyze` — clean
- [ ] `flutter test` — all passing
- [ ] Manual testing on iOS
- [ ] Manual testing on Android
EOF
)"
```

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. You can merge or PR when ready."

#### Option 4: Discard

**Confirm first:**
```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

#### Option 5: Just Cleanup Artifacts

```bash
# Cleanup artifacts (if any)
rm -f docs/plans/*.md docs/specs/*.md task.md
```

## Quick Reference

| Option | Merge | Push | Cleanup Branch |
|--------|-------|------|----------------|
| 1. Merge locally | ✓ | - | ✓ |
| 2. Create PR | - | ✓ | - |
| 3. Keep as-is | - | - | - |
| 4. Discard | - | - | ✓ (force) |
| 5. Just cleanup | - | - | - |

## Common Mistakes

**Skipping test verification**
- **Problem:** Merge broken code, create failing PR
- **Fix:** Always verify tests before offering options

**Skipping build_runner**
- **Problem:** Generated code out of sync, builds fail on CI
- **Fix:** Always run `build_runner` before final verification

**Open-ended questions**
- **Problem:** "What should I do next?" → ambiguous
- **Fix:** Present exactly 5 structured options

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed "discard" confirmation

## Red Flags

**Never:**
- Proceed with failing tests or analysis errors
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request
- Skip `build_runner` before final verification

**Always:**
- Run full Flutter verification suite before offering options
- Present exactly 5 options
- Get typed confirmation for Option 4

## Integration

**Called by:**
- **executing-plans** — After all tasks complete
- Any workflow that completes a feature branch

**Pairs with:**
- **verification-before-completion** — Ensures evidence before claims
