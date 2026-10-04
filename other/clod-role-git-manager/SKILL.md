---
name: "Role: Git Manager"
description: "Git workflow: branch management, commit conventions, PR patterns, conflict resolution."
when_to_use: "When a git operation needs judgement beyond a single command: resolving a conflict, deciding a branch/commit strategy or a workflow question not covered by the branch-* and commit-* command skills."
user-invocable: false
metadata:
  family: clod-role
allowed-tools:
  - Read
  - "Bash(git:*)"
---

# Git Workflow Patterns

Git workflow guidance: branch management, commit conventions, pull request practice, conflict resolution and LazyGit. Covers clean history, collaboration patterns and the user's established branch naming conventions.

## When This Skill Applies

Use this skill when:
- Creating or managing branches
- Writing commit messages
- Preparing pull requests
- Resolving merge conflicts
- Reviewing code changes
- Collaborating with team
- Questions about git best practices
- Using LazyGit for version control

## Branch Naming Strategy

### Standard Prefixes

CLAUDE.md 8.6 is authoritative: `feat/`, `fix/`, `enhance/`, `refactor/`, `test/`, `docs/`, `config/`, `chore/`, `ci/`, `deps/`, `hotfix/`, `spike/`, `agents/`. All lowercase, hyphens between words, imperative mood.

### Naming Conventions

**Structure**: `<prefix>/<short-description>`

**Rules**:
- All lowercase
- Hyphens between words (no underscores or spaces)
- Imperative mood: `add-feature`, not `adds-feature` or `adding-feature`
- Descriptive but concise: `feat/calculate-user-stats` not `feat/stats`
- No ticket numbers

### Good Examples
```
feat/add-user-dashboard
feat/implement-search
enhance/improve-search-speed
enhance/add-sorting-options
fix/correctly-render-button
fix/handle-null-user
hotfix/patch-security-vulnerability
hotfix/restore-payment-flow
refactor/extract-auth-logic
refactor/simplify-validation
types/add-api-response-types
types/define-user-interfaces
perf/optimise-graph-rendering
perf/lazy-load-images
styles/update-button-colours
layout/make-nav-responsive
docs/add-api-examples
test/add-e2e-tests
deps/upgrade-svelte-5
config/update-prettier-rules
agents/add-roadmap-workflow
chore/remove-deprecated-code
spike/investigate-neo4j
```

### Bad Examples
```
feature/new-stuff              # Vague, use feat/ not feature/
fix-button                     # Missing prefix separator
FIX/button-bug                 # Uppercase (should be lowercase)
feat/adding-dashboard          # Not imperative (should be "add")
fix/bug                        # Not descriptive enough
refactor/fix-login             # Wrong prefix (it's a fix, not refactor)
feat/user_dashboard            # Underscores (should be hyphens)
```

### Breaking Changes

For breaking changes, prefix the description with `breaking-`:
```
feat/breaking-api-redesign
refactor/breaking-rename-core-types
enhance/breaking-change-auth-flow
```

**Why prefix not suffix**:
- Branch type stays in consistent position
- Easy to scan in branch lists
- Easy to grep: `git branch | grep breaking`
- Breaking nature still prominent (first word after `/`)

See [breaking-changes.md](breaking-changes.md) for the full detection reference: what counts as breaking across APIs, types, schema, HTTP endpoints, config and component props.

### Decision Tree

When creating a new branch, ask these questions in order:

1. **Does it add NEW functionality?** → `feat/`
2. **Does it fix something BROKEN?** → `fix/` (or `hotfix/` if critical)
3. **Does it IMPROVE existing functionality (not broken)?** → `enhance/`
4. **Does it restructure code WITHOUT changing behaviour?** → `refactor/`
5. **Is it ONLY type definitions (interfaces, types)?** → `types/`
6. **Does it improve PERFORMANCE?** → `perf/`
7. **Is it STYLING changes (colours, fonts, spacing)?** → `styles/`
8. **Is it LAYOUT changes (positioning, grid, responsive)?** → `layout/`
9. **Is it DOCUMENTATION?** → `docs/`
10. **Is it TESTING?** → `test/`
11. **Is it dependency/config/build?** → `deps/`, `config/`, `build/`, `agents/`
12. **Is it CI/CD related?** → `ci/` or `deploy/`
13. **Is it research/experimental?** → `spike/` or `experiment/`
14. **Is it just maintenance/cleanup?** → `chore/`
15. **Still unsure?** → Use the PRIMARY purpose of the branch

### Common Scenarios

**Styles vs Layout**:

Use `styles/` for:
- Colours, fonts, typography
- Spacing, padding, margins
- Borders, shadows, visual effects
- Theme variables
- CSS properties that don't affect structure

Use `layout/` for:
- Grid/flexbox structure
- Responsive breakpoints
- Component positioning
- Page structure
- Display/position properties

**Multiple Changes in One Branch**:
Use the prefix for the PRIMARY purpose.

Examples:
- Adding a feature that requires refactoring → `feat/add-user-dashboard`
- Fixing a bug that requires tests → `fix/handle-null-user`
- Enhancing feature with performance improvements → `enhance/improve-search-speed`

## Commit Message Conventions

### Standard Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore` (CLAUDE.md 8.1)
**Scope**: Component/module affected (optional)
**Subject**: Brief description (50 chars max)
**Body**: Detailed explanation (optional, wrap at 72 chars)
**Footer**: Breaking changes, issue references (optional)

### Examples

**Simple commit**:
```
fix(auth): prevent token expiration race condition
```

**With body**:
```
feat(dashboard): add real-time activity feed

Implements WebSocket connection to stream user activities.
Includes reconnection logic and offline handling.
```

**With footer**:
```
fix(api): correct user data validation

BREAKING CHANGE: email field now required in user creation

Closes #123
Fixes #456
```

### Commit Message Guidelines

**Subject line rules**:
- Start with lowercase
- No period at end
- Imperative mood ("add" not "added" or "adds")
- Max 50 characters

**Good subjects**:
```
fix(login): handle empty password field
feat(search): add fuzzy matching
refactor(db): extract connection pool logic
docs(readme): update installation steps
```

**Bad subjects**:
```
Fixed bug
Updated stuff
Changes to the user service
WIP - still working on this
```

**Body rules**:
- Explain *what* and *why*, not *how*
- Wrap at 72 characters
- Separate from subject with blank line

**House rules**: British spelling, no em dashes, no Oxford commas. The global `commit-msg` git hook (`~/.claude/hooks/commit-msg`) rejects a message that breaks them and prints one `L<n> <rule>: <excerpt>` line per hit; the retry contract (rewrite once, then stop, never `--no-verify`) is in the `commit-one` skill.

**Good body**:
```
feat(export): add CSV export functionality

Users can now export their data as CSV files. This addresses
frequent requests from enterprise customers who need to import
data into their analytics tools.

The implementation uses streaming to handle large datasets
without memory issues.
```

### Atomic Commits

**One logical change per commit**:

**Good** (atomic):
```
1. feat(user): add user profile endpoint
2. test(user): add profile endpoint tests
3. docs(api): document profile endpoint
```

**Bad** (mixed concerns):
```
1. feat(user): add profile endpoint, fix login bug, update dependencies
```

### Commit Frequency

**Commit often, push strategically**:
```bash
# Local development: Commit frequently
git commit -m "feat(auth): add basic login form"
git commit -m "feat(auth): add form validation"
git commit -m "feat(auth): connect to API"
git commit -m "test(auth): add login tests"

# Before pushing: Consider squashing if appropriate
git rebase -i HEAD~4  # Interactive squash if needed

# Push clean history
git push origin feat/add-user-authentication
```

## GitHub Operations

A `github` MCP server (`@modelcontextprotocol/server-github`, user-scoped) is available for GitHub operations (PRs, issues, repo metadata) as an alternative to shelling out to `gh`. Prefer the MCP tools when working with GitHub-hosted repos and structured data is useful (e.g. parsing PR review comments); `gh` remains fine for quick one-off CLI calls. Note: the server needs `GITHUB_PERSONAL_ACCESS_TOKEN` set to do anything beyond unauthenticated public reads.

## Additional resources

Mechanical how-to and reference material, loaded only when needed:

- [lifecycle-and-review.md](lifecycle-and-review.md): branch creation/update/cleanup, PR checklist and description template, merge strategy trade-offs, conflict resolution
- [lazygit-and-advanced.md](lazygit-and-advanced.md): LazyGit key bindings and workflows, stash/cherry-pick/bisect/reflog
- [breaking-changes.md](breaking-changes.md): the full breaking-change detection reference (APIs, types, schema, HTTP endpoints, config, component props) backing CLAUDE.md §8.5

## Success Criteria

Git workflow is successful when:
- Branch names follow established conventions
- Commit history is clear and meaningful
- Commits are atomic and well-described
- PRs are appropriately sized
- Conflicts resolved cleanly
- Team understands workflow
- Easy to trace changes and revert if needed
- LazyGit workflows streamlined
- Breaking changes are flagged and documented
