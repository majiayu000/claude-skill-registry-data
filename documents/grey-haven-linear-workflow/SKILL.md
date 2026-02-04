---
name: grey-haven-linear-workflow
description: Grey Haven's Linear issue workflow - creating well-documented issues, proper branch naming from issue IDs, commit message integration, PR linking, and status management. Use when creating issues, starting work, or managing project workflow.
# v2.0.43: Skills to auto-load for Linear workflow
skills:
  - grey-haven-code-style
  - grey-haven-commit-format
# v2.0.74: Tools for workflow management
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - TodoWrite
  - mcp__linear__*
---

# Grey Haven Linear Workflow

Follow Grey Haven Studio's workflow for **Linear issue management**, **Git branching**, and **pull request integration**.

## Linear Issue Management

### Issue Creation Guidelines

**Always create Linear issues BEFORE starting work** to track progress and context.

**Issue Title Format**: Specific, actionable statements
```
[OK] Good titles:
- Add magic link authentication
- Fix race condition in user repository
- Migrate organizations table to multi-tenant

[X] Bad titles (too vague):
- Auth improvements
- Fix bug
- Update dependencies
```

### Issue Templates

**Feature Issue Structure**:
```markdown
Title: Add magic link authentication

## Description
[What you're building]

## Motivation
[Why this is needed - user pain points, business value]

## Acceptance Criteria
- [ ] Specific, testable criteria
- [ ] Include multi-tenant isolation requirements
- [ ] Target >80% test coverage

## Technical Notes
- Tech stack references (better-auth, TanStack, etc.)
- Doppler environment variables needed
- Database schema changes (snake_case fields)

## Related Issues
- Blocks: GREY-XXX
- Related: GREY-YYY

Labels: feature, [component], [priority]
Estimate: X points
```

**Bug Issue Structure**:
```markdown
Title: Fix race condition in user repository

## Description
[What's broken]

## Steps to Reproduce
1. [Step-by-step]
2. [With specific inputs]
3. [Expected vs actual]

## Impact
- Frequency: X% of requests
- User experience impact
- Data corruption risk

## Proposed Solution
[How to fix it]

## Environment
- Backend: cvi-backend-template
- Database: PostgreSQL with RLS
- Doppler config: production

Labels: bug, [component], [priority]
Priority: [critical/high-priority/normal/low-priority]
```

### Labels

**Type Labels**: `feature`, `bug`, `chore`, `docs`, `refactor`, `performance`

**Component Labels**: `frontend`, `backend`, `database`, `auth`, `multi-tenant`, `testing`

**Priority Labels**: `critical`, `high-priority`, `low-priority`

### Story Point Estimates

Use Fibonacci sequence:
- **1 point**: < 1 hour (config change, simple fix)
- **2 points**: 1-2 hours (small feature, simple bug)
- **3 points**: Half day (moderate feature)
- **5 points**: 1 day (complex feature, migration)
- **8 points**: 2-3 days (large feature, major refactor)
- **13 points**: 1 week (should be broken down into smaller issues)

## Git Branching Strategy

### Branch Naming Convention

**Format**: `<issue-id>-<type>-<short-description>`

```bash
# Examples
GREY-234-feat-magic-link-auth
GREY-456-fix-user-race-condition
GREY-890-migrate-add-tenant-id
GREY-123-chore-update-dependencies
GREY-789-docs-update-api-guide
```

### Creating Branches from Linear Issues

```bash
# Always branch from latest main!
git checkout main
git pull origin main
git checkout -b GREY-234-feat-magic-link-auth
```

### Branch Protection Rules

Main branch protection:
- ✅ Require pull request before merging
- ✅ Require 1 approval
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Require linear history (squash merges)
- ❌ Do NOT allow force pushes
- ❌ Do NOT allow deletions

## Commit Message Integration

### Format with Linear

```
<type>(<scope>): <subject>

[optional body]

[Linear issue reference]
```

**Examples**:

```bash
# Feature commit
feat(auth): add magic link authentication

Implement magic link provider using better-auth with email
verification via Resend.

- Single-use tokens with 15 minute expiry
- Tenant isolation via RLS policies
- Server functions for sending/verifying links

Closes GREY-234

# Bug fix commit
fix(repositories): prevent race condition in user creation

Add database-level unique constraint and proper IntegrityError
handling in UserRepository.

Fixes GREY-456

# Migration commit
feat(db): add tenant_id to organizations table

Add tenant_id column and RLS policies for multi-tenant isolation.
Backfill from service_id column.

Related to GREY-890
```

### Linear Keywords

Use these keywords to automatically update Linear issues:

- **Closes GREY-123**: Marks issue as Done when PR merges
- **Fixes GREY-123**: Same as Closes (for bugs)
- **Related to GREY-123**: Links issue without closing
- **Blocks GREY-123**: Indicates dependency
- **Blocked by GREY-123**: Indicates blocker

## Pull Request Integration

### PR Title Format

Include Linear ID at the end:
```
<type>(<scope>): <description> [GREY-123]
```

**Examples**:
```
feat(auth): add magic link authentication [GREY-234]
fix(repositories): prevent race condition in user creation [GREY-456]
feat(db): add tenant_id to organizations table [GREY-890]
```

### PR Description Template

```markdown
## Summary
[2-4 sentence description]. Closes GREY-XXX.

## Linear Issue
https://linear.app/grey-haven/issue/GREY-XXX/issue-title

## Motivation
[Why these changes are needed]

## Implementation Details

### Key Changes
- **Component**: [what changed]
- **Database**: [schema changes with snake_case]
- **Tests**: [test coverage with markers]

### Multi-Tenant Considerations
- tenant_id added to [tables]
- RLS policies created
- Queries filter by tenant_id

### Doppler Configuration
- Added/updated: [environment variables]
- Required in: [dev/test/staging/production]

## Testing

### Automated Tests
- [OK] Unit tests: [coverage %]
- [OK] Integration tests: [coverage %]
- [OK] E2E tests: [coverage %]
- [OK] Total coverage: >80%

### Manual Testing
Run with Doppler:
```bash
doppler run --config dev -- bun run dev
doppler run --config test -- bun test
```

## Checklist
- [ ] Code follows Grey Haven style (90 char TS, 130 char Python)
- [ ] Tests added/updated (>80% coverage)
- [ ] Multi-tenant isolation verified
- [ ] Doppler env vars documented
- [ ] Pre-commit hooks passing
- [ ] Database migrations tested (if applicable)
- [ ] Linear issue linked
```

## Linear Status Management

### Issue Lifecycle

```
Backlog → Todo → In Progress → In Review → Done
   ↓                                ↓
Canceled                        Canceled
```

### Status Transitions

**Todo → In Progress**:
1. Create branch: `GREY-234-feat-magic-link-auth`
2. Linear automatically moves to "In Progress"
3. Start coding

**In Progress → In Review**:
1. Push commits to branch
2. Create PR with "Closes GREY-234" in description
3. Linear automatically moves to "In Review"
4. Request review from team

**In Review → Done**:
1. Squash and merge PR to main
2. Linear automatically closes issue (via "Closes GREY-234")
3. Delete feature branch

## Supporting Documentation

All supporting files are under 500 lines per Anthropic best practices:

- **[examples/](examples/)** - Complete workflow examples
  - [feature-issue-template.md](examples/feature-issue-template.md) - Feature issue template
  - [bug-issue-template.md](examples/bug-issue-template.md) - Bug issue template
  - [migration-issue-template.md](examples/migration-issue-template.md) - Migration template
  - [commit-message-examples.md](examples/commit-message-examples.md) - Commit message examples
  - [pr-description-examples.md](examples/pr-description-examples.md) - PR description examples
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[reference/](reference/)** - Workflow references
  - [labels.md](reference/labels.md) - Label definitions and usage
  - [status-transitions.md](reference/status-transitions.md) - Status lifecycle details
  - [branch-protection.md](reference/branch-protection.md) - Branch protection rules
  - [linear-keywords.md](reference/linear-keywords.md) - Automatic issue updates
  - [INDEX.md](reference/INDEX.md) - Reference navigation

- **[templates/](templates/)** - Copy-paste ready templates
  - [feature-issue.md](templates/feature-issue.md) - Feature issue template
  - [bug-issue.md](templates/bug-issue.md) - Bug issue template
  - [pr-description.md](templates/pr-description.md) - PR description template

- **[checklists/](checklists/)** - Workflow checklists
  - [issue-creation-checklist.md](checklists/issue-creation-checklist.md) - Pre-issue checklist
  - [pr-checklist.md](checklists/pr-checklist.md) - Pre-PR checklist

## When to Apply This Skill

Use this skill when:
- Creating new Linear issues
- Starting work on a feature or bug
- Creating Git branches
- Writing commit messages
- Opening pull requests
- Managing issue status transitions
- Setting up Linear workflows for new team members

## Template Reference

These patterns are from Grey Haven's production workflows:
- **Linear workspace**: grey-haven team configuration
- **GitHub integration**: Automatic status updates
- **Branch naming**: Issue ID prefixed branches

## Critical Reminders

1. **Create issues BEFORE work**: Track all work in Linear
2. **Branch from main**: Always `git checkout main && git pull`
3. **Branch naming**: `GREY-XXX-<type>-<description>`
4. **Commit keywords**: Use "Closes", "Fixes", "Related to"
5. **PR title format**: Include `[GREY-XXX]` at the end
6. **Multi-tenant**: Document tenant isolation in PRs
7. **Doppler**: Document env vars in issue/PR
8. **Test coverage**: Maintain >80% coverage
9. **Linear automation**: Keywords auto-update issue status
10. **Squash merges**: Keep main branch history clean
