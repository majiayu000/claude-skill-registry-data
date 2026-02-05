---
name: git-commit-formatter
description: Format git commits with proper standards, signatures, and conventional commit format. Use when user says "commit", "create commit", "format commit message", or when staging changes for commit.
allowed-tools: Bash, Read
---

# Git Commit Formatter

## When to Use

Activate this skill when:
- User requests to "commit" changes
- User asks to "create a commit message"
- User says "stage and commit"
- User mentions "git commit" or "commit with message"
- User wants to follow commit message standards
- User needs a properly formatted commit signature

## Instructions

### Step 1: Gather Context
1. Run `git status` to see all untracked and modified files
2. Run `git diff` to see unstaged changes
3. Run `git diff --staged` to see already staged changes
4. Run `git log --oneline -5` to see recent commit message style

### Step 2: Analyze Changes
1. Review all changes comprehensively
2. Identify the type of change:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation only
   - `style:` - Code style/formatting
   - `refactor:` - Code refactoring
   - `test:` - Adding/updating tests
   - `chore:` - Build process, dependencies
   - `perf:` - Performance improvement

### Step 3: Draft Commit Message
Format:
```
<type>: <short summary>

<detailed explanation if needed>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Step 4: Stage and Commit
1. Stage relevant files: `git add <files>`
2. Commit with message using heredoc:
```bash
git commit -m "$(cat <<'EOF'
feat: add user authentication

Implement OAuth 2.0 flow with Google provider
- Add login/logout buttons
- Store user session in Firebase
- Protect authenticated routes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```
3. Run `git status` to verify

### Step 5: Handle Pre-commit Hooks
If commit fails due to pre-commit hook changes:
1. Check authorship: `git log -1 --format='%an %ae'`
2. Check not pushed: `git status` shows "Your branch is ahead"
3. If both true: amend the commit
4. Otherwise: create NEW commit

## Examples

### Example 1: Feature Addition
```bash
# Context: Added new search functionality
git commit -m "$(cat <<'EOF'
feat: implement search functionality

Add full-text search across posts and comments
- Integrate Algolia search API
- Add search bar to navigation
- Display results with highlighting

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Example 2: Bug Fix
```bash
# Context: Fixed authentication redirect
git commit -m "$(cat <<'EOF'
fix: resolve authentication redirect loop

Prevent infinite redirect when session expires
- Check token validity before redirect
- Clear stale session data
- Add error boundary

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Example 3: Documentation
```bash
# Context: Updated README
git commit -m "$(cat <<'EOF'
docs: update installation instructions

Add troubleshooting section and environment setup guide

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## Best Practices

### ✅ DO:
- Always check `git status` and `git diff` first
- Use conventional commit format (`type: description`)
- Focus on "why" rather than "what" in detailed explanation
- Include Claude Code signature
- Use heredoc for multi-line messages
- Ask before committing if unclear about changes
- Keep first line under 72 characters
- Verify commit with `git status` after

### ❌ DON'T:
- Never commit without reviewing changes first
- Never commit files with secrets (.env, credentials.json)
- Never use `git commit --amend` unless fixing pre-commit hook changes
- Never commit unless explicitly requested by user
- Don't use vague messages like "update files" or "fix stuff"
- Don't commit generated files (node_modules, dist, build)

### Conventional Commit Types:
- **feat**: New feature for user
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons (no code change)
- **refactor**: Code restructuring (no behavior change)
- **perf**: Performance improvement
- **test**: Adding/updating tests
- **build**: Build system changes
- **ci**: CI/CD changes
- **chore**: Maintenance tasks, dependencies

### Commit Message Guidelines:
1. First line: Imperative mood ("add" not "added")
2. First line: No period at end
3. Body: Wrap at 72 characters
4. Body: Explain what and why, not how
5. Always include Claude signature block

## Safety Checks

Before committing:
- [ ] No sensitive data (API keys, passwords, tokens)
- [ ] No large binary files
- [ ] No node_modules or dist folders
- [ ] Changes align with commit message
- [ ] User explicitly requested commit
- [ ] Pre-commit hooks passed (or handled)

## Troubleshooting

**Issue**: Pre-commit hook modified files
**Solution**: Check authorship and amend if safe, otherwise create new commit

**Issue**: Large diff, unclear what to commit
**Solution**: Ask user which changes to include

**Issue**: Multiple unrelated changes
**Solution**: Suggest separate commits for different concerns

**Issue**: Unclear commit type
**Solution**: Default to `chore:` or ask user for clarification
