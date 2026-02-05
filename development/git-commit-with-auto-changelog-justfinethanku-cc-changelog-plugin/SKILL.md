---
name: Git Commit with Auto-Changelog
description: Automatically documents code changes in a searchable changelog when committing to git. Creates structured entries with what/why/issues. Use when user asks to commit changes to git.
---

# Git Commit with Auto-Changelog Skill

Automatically documents code changes in a searchable changelog when committing to git.

## Purpose

Every commit creates a structured changelog entry that captures:
- What changed (files, features, fixes)
- Why (decision rationale)
- Issues encountered
- Dependencies added
- Testing notes
- Next steps

All entries are indexed in an auto-generated README for easy searching.

## Usage

**The skill activates automatically when you ask to commit changes:**

```
"Commit these changes"
"Let's commit this work"
"Create a git commit with changelog for this session"
```

You can optionally provide a summary:
```
"Commit with message: Implement sectional evaluation system"
```

## What This Skill Does

### 1. First-Time Setup (if `changelog/` doesn't exist)
- Creates `changelog/` directory
- Creates `.changelog-keywords.txt` with default tags
- Creates initial `README.md` index
- Logs the setup as first changelog entry

### 2. Every Commit
- Analyzes git changes (`git diff --stat`)
- Suggests keywords based on file paths
- Prompts for changelog details (what, why, issues)
- Generates timestamped markdown entry
- Regenerates README index
- Stages all changes (code + changelog)
- Creates commit with descriptive message
- Optionally pushes to remote

### 3. Maintains Searchability
- Auto-updates README with one-line summaries
- Groups entries by month
- Creates keyword index at bottom
- Enables Cmd+F searching across all sessions

## Process Flow

1. **Check for changes**
   - Run `git status`
   - If no changes, exit with message
   - If changes exist, proceed

2. **First-time setup check**
   - Look for `changelog/` directory
   - If missing, create full structure
   - Add setup entry to changelog

3. **Analyze changes**
   - Run `git diff --stat` for file summary
   - Parse file paths to suggest keywords
   - Count lines added/removed

4. **Prompt user for details**
   - Session description (or use provided message)
   - Why these changes were made
   - Issues encountered (optional)
   - Keywords (show suggestions, allow editing)
   - Dependencies added (if package.json changed)

5. **Generate changelog entry**
   - Create `changelog/YYYY-MM-DD-HHMM-descriptive-slug.md`
   - Fill template with user responses
   - Include git diff summary
   - Add timestamp and session duration estimate

6. **Update index**
   - Use Glob to find all `changelog/*.md` files (exclude README.md)
   - Read each file and parse headers (title, keywords, date)
   - Group entries by month (YYYY-MM)
   - Build keyword index with entry counts
   - Write new README with monthly entries + keyword index

7. **Commit everything**
   - Stage all code changes: `git add .`
   - Stage changelog files: `git add changelog/`
   - Create commit with message
   - Show commit SHA

8. **Push prompt**
   - Ask: "Push to remote? (Y/n)"
   - If yes: `git push origin [current-branch]`
   - Show push status

## Keyword Auto-Suggestion

Based on file paths modified:

| File Pattern | Suggested Keywords |
|--------------|-------------------|
| `**/migrations/*.sql` | [DATABASE] [MIGRATION] |
| `**/models/**` | [DATABASE] [MODELS] |
| `**/api/**`, `**/functions/**` | [BACKEND] [API] |
| `**/components/**` | [COMPONENTS] [UI] |
| `**/pages/**`, `**/routes/**` | [FRONTEND] [ROUTING] |
| `**/hooks/**`, `**/composables/**` | [FRONTEND] [HOOKS] |
| `**/styles/**`, `*.css`, `*.scss` | [STYLING] [UI] |
| `package.json`, `requirements.txt`, `Cargo.toml` | [DEPENDENCIES] |
| `.env*`, `*.config.*` | [CONFIG] |
| `*.test.*`, `*.spec.*`, `**/__tests__/**` | [TESTING] |
| `README*`, `docs/**` | [DOCUMENTATION] |
| `Dockerfile`, `*.yml`, `*.yaml` | [DEPLOYMENT] [INFRA] |

User can always add/remove keywords from suggestions.

## Changelog Entry Template

```markdown
# YYYY-MM-DD - Descriptive Title
**Keywords:** [KEYWORD1] [KEYWORD2] [KEYWORD3]
**Session:** [Time of day], Duration (~X hours)
**Commit:** [commit-sha]

## What Changed
- File: `path/to/file.tsx`
  - Added feature X
  - Modified component Y
- File: `path/to/migration.sql`
  - Created table Z
  - Added columns A, B, C

## Why
[User's explanation of decision rationale]

## Issues Encountered
[Problems hit during implementation, workarounds applied]

## Dependencies
[NPM packages added/updated, if any]

## Testing Notes
- What was tested: [description]
- What wasn't tested: [known gaps]
- Edge cases: [discovered issues]

## Next Steps
- [ ] Item 1
- [ ] Item 2
```

## Example Session

```
You: Let's commit this work

Skill analyzing changes...

📊 Changes detected:
  src/api/users/controller.ts
  src/models/user.ts
  src/components/UserProfile.tsx
  tests/users.test.ts
  (8 files changed, 234 insertions(+), 67 deletions(--)

Describe this session (or press Enter for AI summary):
> Add user profile customization feature

Why these changes?
> Users requested ability to customize their profiles. Added avatar upload, bio field, and social links. Integrated with existing authentication system.

Any issues encountered? (optional)
> Avatar upload needed file size validation. Initially tried client-side only, but added server-side validation for security.

Suggested keywords: [BACKEND] [API] [COMPONENTS] [UI] [TESTING]
Modify keywords (or press Enter to accept):
> [add: FEATURE]

Final keywords: [BACKEND] [API] [COMPONENTS] [UI] [TESTING] [FEATURE]

Dependencies changed:
  Added: multer@1.4.5-lts.1 (file upload middleware)

Testing notes (what was tested):
> Tested avatar upload with various file sizes and formats. Verified bio field validation (max 500 chars). Checked social link URL validation.

What wasn't tested? (optional)
> Edge cases for international characters in bio field

Next steps (tasks remaining):
> - Add internationalization for bio field
> - Implement avatar image optimization
> - Update API documentation

✅ Created changelog/2025-01-15-1430-user-profile-customization.md
✅ Updated changelog/README.md (3 total entries)
✅ Staged 10 files (code + changelog)

Commit message:
"feat: Add user profile customization feature

- Added avatar upload with validation (client + server)
- Implemented bio field with 500 char limit
- Added social links section with URL validation
- Integrated with existing auth system

Added multer dependency for file uploads."

Create commit? (Y/n): y

✅ Committed as a7f3c9e

Push to origin/main? (Y/n): y

✅ Pushed successfully

📝 Changelog updated: changelog/2025-01-15-1430-user-profile-customization.md
🔍 Search keywords: [BACKEND] [API] [COMPONENTS] [UI] [TESTING] [FEATURE]
```

## Files Created by Skill

### On First Use

**`changelog/.changelog-keywords.txt`:**
```
# Common Keywords
[FRONTEND]
[BACKEND]
[DATABASE]
[API]
[UI]
[COMPONENTS]
[MODELS]
[ROUTING]
[HOOKS]
[STYLING]
[TESTING]
[BUG_FIX]
[FEATURE]
[REFACTOR]
[PERFORMANCE]
[SECURITY]
[DEPLOYMENT]
[INFRA]
[DOCUMENTATION]
[DEPENDENCIES]
[CONFIG]
[MIGRATION]

# Project-Specific (auto-appended as used)
```

**`changelog/README.md`:**
Auto-generated index (regenerated after every commit)

### After Each Commit

**`changelog/YYYY-MM-DD-HHMM-descriptive-slug.md`:**
Filled template with session details (timestamp prevents collisions across branches)

## Configuration

### Skip Changelog (for trivial changes)

Say: "Commit without changelog: Fix typo in README"

Commits without creating changelog entry (use sparingly).

### Amend Last Entry

Say: "Amend the last changelog entry with these changes"

Updates most recent changelog entry instead of creating new one (if continuing same session).

## Tools Used

- **Bash** - Git operations (status, diff, add, commit, push)
- **Read** - Parse existing changelog entries
- **Write** - Create new entries and update index
- **Grep** - Search for keywords in existing entries (for duplicate detection)

## Error Handling

**No changes to commit:**
```
❌ No changes detected. Nothing to commit.
```

**Merge conflict in changelog:**
```
⚠️ Merge conflict in changelog/README.md
Resolve manually and ask to commit again
```

**Push failed:**
```
❌ Push failed (branch not up to date)
Pull latest changes and try again
```

## Best Practices

### DO:
- ✅ Create entry for every feature, bug fix, or meaningful change
- ✅ Be specific in "What Changed" (file paths, function names)
- ✅ Explain "Why" decisions were made
- ✅ Document failed experiments (valuable context!)
- ✅ Add new keywords to vocabulary when needed

### DON'T:
- ❌ Use for typo fixes (say "commit without changelog")
- ❌ Use generic descriptions ("made changes")
- ❌ Skip "Why" section (most important for future you)
- ❌ Forget to test before committing

## Future Enhancements

**Planned:**
- Search functionality: "Search changelog for [keyword]"
- Stats reporting: "Show changelog statistics"
- PR integration: Copy changelog to PR description
- Auto-detect WIP commits and suggest skipping changelog

## Notes

- Changelog entries are **immutable** - never revised after creation
- README is auto-generated - do not edit manually
- Keywords are case-sensitive by convention (use UPPERCASE)
- One entry per work session (not per commit if doing multiple quick commits)
- If continuing work on same feature same day, ask to amend the last entry to update it
- **Merge-friendly:** Timestamps in filenames prevent collisions across branches
- After merging branches, ask Claude to regenerate the index if needed
