---
name: pr-creator
description: Create pull requests with gh command after development is complete. Use when ready to open a PR.
---

# PR Creator Skill

Create a pull request after development on a branch is complete.

## Development Types

| Type | Branch Pattern | Title Prefix | Draft | Template |
|------|----------------|--------------|-------|----------|
| Feature | `feature/*` | `feat:` | Yes | [feature.md](templates/feature.md) |
| Bug fix | `fix/*` | `fix:` | No | [fix.md](templates/fix.md) |
| Documentation | `docs/*` | `docs:` | No | [docs.md](templates/docs.md) |
| Refactoring | `refactor/*` | `refactor:` | Yes | [refactor.md](templates/refactor.md) |

## Guidelines

1. **Link the specification** - Every PR must reference its specification
2. **One feature per PR** - Keep PRs focused and small
3. **All tests must pass** - Ensure CI is green
4. **Request a review** - Wait for approval before merging

## Workflow

1. **Analyze**: Get branch name, commits (`main..HEAD`), and diff to understand changes
2. **Find spec**: Look for related spec in `docs/specs/`
3. **Draft**: Generate title and body using the appropriate template
4. **Confirm**: Show draft to user for approval
5. **Create**: Push if needed, run `gh pr create`
6. **Report**: Show PR URL
