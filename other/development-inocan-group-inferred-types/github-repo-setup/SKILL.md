---
name: github-repo-setup
version: 0.2.1
description: Use PROACTIVELY when user needs to create a new GitHub repository or set up a project with best practices. Automates repository creation with four modes - quick public repos (~30s), enterprise-grade with security and CI/CD (~120s), open-source community standards (~90s), and private team collaboration with governance (~90s). Not for existing repo configuration or GitHub Actions workflow debugging.
---

# GitHub Repository Setup

## Overview

This skill automates GitHub repository creation following official best practices (2024-2025). It provides four modes tailored to different use cases with appropriate security, documentation, and CI/CD configurations.

**Four Modes:**
1. **Quick Mode** - Fast public repo with essentials (~30s)
2. **Enterprise Mode** - Production-ready with full security and CI/CD (~120s)
3. **Open Source Mode** - Community-focused with templates and guidelines (~90s)
4. **Private/Team Mode** - Internal collaboration with CODEOWNERS and governance (~90s)

## When to Use This Skill

**Trigger Phrases:**
- "create a GitHub repository"
- "set up a new GitHub repo"
- "initialize GitHub repo with best practices"
- "create an enterprise/open source/private repository"

**Use Cases:**
- Starting new projects with GitHub best practices
- Setting up open source projects with community health files
- Creating team repositories with governance and security

## Response Style

- **Efficient**: Automate repetitive setup tasks
- **Guided**: Clear mode selection with trade-offs
- **Security-first**: Enable protection features by default

## Quick Decision Matrix

| User Request | Mode | Setup Time | Key Features |
|-------------|------|------------|--------------|
| "quick repo", "experiment" | Quick | ~30s | README, LICENSE, .gitignore |
| "production repo", "CI/CD" | Enterprise | ~120s | Security + CI/CD + protection |
| "open source project" | Open Source | ~90s | Community templates |
| "private team repo" | Private/Team | ~90s | CODEOWNERS + governance |

## Mode Detection Logic

```javascript
if (userMentions("quick", "test", "experiment")) return "quick-mode";
if (userMentions("enterprise", "production", "ci/cd")) return "enterprise-mode";
if (userMentions("open source", "oss", "public")) return "open-source-mode";
if (userMentions("private", "team", "internal")) return "private-team-mode";
return askForModeSelection();
```

## Modes

| Mode | Description | Details |
|------|-------------|---------|
| Quick | Minimal setup for experiments | → [modes/quick-mode.md](modes/quick-mode.md) |
| Enterprise | Full security and CI/CD | → [modes/enterprise-mode.md](modes/enterprise-mode.md) |
| Open Source | Community health files | → [modes/open-source-mode.md](modes/open-source-mode.md) |
| Private/Team | CODEOWNERS and governance | → [modes/private-team-mode.md](modes/private-team-mode.md) |

## Core Workflow

1. **Mode Selection** - Detect intent or ask user
2. **Prerequisites** - Validate gh CLI, auth, git config
3. **Repository Creation** - Create via GitHub CLI
4. **Security Setup** - Enable Dependabot, secret scanning
5. **Documentation** - Generate README, LICENSE, .gitignore
6. **CI/CD** - Configure workflows (enterprise/open-source)
7. **Templates** - Add issue/PR templates
8. **Protection** - Set branch rules (enterprise/team)
9. **Validation** - Verify setup and provide next steps

## Reference Materials

- [Error Handling & Success Criteria](reference/error-handling.md)

## Important Reminders

1. **Security first** - Enable Dependabot and secret scanning by default
2. **Branch protection** - Protect main branch in production setups
3. **Documentation** - Every repo needs README, LICENSE, and .gitignore
4. **CODEOWNERS** - Use for critical files in team repositories

**Official Documentation**:
- https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories
