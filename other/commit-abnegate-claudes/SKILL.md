---
name: commit
description: Create a git commit with conventional commit message
argument-hint: "[message]"
---

# Smart Commit

Create a git commit following project conventions.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>
```

- **type**: one of the Types below.
- **scope** (optional): the area touched, in lowercase kebab-case, e.g. `fix(auth): handle expired sessions`. Omit it for repo-wide changes.
- **`!`** right before the colon marks a breaking change: `feat(api)!: remove v1 routes`.
- **subject**: lowercase imperative, no trailing period.
- **body** (optional): one short paragraph with only the *why* (rationale, tradeoffs, the reason behind a non-obvious value). Never restate what changed. When the subject says enough, leave out the body and the blank line before it.
- Keep every line within 72 characters.
- No co-authors: no `Co-Authored-By` trailer.

## Types

| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `refactor` | Code restructuring |
| `chore` | Maintenance |
| `docs` | Documentation |
| `test` | Tests |
| `style` | Formatting |
| `perf` | Performance |

## Execution Steps

1. Run `git status` to see changes (never use `-uall`)
2. Run `git diff --staged` and `git diff` to understand changes
3. Run `git log --oneline -5` to see which scopes recent commits use (never copy the legacy `(type): subject` form)
4. If `$ARGUMENTS` provided, use as commit message
5. If no `$ARGUMENTS`:
   - Analyze changes
   - Pick type and scope from the changes
   - Generate appropriate message
6. Stage relevant files with `git add`
7. Create commit with HEREDOC format, leaving out the blank line and `<body>` when there is no body:
   ```bash
   git commit -F - <<'EOF'
   <type>(<scope>): <subject>

   <body>
   EOF
   ```
8. Run `git status` to verify

## Safety Rules

- NEVER commit `.env` or credential files
- NEVER use `--amend` unless explicitly requested
- NEVER use `--force` push
- NEVER skip hooks with `--no-verify`

## Example

```bash
git add src/preferences/
git commit -F - <<'EOF'
feat(preferences): add user preferences endpoint

Preferences lived in local storage, so every new device started empty.
EOF
```
