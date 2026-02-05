---
name: session-wrapup
description: Complete end-of-session workflow for SheldonFS project. Handles code commits, quality checks, documentation updates, and merge process. Use when finishing a development session or feature branch.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

# SheldonFS Session Wrap-Up

Complete workflow for wrapping up a development session or feature branch in the SheldonFS project.

## When to Use This Skill

- At the end of a development session
- When completing work on a feature branch
- Before switching context to a different task
- When the user says "wrap up" or "finish session"

## Prerequisites

- User must provide the feature branch name
- Must be in the SheldonFS project directory structure

## Step-by-Step Process

### Phase 1: Code Quality & Commits (SheldonFS/ directory)

**1.1 Verify Location and Branch**

```bash
cd SheldonFS  # Navigate to code repository
pwd           # Confirm location
git branch    # List branches
git status    # Check current state
```

**1.2 Handle Uncommitted Changes**

If `git status` shows uncommitted changes:

```bash
# Review changes
git diff

# Create semantic commit following the template
git commit -m "feat/fix/refactor: Brief description

- Bullet point if needed
- Additional context"
```

Commit message types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation only
- `test`: Tests
- `chore`: Build/tooling

**1.3 Run Quality Checks**

Execute in order, fixing issues as they appear:

```bash
# 1. Linting
npm run lint

# If errors, attempt to fix
npm run lint:fix

# If still errors, manually fix and verify
npm run lint

# 2. Type checking
npm run typecheck

# If errors, fix them and verify
npm run typecheck

# 3. Tests (if test infrastructure exists)
npm test
```

**1.4 Commit Quality Fixes**

If linting or typechecking errors were fixed:

```bash
git add .
git commit -m "fix: Resolve linting and type errors

- Fixed [specific issues]"
```

**1.5 Handle Test Failures**

If tests fail:
- **DO NOT** attempt to fix them
- Make a note for documentation update (Phase 2)
- Keep feature branch open for next session

### Phase 2: Documentation Updates (sheldon-fs/ parent directory)

**2.1 Analyze Required Updates**

Review the conversation context and code changes:

```bash
cd ..  # Move to parent sheldon-fs/ directory
cd SheldonFS && git diff main..HEAD --stat  # See what changed
cd ..
```

**2.2 Update CLAUDE.md**

Based on changes made, update relevant sections:

**Current Status Section:**
- Move completed items from "Next Steps" to "Completed"
- Add new accomplishments to "Completed" list
- Update "Next Steps" with remaining work

**Example update:**
```markdown
✅ **Completed:**
- File scanner module with SHA256 hash calculation
- Comprehensive metadata extraction (23 fields per file)
+ Test infrastructure with vitest  # NEWLY COMPLETED
+ Database layer with better-sqlite3  # NEWLY COMPLETED

🚧 **Next Steps:**
- ~~Add basic tests~~ DONE
- ~~Build database layer~~ DONE
+ Implement duplicate detection using hash comparisons  # MOVED UP
+ Add reporting functionality (JSON, CSV output)  # MOVED UP
```

**Immediate Next Steps Section:**

If tests failed, add as first item:
```markdown
### 1. Fix Failing Tests
- [Brief description of which tests failed]
- [Why they might be failing - if known]
```

**Tech Stack Section:**
- Add any new dependencies installed
- Move items from "Phase 1-2" to "Core Dependencies" if now in use

**2.3 Update Other Documentation (if needed)**

Check if updates needed in:
- Decision records (if architectural decisions were made)
- README files (if new features completed)

**2.4 Commit Documentation Changes**

```bash
# Check what changed
git status

# Add all documentation changes
git add CLAUDE.md decision-records/

# Determine session number by checking last commit
git log --oneline -3  # Look for "session-X" pattern

# Commit with session number
git commit -m "session-{n}: Brief description of session work

- Bullet point of changes
- Another change
- Additional context"
```

Session number is last session number + 1.

### Phase 3: Merge Decision (SheldonFS/ directory)

**3.1 Merge if All Checks Passed**

```bash
cd SheldonFS

# If linting, typechecking, and tests all passed:
git checkout main
git merge <feature-branch>
git branch -d <feature-branch>  # Delete merged branch
```

**3.2 Keep Branch Open if Tests Failed**

```bash
# Stay on feature branch
git status  # Confirm on feature branch
```

User will fix tests in next session.

### Phase 4: Summary Report

Provide structured summary to user:

```markdown
## Session Wrap-Up Complete

### Updates to Documentation
- Updated CLAUDE.md "Current Status" section with completed items
- Moved [X, Y, Z] from Next Steps to Completed
- Updated "Immediate Next Steps" with [new priority]
- [Any other documentation changes]

### Code Status
- **Feature branch:** `<branch-name>`
- **Commit message(s) added:**
  1. `<type>: <description>` (main feature work)
  2. `fix: Resolve linting errors` (if applicable)
- **Status:** Merged to main / Kept open
- **Follow-up action needed:** Yes/No
  - [If yes, describe what needs attention next session]

### Conclusion
[Brief 2-3 sentence assessment of the session]
[Any issues encountered during wrap-up]
[Suggested next logical task based on current progress]
```

## Examples

### Example 1: Successful Feature Completion

**User:** "Wrap up the feat/add-database-layer branch"

**Process:**
1. Navigate to SheldonFS/, check status
2. No uncommitted changes found
3. Run npm run lint → Passes
4. Run npm run typecheck → Passes
5. Run npm test → Passes
6. Navigate to parent dir
7. Update CLAUDE.md: Move "Build database layer" to Completed
8. Commit: "session-3: Database layer implementation"
9. Merge feature branch to main
10. Provide summary

### Example 2: With Quality Fixes Needed

**User:** "Wrap up feat/duplicate-detection"

**Process:**
1. Navigate to SheldonFS/
2. Uncommitted changes found → Create commit
3. Run npm run lint → **Errors found**
4. Run npm run lint:fix → Fixes applied
5. Verify with npm run lint → Passes
6. Commit fixes: "fix: Resolve linting errors"
7. Run npm run typecheck → Passes
8. Run npm test → 2 tests fail
9. Update CLAUDE.md with test failure note
10. Commit: "session-3: Duplicate detection with test failures"
11. **Keep branch open** for test fixes
12. Provide summary with follow-up action

### Example 3: Documentation-Only Changes

**User:** "Wrap up - only updated decision records"

**Process:**
1. Check SheldonFS/ → No code changes
2. Skip quality checks
3. Update CLAUDE.md if needed
4. Commit: "session-3: Updated Phase 4 decision records"
5. Provide summary

## Important Notes

- **Never force push** or use destructive git operations
- **Always verify** commands succeeded before proceeding
- **If uncertain** about code changes, ask user before committing
- **Session numbers** must be sequential - verify last session commit
- **Test failures** are noted, not fixed during wrap-up
- **Quality fixes** (lint/typecheck) are always attempted during wrap-up
- **Decision records** may need updates if architectural choices were made

## Troubleshooting

**Problem:** Can't find feature branch
**Solution:** List all branches with `git branch -a`, ask user to confirm name

**Problem:** Merge conflicts
**Solution:** Abort merge, notify user, ask for guidance

**Problem:** No package.json found
**Solution:** Verify in correct directory (SheldonFS/ for code commands)

**Problem:** Tests don't exist yet
**Solution:** Skip test step, note in summary that tests not yet implemented

**Problem:** Large diff in documentation
**Solution:** Ask user which specific sections to focus on updating

## Success Criteria

A successful wrap-up includes:
- ✅ All code changes committed with semantic messages
- ✅ Linting and typechecking pass (or fixes committed)
- ✅ Tests run (pass or failures documented)
- ✅ CLAUDE.md accurately reflects current status
- ✅ Feature branch merged (or kept open with clear reason)
- ✅ Session commit created in parent repo
- ✅ Clear summary provided to user

## Related Documentation

- Commit message guidelines: `CLAUDE.md` > "Commit Message Guidelines"
- Development phases: `CLAUDE.md` > "Development Phases"
- Current status: `CLAUDE.md` > "Current Status"
