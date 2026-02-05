---
name: git-secret-scan
description: Scan git changes for secrets and credentials before commit
metadata:
  category: security
  workflow: pre-commit
---

## Quick Scan Checklist

1. [ ] Scan `git diff --staged` for secrets → **CRITICAL** if found
2. [ ] Scan `git diff` for secrets → **HIGH** if found
3. [ ] Check untracked filenames against sensitive patterns
4. [ ] Verify .gitignore coverage for detected files
5. [ ] If any CRITICAL/HIGH issues → **STOP** and report

## Required Context

This skill expects:
- `git diff --staged` (staged changes)
- `git diff` (unstaged changes)
- `git ls-files --others --exclude-standard` (untracked)
- Optionally: `git log -p origin/main..HEAD` (unpushed commits)

## What I do

I scan git changes (staged, unstaged, untracked, and unpushed commits) for sensitive information that should NOT be committed to version control. I detect credentials, keys, tokens, and other secrets, then provide specific remediation steps.

## When to use me

Use this skill when:
- Planning git commits to ensure no secrets are included
- Reviewing pull requests for security issues
- Auditing repositories for leaked credentials
- Before pushing changes to remote repositories

## Detection Patterns

### Common Secret Patterns (Regex)

| Type | Pattern | Example |
|------|---------|---------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | `AKIAIOSFODNN7EXAMPLE` |
| AWS Secret | `[A-Za-z0-9/+=]{40}` | 40-char base64 string |
| GitHub Token | `gh[pousr]_[A-Za-z0-9_]{36,}` | `ghp_xxxx...` |
| Private Key | `-----BEGIN.*PRIVATE KEY-----` | RSA/SSH/PEM |
| Generic Secret | `(api[_-]?key|secret|token|password)\s*[:=]` | `API_KEY=xxx` |

### Content Patterns (in diffs and file contents)
Scan for these patterns in actual file content:
- **API keys, tokens, secrets**: Long alphanumeric strings (20+ chars), base64-encoded data
- **OAuth tokens**: `refreshToken`, `accessToken`, `auth_token`, `bearer_token`
- **Passwords and credentials**: `password=`, `pwd=`, `credential=`, `secret=`
- **Project IDs paired with tokens**: Look for combinations like `projectId` + `refreshToken`

### Filename Patterns (for untracked/changed files)
Flag files matching these patterns:
- `*.env`, `.env`, `.env.*`, `.env.local`, `.env.production`
- `*secret*`, `*credential*`, `*token*`, `*password*`
- `*-accounts.json`, `*-auth.json`, `credentials.*`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa`, `id_ed25519`, `id_dsa`
- `config/master.key`, `config/credentials.yml.enc`

### Examples of Sensitive Data
```json
{
  "refreshToken": "1//abc123def456EXAMPLE_TOKEN_NOT_REAL_xyz789...",
  "projectId": "example-project-abc123"
}
```

```env
API_KEY=sk_live_YOUR_STRIPE_SECRET_KEY_HERE
DATABASE_URL=postgresql://user:password@localhost/db
```

## Exceptions (Not Secrets)

Do NOT flag as issues:
- **Placeholders**: `API_KEY=your-key-here`, `password=changeme`, `<TOKEN>`
- **Example files**: `.env.example`, `config.sample.json`
- **Test fixtures**: Mock data in `test/`, `__tests__/`, `*_test.go`
- **Documentation**: Secret patterns mentioned in README, docs, comments
- **Hash values**: Git SHAs, checksums, file hashes
- **Encoded but not secret**: JWT structure without actual signing key

## Severity Levels

### 1. CRITICAL
- Sensitive data in **staged changes** (about to be committed)
- **Impact**: Will be committed to git history if not stopped
- **Action**: STOP immediately, unstage the file

### 2. HIGH
- Sensitive data in **unstaged changes**
- **Impact**: Not yet staged, but could be accidentally committed
- **Action**: Add to .gitignore before staging

### 3. SEVERE
- Sensitive data in **unpushed commits** (already committed locally)
- **Impact**: In git history, will be pushed to remote if not fixed
- **Action**: Rewrite git history to remove

### 4. INFO
- Files that should be in .gitignore but aren't
- **Impact**: Risk of future accidental commits
- **Action**: Add pattern to .gitignore

## Remediation Steps

### For CRITICAL (staged sensitive files)
```bash
# Unstage the file
git reset HEAD <file>

# Add to .gitignore
echo "<pattern>" >> .gitignore

# Stage the .gitignore change
git add .gitignore
```

### For HIGH (unstaged sensitive files)
```bash
# Add to .gitignore BEFORE staging
echo "<pattern>" >> .gitignore

# Verify it's ignored
git status --ignored
```

### For SEVERE (unpushed commits with secrets)
```bash
# If the secret is in the last N commits (not yet pushed)
git reset --soft HEAD~N

# Fix the issue (add to .gitignore, remove sensitive data)
echo "<pattern>" >> .gitignore

# Re-commit without the sensitive data
git add .
git commit -m "Your commit message"
```

### For INFO (.gitignore updates)
```bash
# Add the pattern to .gitignore
echo "<pattern>" >> .gitignore

# If the file was already tracked, untrack it
git rm --cached <file>

# Commit the .gitignore update
git add .gitignore
git commit -m "chore: ignore sensitive files"
```

## .gitignore Coverage Check

For each sensitive file or pattern detected:
1. Check if it matches any existing .gitignore rule
2. If NOT matched, flag as "missing from .gitignore"
3. Suggest the exact line to add to .gitignore

### Common .gitignore Patterns for Security
```gitignore
# Environment variables
.env
.env.*
!.env.example

# Credentials and secrets
*secret*
*credential*
*-accounts.json
*.key
*.pem

# SSH keys
id_rsa
id_ed25519
id_dsa

# Application-specific
config/master.key
config/credentials.yml.enc
```

## Output Format

When I detect issues, I provide a structured report:

```
## Security Scan Results

### CRITICAL - Staged Changes
- `auth-accounts.json` contains refreshToken
  Remediation: git reset HEAD auth-accounts.json && echo "*-accounts.json" >> .gitignore

### HIGH - Unstaged Changes
- None detected

### SEVERE - Unpushed Commits
- None detected

### INFO - Missing .gitignore entries
- Add `*-accounts.json` to .gitignore
- Add `*.env` to .gitignore

```

If no issues are found:
```
No sensitive data detected. Safe to proceed.
```

## Best Practices

- Always scan before committing; never commit secrets
- Use .env.example for templates; rotate any compromised credentials immediately
