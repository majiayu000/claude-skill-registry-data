---
name: fix-merge-conflicts
description: Resolve git merge conflicts in dependency files, source code, and configuration. Use when merge conflicts are detected.
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Fix Merge Conflicts

You are the AI Engineering Maintenance Bot resolving merge conflicts in a Vector Institute repository.

## Context
Read `.pr-context.json` for PR details. Check `git status` for conflicting files.

## ⚠️ CRITICAL: Do Not Commit Bot Files

**NEVER commit these temporary bot files:**
- `.claude/` directory (bot skills)
- `.pr-context.json` (bot metadata)
- `.failure-logs.txt` (bot logs)

These files are automatically excluded from git, but **do not explicitly `git add` them**.

When committing fixes, only add the actual fix files:
```bash
# ✅ CORRECT: Add only fix-related files
git add src/conflicted-file.ts package.json

# ❌ WRONG: Never do this
git add .  # This might include bot files if exclusion fails
git add .claude/
git add .pr-context.json
```

## Process

### 1. Identify Conflicts
```bash
git status
git diff --name-only --diff-filter=U
```

### 2. Resolution Strategy by File Type

**Dependency Files (package.json, requirements.txt)**
- Prefer newer versions
- Keep additions from both sides
- Maintain consistent formatting

Example:
```
<<<<<<< HEAD
"dep-a": "^2.0.0",
"dep-b": "^1.5.0"
=======
"dep-a": "^1.9.0",
"dep-c": "^3.0.0"
>>>>>>> PR

RESOLVE TO:
"dep-a": "^2.0.0",  // Newer version
"dep-b": "^1.5.0",  // From base
"dep-c": "^3.0.0"   // From PR
```

**Lock Files (package-lock.json, poetry.lock)**
- DON'T manually edit
- Delete and regenerate:
```bash
npm install      # npm
poetry lock      # Python
cargo update     # Rust
```

**Source Code**
- Preserve functionality from both sides when possible
- Base branch wins for different implementations (more recent)
- Combine both additions if compatible
- Follow base formatting

**Configuration Files**
- Merge both sets of changes logically
- Preserve workflow improvements
- Maintain proper syntax

**Documentation**
- Combine both updates
- Keep chronological order for changelogs
- Preserve both feature descriptions

### 3. Resolution Steps
For each file:
1. Read entire file for context
2. Locate conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
3. Analyze both versions
4. Make decision using strategy above
5. Edit file to remove markers
6. Verify syntax is valid

### 4. Finalize
```bash
git add <resolved-files>
git diff --check  # Verify no markers remain
```

### 5. Push to Correct Branch

**CRITICAL**: Push changes to the correct PR branch!

```bash
# Get branch name from .pr-context.json
HEAD_REF=$(jq -r '.head_ref' .pr-context.json)

# Push to the PR branch (NOT a new branch!)
git push origin HEAD:refs/heads/$HEAD_REF
```

**DO NOT**:
- ❌ Create a new branch name
- ❌ Push to a different branch
- ❌ Use `git push origin HEAD` without specifying target

The branch name MUST match `head_ref` from `.pr-context.json`.

## Safety Checklist
- [ ] All conflict markers removed
- [ ] File syntax is valid
- [ ] Dependencies at compatible versions
- [ ] No functionality lost
- [ ] Lock files regenerated (not manually edited)

## Important Rules
- Never leave conflict markers in files
- Prefer newer over older versions
- Keep both additions when non-conflicting
- Regenerate lock files (don't manually resolve)
- Preserve intent from both sides

## Commit Format
```
Resolve merge conflicts

- [File 1]: [Resolution description]
- [File 2]: [Resolution description]

Co-authored-by: AI Engineering Maintenance Bot <aieng-bot@vectorinstitute.ai>
```

## Safety Rules
- ❌ Don't leave conflict markers
- ❌ Don't choose older versions
- ❌ Don't manually edit lock files
- ❌ Don't discard additions
- ✅ Verify syntax after resolution
- ✅ Regenerate lock files properly
