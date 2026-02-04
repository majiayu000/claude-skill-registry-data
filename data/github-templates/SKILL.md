---
name: github-templates
description: GitHub repository templates and configuration. Activate when setting up GitHub repos, CONTRIBUTING.md, CODEOWNERS, issue templates, PR templates, or GitHub Copilot instructions.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# GitHub Templates

Guidelines for GitHub repository configuration and community files.

## Essential Files

| File | Purpose | Required |
|------|---------|----------|
| README.md | Project overview | MUST |
| LICENSE | Legal terms | MUST for open source |
| CONTRIBUTING.md | Contribution guidelines | SHOULD |
| CODE_OF_CONDUCT.md | Community standards | SHOULD |
| SECURITY.md | Vulnerability reporting | MUST for public repos |
| CODEOWNERS | Review assignments | RECOMMENDED |
| .github/copilot-instructions.md | AI coding assistant context | RECOMMENDED |

## Issue Templates

Place in `.github/ISSUE_TEMPLATE/`. Use YAML form format for structured input.

Key elements for `bug_report.yml`:
- Description, steps to reproduce, expected/actual behavior (required)
- Version, OS dropdown, logs textarea (optional)

Key elements for `feature_request.yml`:
- Problem statement, proposed solution (required)
- Alternatives considered, additional context (optional)

Add `config.yml` to disable blank issues and add contact links.

See `assets/bug_report.yml.template` for full example.

## Pull Request Template

Place at `.github/pull_request_template.md`.

```markdown
## Summary
<!-- Brief description of changes -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
<!-- How was this tested? -->

## Checklist
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## CODEOWNERS

Place at `.github/CODEOWNERS` or `CODEOWNERS` in root.

```gitignore
# Default owners
*       @org/team-leads

# Directory ownership
/src/   @org/developers
/docs/  @org/tech-writers

# File patterns
*.js    @org/frontend-team
*.py    @org/backend-team

# Specific files
/config/prod.yml @org/devops @security-lead
```

**Rules:**
- Later rules override earlier ones
- Order from general to specific
- Use teams (`@org/team`) over individuals when possible
- Review groups MUST have write access to request reviews

## Branch Protection

Recommended settings for `main`/`master`:

1. **Require pull request reviews** - At least 1 approval, dismiss stale reviews, require CODEOWNERS review
2. **Require status checks** - Branches must be up to date, select required CI checks
3. **Restrict who can push** - Limit to maintainers/admins
4. **Additional** - Signed commits (sensitive repos), no force pushes, no deletions

## GitHub Actions Basics

Place workflows in `.github/workflows/`.

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

**Common triggers:** `push`, `pull_request`, `schedule` (cron), `workflow_dispatch` (manual)

## Copilot Instructions

Place at `.github/copilot-instructions.md` for workspace-level AI context.

**Purpose:** Project-specific context for GitHub Copilot including tech stack, coding standards, patterns, and domain terminology.

**Key sections:**
- Project overview and tech stack
- Coding standards and naming conventions
- Preferred patterns (repository, service layer, DTOs)
- Domain terminology glossary
- Common task workflows

See `assets/copilot-instructions.md.template` for full example.

## Dependabot Configuration

Place at `.github/dependabot.yml`.

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels: ["dependencies"]
    groups:
      dev-dependencies:
        dependency-type: "development"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

## .gitattributes

Place in repository root for consistent line endings.

```gitattributes
* text=auto
*.sh text eol=lf
*.bat text eol=crlf
*.png binary
*.jpg binary
*.pdf binary
package-lock.json -diff
yarn.lock -diff
```

## Quick Setup Checklist

1. [ ] README.md with project overview
2. [ ] LICENSE file selected
3. [ ] .gitignore appropriate for stack
4. [ ] .gitattributes for line endings
5. [ ] CONTRIBUTING.md with guidelines
6. [ ] SECURITY.md for vulnerability reporting
7. [ ] Issue templates in `.github/ISSUE_TEMPLATE/`
8. [ ] PR template at `.github/pull_request_template.md`
9. [ ] CODEOWNERS with team assignments
10. [ ] Branch protection on main
11. [ ] CI workflow in `.github/workflows/`
12. [ ] Dependabot configuration
13. [ ] Copilot instructions (optional)

## Templates Location

Asset templates available in this skill's `assets/` directory:
- `CONTRIBUTING.md.template` - Contribution guidelines
- `SECURITY.md.template` - Vulnerability reporting process
- `CODEOWNERS.template` - Code ownership patterns
- `pull_request_template.md.template` - PR template
- `bug_report.yml.template` - Bug report issue form
- `copilot-instructions.md.template` - AI assistant context
