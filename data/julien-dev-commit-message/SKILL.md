---
name: julien-dev-commit-message
description: "Generate semantic commit messages and create git commits. Handles OneDrive mmap errors automatically. Use when user wants to commit, needs a commit message, or git commit fails."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "2.0.0"
  category: "development"
triggers:
  # English - Keywords
  - "commit"
  - "git commit"
  - "commit message"
  - "commit changes"
  # English - Actions
  - "make a commit"
  - "create a commit"
  - "write commit message"
  - "generate commit"
  - "help me commit"
  - "commit my changes"
  - "commit this"
  - "commit these changes"
  - "stage and commit"
  # French - Keywords
  - "commiter"
  - "committer"
  - "message de commit"
  # French - Actions
  - "faire un commit"
  - "créer un commit"
  - "écrire un message de commit"
  - "committer les changements"
  - "commiter mes changements"
  - "aide moi à commiter"
  - "génère un commit"
  # Error handling
  - "mmap failed"
  - "git error"
  - "commit failed"
  - "onedrive git"
allowed-tools:
  - Bash
  - Read
---

# Commit Message Generator

Generate semantic commit messages and create git commits. Automatically handles OneDrive mmap errors.

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-dev-commit-message" activated
```

## Quick Reference

```
<type>(<scope>): <description max 50 chars>

<body explaining why>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code restructure (no functional change) |
| `style` | Formatting (no code change) |
| `test` | Adding/updating tests |
| `chore` | Maintenance, dependencies |

## Execution Process

### Step 1: Analyze Changes

```bash
git status
git diff --cached --stat
git diff --cached
git log --oneline -5
```

### Step 2: Generate Message

1. Identify **type** from changes (feat/fix/docs/etc.)
2. Identify **scope** from file paths
3. Write **description** (≤50 chars, imperative mood)
4. Write **body** explaining WHY (not what)

### Step 3: Present to User

```markdown
## Proposed Commit

\`\`\`
feat(api): add user authentication endpoint

- Implemented JWT token generation
- Added password hashing with bcrypt
- Created login/logout routes

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
\`\`\`

**Ready to commit?** Run:
\`\`\`bash
git add -A && git commit -m "$(cat <<'EOF'
feat(api): add user authentication endpoint

- Implemented JWT token generation
- Added password hashing with bcrypt
- Created login/logout routes

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
\`\`\`
```

### Step 4: Wait for Approval

**NEVER commit automatically.** Always wait for user to execute the command.

## OneDrive Error Handling

If `git commit` fails with `fatal: mmap failed: Invalid argument`:

### Automatic Detection

Check if repo is in OneDrive:
```bash
pwd | grep -i onedrive && echo "OneDrive detected"
```

### Workaround: Git Plumbing Commands

```bash
# 1. Configure memory limits
git config core.packedGitWindowSize 1m
git config pack.windowMemory 1m

# 2. Create blob objects
SHA=$(git hash-object -w path/to/file)

# 3. Update index
git update-index --add --cacheinfo 100644,$SHA,path/to/file

# 4. Create tree
TREE=$(git write-tree)

# 5. Get parent
PARENT=$(git rev-parse HEAD)

# 6. Create commit
COMMIT=$(echo "your message" | git commit-tree $TREE -p $PARENT)

# 7. Update branch
git update-ref refs/heads/$(git branch --show-current) $COMMIT
```

### Alternative

If plumbing fails, recommend:
- Git GUI (included with Git for Windows)
- GitHub Desktop
- VSCode Source Control

## Security Checks

**Warn if staged files contain:**
- `.env` files
- `credentials.json`
- API keys, tokens
- Private keys (`.pem`, `.key`)

## Checklist

Before presenting:
- [ ] Type matches changes
- [ ] Description ≤50 chars, imperative mood
- [ ] Body explains WHY
- [ ] No secrets in staged files
- [ ] Attribution included
- [ ] Command provided (not auto-committed)

## Skill Chaining

### Input Expected
- Git repository with staged or unstaged changes

### Output Produced
- **Format**: Commit message + git command to execute
- **Side effects**: None until user executes command

### Tools Used
- `Bash` (git status, git diff, git log)
- `Read` (if needed to understand file changes)
