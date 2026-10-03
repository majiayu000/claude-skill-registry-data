---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI."
allowed-tools:
  - bash
enabled: true
related-skills: [github-pr-workflow, github-code-review, github-issues]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT)
---

# GitHub Authentication Setup

Sets up authentication so the agent can work with GitHub repositories, PRs,
issues, and CI.

## Detection Flow

When a user asks to work with GitHub, run this check first:

```bash
git --version
gh --version 2>/dev/null || echo "gh not installed"
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → use `gh` for everything
2. If `gh` installed but not authenticated → use "gh auth" method
3. If `gh` not installed → use "git-only" method

## Method 1: Git-Only (No gh)

### HTTPS with Personal Access Token (Recommended)

**Step 1: Create a token** at https://github.com/settings/tokens (classic)
or https://github.com/settings/personal-access-tokens (fine-grained). Scope:
`repo`, `workflow`, `read:org`.

**Step 2: Configure git credential helper:**

```bash
# Store credentials (plaintext, dev machine only)
git config --global credential.helper store

# Or use a credential cache (timed, more secure)
git config --global credential.helper 'cache --timeout=3600'
```

**Step 3: First push triggers prompt:**
```bash
# Username: your GitHub username
# Password: paste your token (not your GitHub password)
git push origin main
```

**Step 4 (optional): Set token as env var for API calls:**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
# Add to .env for persistence
```

### SSH Keys

```bash
# Generate key (if no existing key)
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519_github

# Start ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github

# Copy public key
cat ~/.ssh/id_ed25519_github.pub
# Paste at https://github.com/settings/keys

# Test
ssh -T git@github.com

# Set remote to SSH
git remote set-url origin git@github.com:owner/repo.git
```

## Method 2: gh CLI

```bash
# Install gh (if not present)
# macOS: brew install gh
# Linux: see https://github.com/cli/cli#installation
# Windows: winget install GitHub.cli

# Authenticate
gh auth login
# Follow prompts: choose HTTPS or SSH, authenticate via browser or token

# Verify
gh auth status

# Use gh for everything
gh repo clone owner/repo
gh pr create
gh issue list
```

## Verification

```bash
# Test git auth
git ls-remote origin

# Test gh auth
gh api user --jq '.login'

# Test API token
curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | python3 -c "import sys,json; print(json.load(sys.stdin)['login'])"
```

## Common Auth Setup Block

Many skills need owner/repo. Use this reusable block:

```bash
# Determine auth method
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
fi

# Extract owner/repo from remote
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## Pitfalls

- **2FA**: HTTPS with password no longer works (GitHub requires token). Use
  personal access token, not password.
- **Token expiry**: fine-grained tokens expire. Check `gh auth status` or
  `curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`.
- **SSH on Windows**: use `ssh-keygen` in Git Bash or PowerShell (OpenSSH
  client built into Windows 10+).
- **Credential helper on Windows**: `git config --global credential.helper
  manager` uses Windows Credential Manager.
- **Rate limits**: unauthenticated API calls limited to 60/hour. Use token for
  5000/hour.
