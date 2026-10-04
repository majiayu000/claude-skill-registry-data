---
name: changelog
description: Generate a changelog entry in HISTORY.md from git changes. Use when user requests changelog, version update, or history entry.
disable-model-invocation: true
---

# Changelog Generation Skill

Generate a changelog entry in HISTORY.md based on recent git changes.

## Workflow

Follow these steps to create a changelog entry:

### 1. Get Git Changes

Try to get git changes using one of these approaches:
- For uncommitted changes: `git diff HEAD`
- For last commit: `git log -1 --stat`
- For changes between commits: `git diff <commit1> <commit2> --stat`

If git is not available, ask the user what changes were made.

### 2. Read Current Version

Read `HISTORY.md` and extract the latest version number at the top of the file.
- Format: `# X.Y.Z Title`
- Example: `# 0.1.0 Initial project setup`

### 3. Increment Version

Increase the **minor** version (Y) by 1 and reset the **patch** (Z) to 0:
- `0.1.0` → `0.2.0`
- `0.2.5` → `0.3.0`
- `1.9.0` → `1.10.0`

### 4. Analyze Changes

Categorize the changes into one or more of these sections:
- **Added**: New features, files, or capabilities
- **Changed**: Modifications to existing functionality
- **Removed**: Deleted features or files
- **Fixed**: Bug fixes or corrections

Summarize each change in **5-12 words**.

### 5. Generate Entry

Create a new entry at the **TOP** of HISTORY.md with this format:

```markdown
# {version} {5-word title}

## {Section}
- {change description 5-12 words}
- {change description 5-12 words}
- {change description 5-12 words}

{blank line before previous entry}
```

## Constraints

- **Title**: Maximum 5 words describing the main change
- **Bullet points**: Maximum 5 items
- **Bullet length**: 5-12 words each
- **Sections**: Use one or more of: Added, Changed, Removed, Fixed
- **Placement**: New entry goes at the TOP of the file
- **Spacing**: One blank line between entries

## Example Output

```markdown
# 0.3.0 Added user authentication system

## Added
- User login and registration endpoints
- JWT token generation and validation
- Password hashing with bcrypt
- Session management middleware

# 0.2.0 Database integration complete

## Added
- PostgreSQL database connection pool
- Migration system with versioning
```

## Notes

- If git is unavailable, work with the user to identify changes
- Focus on user-facing changes, not internal refactoring
- Keep descriptions clear and concise
- Always preserve existing changelog entries below

