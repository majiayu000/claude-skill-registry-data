---
name: "remote-git-operations"
description: 'Manage remote Git operations including GitHub, Azure DevOps, pull requests, CI/CD integration, and branch protection. Use when configuring remote repositories, setting up authentication, managing pull request workflows, integrating with CI/CD pipelines, or troubleshooting Git remote issues.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 platforms: ["github", "azure-devops"]
---

# Remote Git Repository Operations

> **Purpose**: Best practices for working with remote Git repositories, including GitHub, Azure DevOps, GitLab, and Bitbucket.

---

## When to Use This Skill

- Configuring remote Git repositories and authentication
- Managing pull request workflows across platforms
- Resolving conflicts between local and remote branches
- Integrating Git with CI/CD pipelines
- Working with Git LFS for large files

## Prerequisites

- Git 2.30+ installed
- Remote repository access (GitHub, Azure DevOps, GitLab, etc.)

## Remote Repository Setup

### Adding and Managing Remotes

```bash
# View existing remotes
git remote -v

# Add a new remote
git remote add origin https://github.com/username/repo.git
git remote add upstream https://github.com/original/repo.git

# Change remote URL
git remote set-url origin https://github.com/username/new-repo.git

# Remove a remote
git remote remove upstream

# Rename a remote
git remote rename origin main-repo

# Fetch remote information
git remote show origin
```

### Clone Strategies

```bash
# Standard clone
git clone https://github.com/username/repo.git

# Clone with different folder name
git clone https://github.com/username/repo.git my-project

# Clone specific branch
git clone -b develop https://github.com/username/repo.git

# Shallow clone (faster, less history)
git clone --depth 1 https://github.com/username/repo.git

# Clone with submodules
git clone --recursive https://github.com/username/repo.git

# Clone using SSH
git clone git@github.com:username/repo.git
```

---

## Troubleshooting Common Issues

### "Your branch is ahead/behind origin"

```bash
# View differences
git log origin/main..HEAD # Commits you have but remote doesn't
git log HEAD..origin/main # Commits remote has but you don't

# Sync with remote
git pull --rebase origin main
git push origin main
```

### "Failed to push: rejected"

```bash
# Fetch latest changes first
git fetch origin

# Option 1: Merge (creates merge commit)
git merge origin/main
git push origin main

# Option 2: Rebase (cleaner history)
git rebase origin/main
git push origin main

# Option 3: Force push (dangerous!)
git push --force-with-lease origin main
```

### "Authentication failed"

```bash
# Update credentials
git credential reject
git pull # Will prompt for new credentials

# Use SSH instead of HTTPS
git remote set-url origin git@github.com:username/repo.git

# Check credential helper
git config --global credential.helper
```

### Large Push Failures

```bash
# Increase buffer size
git config --global http.postBuffer 524288000 # 500MB

# Use SSH instead of HTTPS (more reliable)
git remote set-url origin git@github.com:username/repo.git

# Push in smaller chunks
git push origin main~10:main
git push origin main~5:main
git push origin main
```

---

## Best Practices Summary

### [PASS] DO
- Use SSH authentication for security
- Fetch before pushing
- Use `--force-with-lease` instead of `--force`
- Keep commits small and focused
- Write clear commit messages
- Pull with rebase for cleaner history
- Protect main branch with branch policies
- Sign commits for verification
- Use Git LFS for large binary files
- Run tests before pushing

### [FAIL] DON'T
- Commit sensitive data (keys, passwords)
- Force push to shared branches
- Push untested code
- Rewrite public history
- Use ambiguous commit messages
- Commit large binary files without LFS
- Push directly to main (use PRs)
- Leave merge conflicts unresolved
- Ignore .gitignore patterns

---

**Related Skills**:
- [Version Control](../../development/version-control/SKILL.md)
- [Security](../../architecture/security/SKILL.md)
- [Code Organization](../../architecture/code-organization/SKILL.md)

## References

- [Auth Fetch Push Branch](references/auth-fetch-push-branch.md)
- [Pr Conflicts Lfs](references/pr-conflicts-lfs.md)
- [Cicd Maintenance Advanced](references/cicd-maintenance-advanced.md)