---
name: commit-message-style
description: "Apply commit message style: conventional commits format (type: subject), imperative mood, <50 char subject, explain why in body. Use when writing commits, reviewing commit messages, or discussing git history."
---

# Commit Message Style

Conventional commits format for clear, consistent git history. Universal standard across projects and teams.

## Core Principle

**Commit messages are for humans reading git history.**

Good commits help understand what changed and why. They enable searching, filtering, and generating changelogs.

---

## Format

### Basic Structure

```
type(scope): subject

body

footer
```

**Required:** type, subject
**Optional:** scope, body, footer

### Example

```
feat(auth): add OAuth2 integration

Implement OAuth2 authentication flow for Google and GitHub.
This allows users to sign in with existing accounts.

Fixes #234
```

---

## Commit Types

**feat:** New feature
```
feat: add user authentication
feat(api): add rate limiting to endpoints
```

**fix:** Bug fix
```
fix: handle null user in profile page
fix(auth): prevent token expiry race condition
```

**refactor:** Code change (no feature or bug fix)
```
refactor: extract payment logic to separate module
refactor(db): simplify query builder
```

**docs:** Documentation only
```
docs: update README with installation steps
docs(api): add examples to endpoint descriptions
```

**test:** Tests only
```
test: add edge cases for calculateTotal
test(auth): add integration tests for OAuth flow
```

**chore:** Build, dependencies, tooling
```
chore: upgrade dependencies to latest versions
chore(deps): update React to v18
```

**perf:** Performance improvement
```
perf(db): add index on user email column
perf: lazy load images to reduce initial bundle
```

**style:** Formatting, whitespace (no logic change)
```
style: format code with prettier
style: fix inconsistent indentation
```

**ci:** CI/CD changes
```
ci: add automated deployment to staging
ci: run tests on pull requests
```

**build:** Build system changes
```
build: configure webpack for production
build: add TypeScript compilation step
```

---

## Subject Line Rules

### Imperative Mood

Use imperative mood (command form), not past tense.

✅ **Good:**
- `add user authentication`
- `fix null pointer error`
- `update dependencies`

❌ **Bad:**
- `added user authentication` (past tense)
- `adding user authentication` (continuous)
- `adds user authentication` (third person)

**Think:** "This commit will [subject]"
- "This commit will add user authentication" ✅
- "This commit will added user authentication" ❌

### Lowercase

Start subject with lowercase (after type).

✅ `feat: add feature`
❌ `feat: Add feature`

### No Period

Don't end subject with period.

✅ `fix: handle edge case`
❌ `fix: handle edge case.`

### Length

- **Ideal:** <50 characters
- **Maximum:** 72 characters
- Longer descriptions go in body

✅ `feat: add OAuth integration`
❌ `feat: add OAuth integration for Google, GitHub, and Microsoft accounts with automatic token refresh`

### Be Specific

Subject should clearly describe what changed.

✅ **Good:**
- `fix: prevent crash when user has no email`
- `feat(api): add pagination to user list endpoint`
- `refactor: extract validation to separate module`

❌ **Bad:**
- `fix bug` (what bug?)
- `update` (update what?)
- `changes` (what changes?)
- `WIP` (work in progress—finish before committing)

---

## Scope (Optional)

Scope indicates affected area of codebase.

**Format:** `type(scope): subject`

**Common scopes:**
- Component/module: `(auth)`, `(api)`, `(ui)`
- Feature: `(payments)`, `(search)`, `(notifications)`
- Layer: `(db)`, `(cache)`, `(middleware)`

**Examples:**
```
feat(auth): add OAuth2 support
fix(api): handle timeout errors
refactor(db): optimize user queries
```

**When to omit scope:**
- Changes affect entire codebase
- Scope is obvious from subject
- Small projects without clear modules

---

## Body (Optional)

Use body to explain **why**, not what (diff shows what).

### When to Add Body

- **Complex changes** (need context)
- **Non-obvious decisions** (why this approach)
- **Breaking changes** (always explain)
- **Trade-offs** (why chose X over Y)

### Body Rules

- Blank line between subject and body
- Wrap at 72 characters
- Explain motivation, not mechanics
- Can use bullet points

### Example

```
refactor(auth): switch from JWT to session cookies

JWT tokens were causing issues with token revocation.
Session cookies allow immediate logout and better
security control.

Trade-off: Requires server-side session storage,
but improved security is worth the complexity.
```

---

## Footer (Optional)

### Breaking Changes

**Format 1** (footer):
```
feat: redesign authentication API

BREAKING CHANGE: login endpoint now requires email instead of username
```

**Format 2** (type with !):
```
feat!: redesign authentication API

Login endpoint now requires email instead of username.
```

**Always include:**
- What broke
- How to migrate
- Why the break was necessary

### Issue References

**Close issues:**
```
Fixes #123
Closes #456
Resolves #789
```

**Reference without closing:**
```
Refs #123
See #456
```

**Multiple issues:**
```
Fixes #123, fixes #456
```

### Co-authors

For pair programming or collaboration:

```
Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

---

## Examples

### Simple Commit

```
feat: add dark mode toggle
```

### With Scope

```
fix(api): handle network timeout errors
```

### With Body

```
perf(db): add index on user email column

Queries filtering by email were taking >2s on production.
Adding index reduces query time to <50ms.
```

### Complex Commit

```
feat(auth): add OAuth2 integration

Implement OAuth2 authentication flow for Google and GitHub.
This allows users to sign in with existing accounts instead
of creating new credentials.

Chose OAuth2 over SAML due to better mobile support and
simpler integration with third-party providers.

Fixes #234
Co-authored-by: Jane Developer <jane@example.com>
```

### Breaking Change

```
feat!: remove legacy API endpoints

Removed /api/v1 endpoints in favor of /api/v2.

BREAKING CHANGE: All clients must migrate to /api/v2.
See migration guide: docs/migration-v2.md

Closes #567
```

---

## Bad Examples

❌ `fix bug`
- Too vague. What bug?

❌ `update`
- What was updated?

❌ `WIP`
- Not a commit type. Finish work before committing.

❌ `fix: Fixed the login issue`
- Past tense ("Fixed"). Should be: `fix: handle login timeout`

❌ `feat: Added new feature for users`
- Past tense, vague. What feature?

❌ `refactor: refactored the code`
- Redundant. What code? Why?

---

## Quick Reference

### Format Template

```
type(scope): subject under 50 chars

Body explaining why (not what).
Wrap at 72 characters.

BREAKING CHANGE: if applicable
Fixes #123
Co-authored-by: Name <email>
```

### Types Cheatsheet

- `feat` → New feature
- `fix` → Bug fix
- `refactor` → Code change (no feature/bug)
- `docs` → Documentation
- `test` → Tests
- `chore` → Build, deps, tooling
- `perf` → Performance
- `style` → Formatting
- `ci` → CI/CD
- `build` → Build system

### Subject Rules

- ✅ Imperative mood
- ✅ Lowercase after type
- ✅ No period
- ✅ <50 chars ideal
- ✅ Specific, clear

---

## Philosophy

**"Good commits tell a story."**

Git history is documentation. Well-written commits help:
- Understand why changes were made
- Find when bugs were introduced
- Generate changelogs automatically
- Review code changes in context

**Commit often, commit well:**
- Small, focused commits
- One logical change per commit
- Clear message for each

**Remember:** You're writing for the person debugging at 2am in 6 months. That person might be you.
