---
name: forge-conventions
description: Project conventions for git commits, branch naming, and code style. Use when committing code, creating branches, or reviewing code style.
---

# Project Conventions

## Git Commit Style: {{COMMIT_STYLE}}

{{#CONVENTIONAL}}
### Conventional Commits

Format: `type(scope): description`

**Types:**
| Type | Use For |
|------|---------|
| feat | New features |
| fix | Bug fixes |
| docs | Documentation |
| style | Formatting (no code change) |
| refactor | Code restructuring |
| test | Adding tests |
| chore | Maintenance tasks |

**Examples:**
```
feat(auth): add JWT token validation
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
```
{{/CONVENTIONAL}}

{{#FREEFORM}}
### Freeform Commits

Write clear, descriptive messages:
- Start with imperative verb (Add, Fix, Update, Remove)
- Keep first line under 72 characters
- Add body for complex changes

**Examples:**
```
Add user authentication with JWT tokens
Fix null pointer in API response handler
Update README with new installation steps
```
{{/FREEFORM}}

## Branch Naming: {{BRANCH_STYLE}}

{{#FEATURE_BRANCH}}
### Feature Branch Style

Format: `type/description`

| Prefix | Use For |
|--------|---------|
| feature/ | New features |
| fix/ | Bug fixes |
| hotfix/ | Urgent fixes |
| docs/ | Documentation |
| refactor/ | Code cleanup |

Example: `feature/user-authentication`
{{/FEATURE_BRANCH}}

{{#INITIALS_BRANCH}}
### Initials Style

Format: `initials/description`

Example: `mr/user-authentication`
{{/INITIALS_BRANCH}}

See [reference/commit-style.md](reference/commit-style.md) for more examples.
