---
name: setup-cdk-git
description: Use when setting up git workflows for Claude Code - installs pre-commit hooks, commit templates with Claude attribution, PR templates, branch naming helpers, and Claude-specific gitignore entries
---

# Setup CDK Git

## Overview

Git workflow configuration optimized for Claude Code development. Installs hooks, templates, and conventions for consistent AI-assisted commits and PRs.

## When to Use

- Setting up git workflows for Claude development
- User asks about commit conventions or PR templates
- Part of `setup-claude-dev-kit` bundle
- User wants pre-commit hooks or Claude attribution

## Quick Reference

| Component | Location |
|-----------|----------|
| Commit Template | `~/.gitmessage` |
| Global Hooks | `~/.config/git/hooks/` |
| Project Hooks | `.git/hooks/` or `.husky/` |
| PR Template | `.github/pull_request_template.md` |
| Gitignore | `~/.gitignore_global` |

## Installation Steps

### 1. Configure Git User (if needed)

```bash
# Check if configured
git config --global user.name || echo "Name not set"
git config --global user.email || echo "Email not set"

# Set if empty
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 2. Install Commit Message Template

Create `~/.gitmessage`:

```bash
cat > ~/.gitmessage << 'EOF'
# <type>(<scope>): <subject>
#
# Types: feat, fix, docs, style, refactor, test, chore
# Scope: component affected (optional)
# Subject: imperative, no period, <50 chars
#
# Body: explain what and why (wrap at 72 chars)
#


# Footer: references, breaking changes, co-authors
#
# Co-Authored-By: Claude <noreply@anthropic.com>
EOF

git config --global commit.template ~/.gitmessage
```

### 3. Configure Global Gitignore

Create `~/.gitignore_global`:

```bash
cat > ~/.gitignore_global << 'EOF'
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*

# Editors
*.swp
*.swo
*~
.idea/
.vscode/
*.sublime-*

# Claude artifacts
.claude/memory/
.claude-context/
*.claude-session

# Environment files (safety)
.env.local
.env.*.local
*.pem
*.key
EOF

git config --global core.excludesfile ~/.gitignore_global
```

### 4. Install Pre-commit Hook Framework

**Option A: Simple bash hooks (no dependencies)**

```bash
mkdir -p ~/.config/git/hooks

cat > ~/.config/git/hooks/pre-commit << 'EOF'
#!/bin/bash
# CDK Pre-commit Hook

# Check for debug statements
if git diff --cached --name-only | xargs grep -l "console.log\|debugger\|print(" 2>/dev/null; then
  echo "Warning: Debug statements found. Continue? (y/n)"
  read -r response
  [[ "$response" != "y" ]] && exit 1
fi

# Check for large files
MAX_SIZE=5000000  # 5MB
for file in $(git diff --cached --name-only); do
  if [ -f "$file" ]; then
    size=$(wc -c < "$file")
    if [ "$size" -gt "$MAX_SIZE" ]; then
      echo "Error: $file is larger than 5MB"
      exit 1
    fi
  fi
done

exit 0
EOF

chmod +x ~/.config/git/hooks/pre-commit
git config --global core.hooksPath ~/.config/git/hooks
```

**Option B: Using Husky (for Node.js projects)**

```bash
# In project directory
npm install --save-dev husky
npx husky init

# Add hook
echo 'npm test' > .husky/pre-commit
```

### 5. Install Commit-msg Hook (Conventional Commits)

```bash
cat > ~/.config/git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Validate conventional commit format

commit_regex='^(feat|fix|docs|style|refactor|test|chore|build|ci)(\(.+\))?: .{1,50}'

if ! grep -qE "$commit_regex" "$1"; then
  echo "Error: Commit message doesn't follow conventional format."
  echo "Expected: <type>(<scope>): <subject>"
  echo "Types: feat, fix, docs, style, refactor, test, chore, build, ci"
  echo ""
  echo "Your message:"
  cat "$1"
  exit 1
fi
EOF

chmod +x ~/.config/git/hooks/commit-msg
```

### 6. Create PR Template

For GitHub, create `.github/pull_request_template.md`:

```markdown
## Summary

<!-- Brief description of changes -->

## Changes

-

## Test Plan

- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regressions introduced

## Screenshots

<!-- If applicable -->

## Checklist

- [ ] Code follows project style
- [ ] Self-reviewed my changes
- [ ] Added/updated documentation
- [ ] No secrets or credentials included

---
Generated with Claude Code
```

### 7. Configure Helpful Aliases

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# Claude-friendly aliases
git config --global alias.wip 'commit -am "wip: work in progress"'
git config --global alias.undo 'reset --soft HEAD~1'
git config --global alias.amend 'commit --amend --no-edit'
```

### 8. Branch Naming Helper

Add to shell config (`~/.zshrc` or `~/.bashrc`):

```bash
# Branch naming helper
newbranch() {
  local type=$1
  local name=$2
  local branch="${type}/${name}"

  if [[ -z "$type" || -z "$name" ]]; then
    echo "Usage: newbranch <type> <name>"
    echo "Types: feature, fix, docs, refactor, test"
    echo "Example: newbranch feature user-auth"
    return 1
  fi

  git checkout -b "$branch"
  echo "Created and switched to: $branch"
}
```

## Verification

```bash
# Check global config
git config --global --list | grep -E "(template|excludes|hooks)"

# Check commit template
[ -f ~/.gitmessage ] && echo "Commit template installed"

# Check hooks
[ -x ~/.config/git/hooks/pre-commit ] && echo "Pre-commit hook installed"
[ -x ~/.config/git/hooks/commit-msg ] && echo "Commit-msg hook installed"

# Test conventional commit validation
echo "bad commit" | git commit --dry-run -F - 2>&1 | grep -q "Error" && echo "Commit validation working"
```

## Adaptation Mode

When existing git setup detected:

1. **Backup configs:**
```bash
mkdir -p ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)
cp ~/.gitconfig ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/gitconfig.bak 2>/dev/null
cp ~/.gitmessage ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/gitmessage.bak 2>/dev/null
```

2. **Check for conflicts:**
- Existing commit template → Merge Claude attribution
- Custom hooks path → Add CDK hooks alongside
- Project-level .husky → Don't override with global hooks

3. **Merge, don't replace:**
```bash
# Append Claude co-author to existing template
echo "" >> ~/.gitmessage
echo "# Co-Authored-By: Claude <noreply@anthropic.com>" >> ~/.gitmessage
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Hooks not running | Check `core.hooksPath` config and permissions |
| Commit rejected | Verify message follows conventional format |
| Template not showing | Ensure `commit.template` is set correctly |
| Large file blocked | Use Git LFS or adjust hook threshold |
| Husky conflicts | Choose either global hooks OR husky, not both |

## Updating

```bash
# Re-run setup to update hooks
# CDK updates hooks in place

# For husky projects
npm update husky
```

## Hook Reference

| Hook | Purpose |
|------|---------|
| pre-commit | Check for debug statements, large files |
| commit-msg | Validate conventional commit format |
| pre-push | (Optional) Run tests before push |

## Commit Types

| Type | Use For |
|------|---------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Formatting, no code change |
| refactor | Code change, no feature/fix |
| test | Adding/updating tests |
| chore | Build, deps, tooling |
| build | Build system changes |
| ci | CI configuration |
