---
name: commit-message
description: Write clean Conventional Commits messages and pull request descriptions from staged changes or diffs. Use when the user asks to write a commit message, commit their changes, describe a PR, open a pull request, summarise a branch, or says "write a commit", "create a PR", "what should I call this commit", or "draft my PR description".
---

# Commit Messages & Pull Request Descriptions

Every commit message and PR description is a permanent record. Future engineers — including yourself in six months — will read them to understand why the codebase is the way it is. A bad commit message is a mystery. A good commit message is documentation that never goes stale.

Write commit messages and PR descriptions as if the reader has zero context about what problem you were solving. Because they do.

---

## Commit Message Principles

- **The commit message is for the reader, not the writer.** You know what you changed. The message exists for someone reading `git log` in a year.
- **Why, not what.** The diff shows what changed. The commit message must explain why.
- **One commit, one concern.** A commit that fixes a bug and refactors a module is two commits. Atomic commits make revert, bisect, and cherry-pick safe and surgical.
- **Present tense, imperative mood.** "Add validation" not "Added validation" or "Adds validation". Read the subject as completing: "This commit will ___."
- **Never commit broken code.** Every commit on the main branch must compile, pass tests, and leave the system in a working state.

---

## Conventional Commits Format

Every commit follows the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Type Reference

| Type | When to use |
|------|------------|
| `feat` | A new feature visible to users or API consumers |
| `fix` | A bug fix |
| `docs` | Documentation only changes (README, comments, API docs) |
| `style` | Formatting changes that do not affect logic (whitespace, semicolons) |
| `refactor` | Code restructuring that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Changes to build system, dependencies, or CI configuration |
| `ci` | Changes to CI/CD pipeline configuration |
| `chore` | Maintenance tasks (dependency updates, config tweaks) |
| `revert` | Revert a previous commit |

### Scope (optional but recommended)
The scope narrows what part of the codebase was changed:
```
feat(auth): add OAuth2 PKCE flow
fix(api/users): return 404 when user not found
test(payments): add integration test for refund flow
perf(db): add index on orders.created_at
```

### Breaking Changes
Append `!` to the type or add `BREAKING CHANGE:` in the footer:
```
feat(api)!: change pagination from offset to cursor-based

BREAKING CHANGE: The `page` and `offset` query parameters on /v1/users
are removed. Use `cursor` instead. See migration guide: docs/migration/v2.md
```

---

## Writing the Subject Line

The subject is the single most important part of a commit message. It appears in `git log`, GitHub, Slack notifications, and changelogs.

**Rules:**
- Maximum 72 characters
- Imperative mood: "Add", "Fix", "Remove", "Update", "Refactor" — not "Added", "Fixes", "Removes"
- No period at the end
- Lowercase after the colon: `fix(auth): handle expired tokens` not `fix(auth): Handle expired tokens`
- Be specific: "fix(api): return 404 when user is not found" not "fix: bug fix"

**Good vs bad subjects:**

| ❌ Bad | ✅ Good |
|--------|--------|
| `fix stuff` | `fix(auth): handle nil pointer when token is missing` |
| `WIP` | `feat(users): add email verification on signup` |
| `changes` | `refactor(db): extract query builder into repository layer` |
| `update` | `chore(deps): bump jsonwebtoken from 8.5.1 to 9.0.2` |
| `JIRA-1234` | `fix(orders): prevent duplicate charge on network retry (JIRA-1234)` |
| `added the new feature for the login page to work better` | `feat(auth): add remember-me cookie on successful login` |

---

## Writing the Body

The body explains **why** the change was made. Write it when:
- The reason for the change is not obvious from the subject
- You are making a non-trivial design decision
- You are fixing a bug and the root cause is worth documenting
- You are working around an external limitation or known issue

**Body format:**
```
feat(cache): use Redis for session storage instead of in-memory

In-memory session storage meant users were logged out on every
deployment and could not be load-balanced across multiple instances.

Redis provides shared session state across all API instances and
persists sessions across deployments. Sessions expire after 24h
matching the existing JWT expiry.

Note: requires REDIS_URL environment variable to be set. See
.env.example for the required format.
```

**Body rules:**
- Blank line between subject and body — always
- Wrap at 72 characters
- Write in full sentences
- Explain the problem being solved, not the implementation

---

## Writing the Footer

Use the footer for:

```
# Referencing issues
Closes #342
Fixes #201
Refs #99

# Co-authors
Co-authored-by: Jane Doe <jane@example.com>

# Breaking changes
BREAKING CHANGE: The `userId` parameter is renamed to `user_id`.
Update all callers before deploying.

# Generated commits (BEACON requirement)
Generated with BEACON
```

---

## Complete Examples

### Simple bug fix
```
fix(api/orders): return 404 when order does not belong to user

Previously, the endpoint returned 500 when a user queried an order
owned by another user due to a null pointer on the missing record.

The fix adds an ownership check after fetching the order and returns
a 404 (not 403) to avoid leaking the existence of other users' orders.

Closes #412
```

### New feature
```
feat(auth): add OAuth2 login with GitHub

Adds GitHub as a third-party OAuth2 provider alongside the existing
Google integration. Uses the same OAuth2 abstraction layer — adding
a new provider required only a new config entry and scope mapping.

Requires GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET environment
variables. See .env.example and docs/auth/oauth2.md.

Closes #287
```

### Breaking change
```
feat(api)!: replace offset pagination with cursor-based pagination

Offset pagination on large tables became unbearably slow above 100K
rows (O(n) DB scans). Cursor pagination is O(log n) using the
indexed `created_at` column.

BREAKING CHANGE: `page` and `offset` query parameters on all
collection endpoints are removed. Use `cursor` (returned in the
`pagination.cursor` field of every collection response) instead.

Migration guide: docs/migration/pagination-v2.md
Closes #198
```

### Dependency update
```
chore(deps): upgrade jsonwebtoken to 9.0.2

Fixes CVE-2022-23529 (arbitrary code execution via malformed JWT).
No API changes required — the fix is internal to the library.

See: https://github.com/advisories/GHSA-hjrf-2m68-5959
```

---

## Pull Request Description Standard

A PR description is a decision record. It must give reviewers enough context to review effectively and give future engineers enough context to understand why the change was made.

### PR Title
Follow the same Conventional Commits format as a commit subject:
```
feat(auth): add OAuth2 login with GitHub
fix(api/orders): return 404 when order does not belong to user
refactor(db): extract query builder into repository layer
```

### PR Description Template

```markdown
## Summary
<!-- One paragraph: what problem does this solve and how. 
     Write as if the reviewer has not read the ticket. -->

## Changes
<!-- Bullet list of what changed. One line per logical change. -->
- Added `GitHubOAuthProvider` implementing the `OAuthProvider` interface
- Added `/auth/github/callback` endpoint
- Added `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` to `.env.example`
- Added integration test for the full GitHub OAuth flow

## Why
<!-- Why this approach? Alternatives considered? Constraints that drove the design? -->

## Testing
<!-- How was this tested? What test cases were added? 
     How can the reviewer verify this works? -->
- [ ] Unit tests: `npm test -- --grep "GitHubOAuthProvider"`
- [ ] Integration test: `npm run test:integration -- oauth`
- [ ] Manual: tested against a real GitHub OAuth app in staging

## Breaking Changes
<!-- None, or: list what breaks and the migration path -->
None.

## Screenshots / Demo
<!-- For UI changes: before/after screenshots or a screen recording -->

## Checklist
- [ ] Tests added for new behaviour
- [ ] Tests pass locally
- [ ] No secrets or credentials in the diff
- [ ] `.env.example` updated if new env vars added
- [ ] Documentation updated if behaviour changed
- [ ] No debug code, `console.log`, or TODO comments in production paths
```

---

## Branch Naming Convention

```
<type>/<short-description>

feat/github-oauth
fix/order-404-ownership-check
refactor/db-query-builder
chore/upgrade-jsonwebtoken
docs/oauth2-setup-guide
```

**Rules:**
- Lowercase, hyphen-separated
- Short but descriptive (3–5 words)
- Matches the commit type
- Include a ticket number if your team uses one: `feat/JIRA-1234-github-oauth`

---

## Commit Hygiene Rules

**Atomic commits:**
- One logical change per commit
- Every commit on main must build and pass tests
- Refactors and feature changes are separate commits

**What to never commit:**
- Hardcoded secrets, API keys, passwords, tokens
- `console.log`, `print`, `debugger` statements in production paths
- Commented-out code (delete it; git history preserves it)
- Merge conflicts markers (`<<<<<<<`, `=======`, `>>>>>>>`)
- Generated files that belong in `.gitignore`
- Lock files for the wrong package manager

**Commit before you forget:**
- Commit at logical completion points — not just end of day
- A commit that captures "I got X working" is better than one giant commit at the end
- Use `git stash` for in-progress work, not half-finished commits on main

---

## Definition of Done — Commit / PR

A commit is done when:
- [ ] Conventional Commits type and scope correct
- [ ] Subject ≤ 72 characters, imperative mood, no period
- [ ] Body explains why (if the reason is not self-evident)
- [ ] Breaking changes documented in footer with migration path
- [ ] No secrets, debug code, or commented-out code in the diff
- [ ] All tests pass

A PR is done when:
- [ ] Title follows Conventional Commits format
- [ ] Summary written for someone with no ticket context
- [ ] Changes listed as bullet points
- [ ] Testing section explains how to verify
- [ ] Breaking changes section complete (or explicitly "None")
- [ ] Checklist items all checked
- [ ] Screenshots/demo included for UI changes
- [ ] `Generated with BEACON` included in commit message if AI-assisted
