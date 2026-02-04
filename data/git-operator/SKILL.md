---
name: git-operator
description: Rules and procedures for Git operations (add, branch, commit, push). Use when performing git add, git commit, git push, or creating branches.
---

# Git Operator

This skill defines rules and procedures for Git operations.

## Prohibited Operations

The following operations must never be performed.

### git commit --amend

Do not modify commits once created. Address issues with new commits.

```bash
# Prohibited
git commit --amend
git commit --amend -m "..."
```

### git push --force

Force push is prohibited.

```bash
# Prohibited
git push --force
git push -f
git push --force-with-lease
```

### Other History-Rewriting Operations

The following operations are also prohibited.

- `git rebase` operations that rewrite history
- `git reset --hard` operations that erase history
- Any other operations that modify pushed commits

These operations rewrite Git history and cause problems in collaborative work: other developers' work may be lost, history integrity may be compromised, and merge conflicts become more likely.

Once a commit is pushed, fix issues with new commits instead of modifying history.

---

## Staging

Stage only task-related files. Do not use `git add .` or `git add -A` without explicit confirmation.

```bash
git status                  # Run this first
git add <file>              # Stage specific files
```

Before staging, verify:
- No secrets (.env, credentials.json, API keys)
- No unrelated changes included

## Branch Creation

Branch names must be in kebab-case.

Good: `add-user-authentication`, `fix-login-bug`, `update-readme`
Bad: `addUserAuthentication`, `Add_User_Auth`, `ADD-USER-AUTH`

```bash
git switch -c <branch-name>
```

## Commit

Follow Conventional Commits format.

```
<type>(<scope>): <description>

[optional body]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: Code changes that neither fix a bug nor add a feature
- `perf`: Code changes that improve performance
- `test`: Adding or modifying tests
- `build`: Changes that affect the build system or external dependencies
- `ci`: Changes to CI configuration files or scripts
- `chore`: Other changes (not modifying src or test)

### Procedure

Analyse staged changes to create a message focusing on "why" rather than "what".

```bash
git diff --cached           # Review staged changes
git commit -m "<type>(<scope>): <description>"
```

Good example:
```
fix(auth): prevent session timeout on mobile

Users reported being logged out after 5 minutes on mobile.
Root cause was incorrect token refresh interval.
```

Bad example:
```
fixed bug
```

For multi-line messages, use HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body>
EOF
)"
```

## Push

### Pre-push Verification

Run these commands before pushing:

```bash
git log --oneline -5        # Verify recent commits
git branch -vv              # Verify current branch and tracking
git status                  # Ensure working directory is clean
```

Proceed only after reviewing the output.

### Procedure

For new branches:

```bash
git push -u origin <branch-name>
```

For existing remote tracking branches:

```bash
git push
```
