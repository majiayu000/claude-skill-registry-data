---
name: changelog-tracker
description: Analyzes uncommitted git changes and updates CHANGELOG.md and CLAUDE.md. Executes git commands, reads diffs, categorizes changes, and stages updated documentation automatically.
---

# Changelog Tracker Skill

This skill actively analyzes your git repository, examines uncommitted changes, and automatically updates documentation files (CHANGELOG.md and CLAUDE.md).

## Execution Steps

When this skill is invoked, immediately execute the following actions:

### 1. Verify Git Repository

```bash
# Check if current directory is a git repository
git rev-parse --is-inside-work-tree
```

If not a git repo, exit with message: "Not a git repository. This skill requires git."

### 2. Gather Change Information

Execute these commands in parallel:

```bash
# Get status of all files
git status --porcelain

# Get unstaged changes
git diff

# Get staged changes
git diff --cached

# Get list of modified files
git diff --name-only HEAD

# Get recent commits for context
git log --oneline -5
```

### 3. Read Current Documentation

Read these files (if they exist):
- `CHANGELOG.md` - to understand format and add new entries
- `CLAUDE.md` - to check if structural updates needed
- `.gitignore` - to understand project patterns

### 4. Analyze Changes

Based on the git diff output:

**Categorize changes:**
- New files → "Added"
- Modified files → "Changed" or "Fixed" (analyze diff content)
- Deleted files → "Removed"
- Build files (pom.xml, build.gradle, package.json) → May need CLAUDE.md update
- Config files → May need CLAUDE.md update

**Filter out excluded changes:**
- `.idea/`, `.iml` files
- `.gitignore`, `.gitattributes`
- `*.md` files (documentation only)
- Whitespace-only changes

**Determine documentation needs:**
- If substantive code changes exist → Update CHANGELOG.md
- If build/structure changes exist → Update CLAUDE.md

### 5. Update CHANGELOG.md

If CHANGELOG.md doesn't exist, create it:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

```

If it exists, find or create the `## [Unreleased]` section.

**Add entries under appropriate categories:**
- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

**Rules:**
- Maximum 3 sentences per entry
- Start with action verb (Add, Fix, Change, Remove, etc.)
- Focus on WHAT changed and WHY
- One entry per logical change

**Example:**
```markdown
## [Unreleased]

### Added
- Implement circular gesture navigation for tag selection. Optimized for small watch screens with touch-friendly hit areas.

### Fixed
- Resolve NullPointerException when database is empty on first launch. Added initialization checks in DataRepository.
```

### 6. Update CLAUDE.md (Conditional)

Only update if changes include:
- New build files or dependencies
- Project structure changes (new directories)
- New workflows or commands
- Architecture changes

Update relevant sections:
- Project Configuration
- Development Setup
- Project Structure
- Development Workflow

### 7. Stage Updated Files

```bash
git add CHANGELOG.md
git add CLAUDE.md  # only if modified
```

Verify with:
```bash
git status --porcelain
```

### 8. Report Results

Show the user:
- What files were analyzed
- What changes were detected
- What documentation was updated
- What entries were added to CHANGELOG.md
- What files are now staged

## Implementation Notes

**Use tools, not instructions:**
- ✅ Execute `Bash` tool to run git commands
- ✅ Use `Read` tool to read existing documentation
- ✅ Use `Edit` tool to update files precisely
- ✅ Use `Grep` tool to search for patterns if needed
- ❌ Don't just tell the user to run commands

**Be autonomous:**
- Make decisions based on the actual changes seen
- Don't ask for permission for standard documentation updates
- Handle missing files gracefully
- Create CHANGELOG.md if it doesn't exist

**Be accurate:**
- Parse git diff output to understand actual changes
- Match existing CHANGELOG.md style and formatting
- Preserve existing content exactly
- Don't hallucinate changes

## Quality Standards

**Changelog Entries:**
- Concise (≤3 sentences)
- Descriptive (explain what and why)
- Properly categorized
- Chronologically ordered (newest first in category)

**CLAUDE.md Updates:**
- Only when structurally necessary
- Maintain existing style
- Update specific sections, not entire file
- Keep accurate with code reality

## Error Handling

If git commands fail:
- Report exact error
- Suggest resolution
- Don't continue with bad data

If files can't be read:
- Report specific file issue
- Continue with available data
- Create missing files if appropriate

If no changes detected:
- Report "No uncommitted changes found"
- Exit gracefully

## Success Criteria

✅ Git repository verified
✅ All changes analyzed
✅ CHANGELOG.md updated with new entries
✅ CLAUDE.md updated if needed
✅ Documentation files staged
✅ User informed of updates
