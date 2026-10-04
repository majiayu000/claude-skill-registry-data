---
name: commit-all
description: Create git commits in logical groups for all current changes
---

# Smart Commit

Create logically grouped git commits following project conventions.

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
4. Analyze changes
5. Determine logical groups of features in current diff
6. Pick type and scope from the changes in each group
7. Generate appropriate messages
8. Stage relevant files with `git add`
9. Create commit with HEREDOC format, leaving out the blank line and `<body>` when there is no body:
   ```bash
   git commit -F - <<'EOF'
   <type>(<scope>): <subject>

   <body>
   EOF
   ```
10. Repeat for each logical group of changes
11. Run `git status` to verify

## Safety Rules

- NEVER commit `.env` or credential files
- NEVER use `--amend` unless explicitly requested
- NEVER push
- NEVER skip hooks with `--no-verify`

## Example

```bash
git add src/preferences/
git commit -F - <<'EOF'
feat(preferences): add user preferences endpoint

Preferences lived in local storage, so every new device started empty.
EOF
```
