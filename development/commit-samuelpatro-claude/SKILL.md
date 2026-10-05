---
name: commit
effort: low
allowed-tools: Read, Grep, Glob, Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*)
description: >
  Create atomic git commits with terse, exact Conventional Commits messages.
  Cuts noise, preserves intent. Subject ≤50 chars. Body only when "why" isn't obvious.
  Use when the user says "commit", "commit this", "/commit", or asks to stage and commit changes.
---

## Context

- Current git status: !`git status --short`
- Diff summary (file + line counts): !`git diff HEAD --stat`
- Current branch: !`git branch --show-current`
- Recent commits (for style matching): !`git log --oneline -10`

The full diff is intentionally NOT loaded above. Read hunks on demand with `git diff HEAD -- <file>` for only the files you need to inspect to write the message and decide splits. Do not run `git diff HEAD` with no path filter.

## Your task

Create atomic, self-contained commits with terse, exact messages. Conventional Commits format. No fluff. Why over what.

### Commit Splitting

Split into multiple commits when changes involve:

- **Different concerns** — unrelated parts of the codebase
- **Different types** — mixing feat/fix/refactor/tests/docs/config
- **Different file patterns** — source vs docs vs config
- **Large changesets** — break down for reviewability

Each commit must build and make sense on its own. If all changes relate to one concern, a single commit is fine.

### Message Rules

**Subject line:**
- `<type>(<scope>): <imperative summary>` — `<scope>` optional
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`
- Imperative mood: "add", "fix", "remove" — not "added", "adds", "adding"
- ≤50 chars when possible, hard cap 72
- No trailing period
- Match project convention for capitalization after the colon (check recent commits above)

**Body (only if needed):**
- Skip entirely when the subject is self-explanatory
- Add body only for: non-obvious *why*, breaking changes, migration notes, linked issues
- Wrap at 72 chars
- Bullets `-` not `*`
- Reference issues/PRs at end: `Closes #42`, `Refs #17`

**Auto-clarity — always include body for:** breaking changes, security fixes, data migrations, revert commits. Never compress these into subject-only; future debuggers need the context.

**Breaking changes:** mark subject with `!` and add a `BREAKING CHANGE:` footer explaining the migration.

```
feat(api)!: rename /v1/orders to /v1/checkout

BREAKING CHANGE: clients on /v1/orders must migrate to /v1/checkout
before 2026-06-01. Old route returns 410 after that date.
```

**What NEVER goes in:**
- "This commit does X", "I", "we", "now", "currently" — the diff says what
- "As requested by..." — use `Co-authored-by:` trailer instead
- AI attribution: "Generated with Claude Code", co-authorship footers, 🤖 emoji
- Emoji unless project convention requires
- Restating the filename when the scope already covers it

### Examples

Trivial change, no body needed:
```
fix(auth): handle expired refresh token
```

Non-obvious why — body explains motivation:
```
feat(api): add GET /users/:id/profile

Mobile client needs profile data without the full user payload
to reduce LTE bandwidth on cold-launch screens.

Closes #128
```

Breaking change:
```
feat(api)!: rename /v1/orders to /v1/checkout

BREAKING CHANGE: clients on /v1/orders must migrate to /v1/checkout
before 2026-06-01. Old route returns 410 after that date.
```

### HEREDOC Format

```
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body if needed>
EOF
)"
```

### Staging Rules

- Stage specific files by name — do NOT use `git add -A` or `git add .`
- NEVER stage files that may contain secrets: `.env`, `.env.*`, `credentials.json`, `*.key`, `*.pem`, `*.p12`, `id_rsa*`, `token.json`, `secret*`. Warn the user and skip them.
- If all changes are already staged, do not re-stage them.

### Edge Cases

- No changes (nothing staged, nothing modified): say so and stop. Do not create an empty commit.
- Only untracked files that look like generated artifacts (`dist/`, `node_modules/`, `*.log`): warn the user instead of committing them.
- If the user says "normal mode" or "verbose commit": allow a longer, descriptive style for this commit only.
