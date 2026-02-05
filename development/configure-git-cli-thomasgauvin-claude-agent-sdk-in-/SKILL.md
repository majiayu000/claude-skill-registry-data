---
name: configure-git-cli
description: Configure Git CLI with GitHub authentication using environment variables (GITHUB_EMAIL, GITHUB_NAME, GITHUB_PAT)
compatibility: Requires git installed and GITHUB_EMAIL, GITHUB_NAME, GITHUB_PAT environment variables set
license: MIT
---

# Configure Git CLI

## When to use this skill

Use this skill before performing git operations (clone, push, commit, etc.). Required by the `codebase-fix-and-pr` skill.

## Prerequisites

**Required environment variables:**
- `GITHUB_EMAIL`: Email address for git commits
- `GITHUB_NAME`: Name for git commits
- `GITHUB_PAT`: GitHub Personal Access Token with repo and workflow scopes

## Workflow

### Step 1: Verify Git Installation

```bash
git --version
```

### Step 2: Configure Git User Identity

```bash
git config --global user.email "${GITHUB_EMAIL}"
git config --global user.name "${GITHUB_NAME}"
```

### Step 3: Configure Credentials

Enable credential storage and preload GitHub credentials:

```bash
git config --global credential.helper store
cat <<EOF > ~/.git-credentials
https://${GITHUB_NAME}:${GITHUB_PAT}@github.com
EOF
chmod 600 ~/.git-credentials
```

### Step 4: Verify Configuration

```bash
git config user.email
git config user.name
git ls-remote https://github.com/test/test.git
```

All commands should succeed without prompting for credentials.

## Success Criteria

- ✅ `git --version` succeeds
- ✅ `git config user.email` and `git config user.name` return correct values
- ✅ `git ls-remote` succeeds without prompting

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Git not found | Install git using your system package manager |
| Authentication failed | Verify GITHUB_PAT is valid, not expired, and has repo scope |
| Permission denied | Check write permissions to home directory |
| Credentials not working | Run `rm ~/.git-credentials` and reconfigure |
