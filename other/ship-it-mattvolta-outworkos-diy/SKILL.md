---
name: ship-it
description: "/ship-it - Commit, Push, and Create PR"
argument-hint: "[optional commit message]"
disable-model-invocation: true
---

# /ship-it - Commit, Push, and Create PR

Ship your completed work with proper commits, PR creation, and cleanup guidance.

## Usage

```
/ship-it
```

No arguments - operates on current branch.

---

## Pre-Conditions

**This command will STOP if:**
- You're on the `main` branch
- Build fails
- There are no changes to commit

---

## Workflow Steps

Execute these steps in order. **STOP and report if any step fails.**

### Step 1: Verify Not on Main

```bash
current_branch=$(git branch --show-current)
```

**If `main`:**
> "You're on the main branch. You should never commit directly to main."
> "Use `/start-work <issue>` to create a feature branch first."
> STOP.

### Step 2: Extract Issue Number from Branch

```bash
# Branch format: type/123-description
# Extract: 123
issue_number=$(git branch --show-current | grep -oE '[0-9]+' | head -1)
```

**If no issue number found:**
> "Could not detect issue number from branch name."
> Ask user: "What issue number is this work for? (or 'none')"

### Step 3: Run Build

**Detect the project's build command.** Check for:
1. `package.json` in the project root or common subdirectories — use `npm run build`
2. `Makefile` — use `make build`
3. Other build systems as appropriate

```bash
# Run from the project root (or appropriate app directory)
npm run build
```

**If build fails:**
> "Build is failing. You must fix build errors before shipping."
> Show errors and STOP.

**If build passes:** Proceed.

**If no build system found:** Skip and note "No build step detected."

### Step 4: Run Tests

**Detect the project's test command.** Check for:
1. `package.json` with a `test` script — use `npm test`
2. `pytest.ini` or `pyproject.toml` — use `pytest`
3. Other test runners as appropriate

```bash
npm test 2>&1 | tail -30
```

**Record results.** Note: Some pre-existing test failures may be acceptable.

**If NEW test failures (compared to baseline):**
> "Tests are failing. Review the failures:"
> Show failures
> Ask: "Are these pre-existing failures? [y/n]"

**If no test system found:** Skip and note "No test runner detected."

### Step 5: Gather Changes

```bash
# Staged and unstaged changes
git status

# Full diff
git diff HEAD --stat

# Detailed diff for commit message
git diff HEAD
```

**Present to user:**
```
Changes to be committed:
  [file list with status]

Summary:
  [X] files changed
  [Y] insertions(+)
  [Z] deletions(-)
```

### Step 6: Compose Commit Message

**Analyze changes and draft conventional commit message.**

**Determine type from changes:**
| Change Type | Commit Type |
|-------------|-------------|
| New feature | `feat` |
| Bug fix | `fix` |
| Documentation | `docs` |
| Refactoring | `refactor` |
| Tests only | `test` |
| Build/deps | `build` |
| Maintenance | `chore` |

**Draft message format:**
```
type(scope): description

[Body explaining what and why]

Closes #[issue-number]
```

**Present to user for approval:**
```
Proposed commit message:
---
feat(reminders): add email reminder scheduling

Implement scheduled email reminders for company update forms.
- Add reminder scheduler script
- Add template variable replacement
- Add Resend email integration
- Add GitHub Actions workflow for daily execution

Closes #198

Co-Authored-By: Claude <noreply@anthropic.com>
---

Proceed with this message? [yes/edit/cancel]
```

**Wait for user confirmation.** Do not proceed without explicit approval.

### Step 7: Update Changelog (Conditional)

**Determine if changelog entry is needed based on commit type:**

| Commit Type | Changelog Action |
|-------------|------------------|
| `feat` | Always generate entry |
| `fix` (user-facing bug) | Generate entry |
| `fix` (internal/dev bug) | Ask user |
| `refactor`, `chore`, `test`, `build`, `ci`, `docs` | Skip (offer to add if user wants) |

**If changelog entry IS needed:**

1. **Check for CHANGELOG.md** in the project root. If it exists, read it to find the insertion point.

2. **Determine insertion point:**
   - If today's date section exists → append to it
   - If today's date section doesn't exist → create new date header
   - If current month section doesn't exist → create new month header

3. **Transform commit message to changelog entry** using changelog-writer skill patterns:

   **Language transformation:**
   | Commit Style | Changelog Style |
   |--------------|-----------------|
   | "add feature X" | "We've added **Feature X**..." |
   | "implement Y" | "We've launched **Y**..." |
   | "improve Z" | "We've improved Z..." |
   | "fix bug in W" | "We've resolved an issue with W..." |

   **Apply security reframing** if commit touches security:
   - Never mention: vulnerability, exploit, security issue, XSS, injection
   - Reframe as: "Added validation", "Enhanced access controls", "Improved data handling"

4. **Present changelog entry to user for approval.**

5. **If approved:** Insert entry at correct position in CHANGELOG.md.

6. **Check for a public changelog page** (e.g., `app/(marketing)/changelog/page.tsx` or similar). If found, update its data structure to match.

**If changelog entry is NOT needed:**
> "This commit type (`refactor`/`test`/etc.) typically doesn't need a changelog entry."
> "Add changelog entry anyway? [yes/no]"

**If user selects 'skip':** Proceed without changelog update.

**If CHANGELOG.md doesn't exist:**
> "No CHANGELOG.md found. Create one? [yes/no]"
> If yes, create with standard header and first entry.

### Step 8: Stage and Commit

```bash
# Stage all changes (includes CHANGELOG.md if updated)
git add -A

# Commit with approved message
git commit -m "$(cat <<'EOF'
[approved commit message here]
EOF
)"
```

### Step 9: Push Branch

```bash
git push -u origin $(git branch --show-current)
```

**If push fails (e.g., remote exists):**
```bash
git push --force-with-lease origin $(git branch --show-current)
```

### Step 10: Create Pull Request

**Compose PR description:**

```markdown
## Summary
[2-3 bullet points from commit]

## Changes
[List of significant changes]

## Test Plan
- [ ] Build passes
- [ ] Tests pass
- [ ] Manual verification completed

## Related Issues
Closes #[issue-number]
```

**Create PR:**
```bash
gh pr create \
  --title "type(scope): description" \
  --body "[PR description]" \
  --base main
```

### Step 11: Report Success and Post-Merge Instructions

```
============================================
PR CREATED SUCCESSFULLY
============================================

PR:       #[pr-number]
URL:      [pr-url]
Branch:   [branch-name] → main

Status:
  Build:     [PASS/SKIPPED]
  Tests:     [X passing / SKIPPED]
  Commit:    [commit-hash]
  Changelog: [Updated/Skipped]

============================================
POST-MERGE CLEANUP (DO THIS AFTER PR MERGES)
============================================

After the PR is merged, run these commands:

  git checkout main
  git pull origin main
  git branch -d [branch-name]

Or run: /cleanup-branches

IMPORTANT: Do NOT continue work on this branch after merge.
           If more work is needed, create a NEW branch.
============================================
```

---

## Error Handling

| Error | Action |
|-------|--------|
| On main branch | STOP - must use feature branch |
| Build fails | STOP - must fix before shipping |
| No changes | STOP - nothing to commit |
| Push rejected | Try --force-with-lease, else report |
| PR creation fails | Show error, provide manual steps |
| CHANGELOG.md malformed | Show error, ask user to fix manually |

---

## What This Command Does NOT Do

- Does not merge the PR (that's done via GitHub after review)
- Does not delete the branch (that's post-merge cleanup)
- Does not skip build verification
- Does not commit without user approval of message
- Does not force changelog entries for non-user-facing changes

---

## Quick Reference: The Full Workflow

```
/start-work 198        # Begin: creates branch, establishes baseline
[... do your work ...]
[... verify it works ...]
/ship-it               # End: commits, pushes, creates PR (with changelog)
[... PR is reviewed and merged via GitHub ...]
/cleanup-branches      # Cleanup: deletes merged branches
```

---

## Related Skills

- **changelog-writer**: Provides patterns for writing changelog entries
