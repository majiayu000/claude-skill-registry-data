---
name: Conventional Commits - Advanced
description: Advanced usage of conventional commits with breaking changes, issue references, and multi-file commits.
---

# Advanced Conventional Commits Skill

Create conventional commits directly for advanced scenarios.

---

## Before Starting

Check the repository state:

```bash
git status
git diff --staged
git log --oneline -5
```

Stop if repository is in conflict state or no changes are staged.

---

## Analyze the Changes

Look at what's staged and determine:

**Type** - What kind of change is this?
- `feat` - new feature
- `fix` - bug fix
- `docs` - documentation only
- `style` - formatting only
- `refactor` - code restructure (no behavior change)
- `perf` - performance improvement
- `test` - test changes
- `build` - build/dependency changes
- `ci` - CI/CD changes
- `chore` - maintenance/tooling

**Scope** - What part of the project is affected?
- Look at recent commits to see what scopes are used
- Use project conventions (like `auth`, `api`, `ui`, `db`)
- Use singular form (`user` not `users`)

**Breaking changes?** - Does this break existing functionality?
- Removed or renamed APIs
- Changed function signatures
- Changed response formats
- Removed configuration options
- Changed default behaviors

If yes: Use `!` marker and include `BREAKING CHANGE:` footer

**Issue references?** - Is this linked to any issues?
- `Fixes #123` - for bug fixes
- `Closes #456` - for any issue type
- `Relates to #789` - for references without closing

---

## Write the Commit Message

### Header (always)

```
type(scope): short description
```

Examples:
- `feat(auth): add two-factor authentication`
- `fix(payment): prevent duplicate charges`
- `docs(readme): add installation guide`

Rules for header:
- Type lowercase
- Scope lowercase
- Description starts lowercase
- Use imperative mood ("add" not "added")
- No period at end
- Keep under 50 characters

### Body (if needed)

Add a body when:
- Change is complex and needs explanation
- Multiple related changes
- Breaking change needs migration info

Format:
- Blank line after header
- Explain WHY the change was made
- Keep lines under 72 characters
- Use bullet points for lists

Example:

```
feat(auth): add JWT token support

Implement JWT tokens for stateless authentication across the API.

- Add JWT generation and validation service
- Update authentication middleware
- Add refresh token endpoint
- Add token expiration handling
```

### Footer (if needed)

Add footer for breaking changes or issue references.

**Breaking change example**:

```
feat(api)!: restructure response format

BREAKING CHANGE: User endpoints now return nested structure

Before:
{ "id": 1, "name": "John" }

After:
{ "user": { "id": 1, "name": "John" } }

Migration: Update clients to access response.user

Closes #567
```

**Issue reference example**:

```
fix(payment): prevent duplicate charges

Users could be charged twice when clicking submit multiple times.

- Add idempotency keys to payment requests
- Disable button during processing
- Add concurrency tests

Fixes #834
```

---

## Execute the Commit

Build the complete message and use heredoc format:

```bash
git commit -m "$(cat <<'EOF'
type(scope): description

Body explaining the change if needed.

BREAKING CHANGE: or issue references if needed
Fixes #123
EOF
)"
```

Important: Use single quotes in `<<'EOF'` to prevent shell expansion.

---

## Verify Success

After committing, verify:

```bash
git log -1 --format=fuller
```

Check that:
- Message is correct
- No Claude Code signatures present
- Author is correct
- All changes included

---

## Critical Rules

**Always do**:
- Use imperative mood (add, fix, remove)
- Keep header under 50 characters
- Use heredoc for multi-line messages
- Mark breaking changes with ! and BREAKING CHANGE footer
- Verify after committing

**Never do**:
- Add Claude Code signatures
- Add "Generated with Claude Code" references
- Add "Co-Authored-By: Claude" lines
- Add tool attribution
- Use past tense in description
- Capitalize description (unless proper noun)

---

## Multiple Changes

If changes contain multiple unrelated things:
- Create separate commits for each logical change
- One commit = one logical unit

Example:
```bash
# Commit 1
feat(api): add user endpoint

# Commit 2
chore(deps): upgrade TypeScript

# Commit 3
docs: update API documentation
```

---

## See Also

Detailed examples and patterns: [EXAMPLE.md](EXAMPLE.md)
