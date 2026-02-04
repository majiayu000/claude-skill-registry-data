---
name: gh-auth
description: Automatically authenticate GitHub CLI using .gh-token.txt when seeing errors about "gh auth login", "GH_TOKEN environment variable", or "not logged into any GitHub hosts"
allowed-tools:
  - Bash
---

# GitHub CLI Authentication

Automatically authenticate `gh` CLI using the token from `.gh-token.txt` in the repository root.

## When to Use

Use this skill when:
- Seeing authentication errors: "gh auth login", "GH_TOKEN environment variable", "not logged into any GitHub hosts"
- Before running `gh` commands if auth status is uncertain
- User explicitly requests GitHub authentication

## Authentication Steps

### 1. Get repo root and authenticate

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
gh auth login --with-token < "$REPO_ROOT/.gh-token.txt"
```

### 2. Verify success

```bash
gh auth status
```

Should show: `✓ Logged in to github.com account <username>`

### 3. Proceed with original task

If authentication was triggered by a failed command, retry that command.

## Error Handling

**Missing `.gh-token.txt`**:
```
ERROR: .gh-token.txt not found in repository root

Create it:
1. Generate token: https://github.com/settings/tokens
2. Save to .gh-token.txt in repo root
3. File is git-ignored
```

**Invalid token format**:
```
ERROR: Invalid token format

Tokens should start with github_pat_ or ghp_
Check .gh-token.txt for correct token
```

**Already authenticated**:
If `gh auth status` shows active authentication, skip to the original task.

## Example

**User**: "List pull requests"

**Action**:
1. Run `gh pr list` → authentication error
2. Detect error → activate skill
3. Run: `REPO_ROOT=$(git rev-parse --show-toplevel) && gh auth login --with-token < "$REPO_ROOT/.gh-token.txt"`
4. Verify: `gh auth status` → success
5. Retry: `gh pr list` → returns PR list

## Security

- Token read via stdin (never in command args or history)
- `.gh-token.txt` should be in `.gitignore`
- Tokens masked in `gh auth status` output
