---
name: committing-code
description: Writes git commit messages using conventional commits format with gitmoji. Use when creating git commits, preparing commit messages, or when the user asks to commit changes. Triggers on "commit", "git commit", "save changes", or any request to record changes to version control.
---

# Committing Code

## Overview

**Every commit message uses conventional commits with gitmoji.** The format is consistent, scannable, and conveys intent at a glance.

## Format

```
<emoji> <type>: <short description>

<body — what changed and why>

Co-Authored-By: Claude <agent> <noreply@anthropic.com>
```

The short description is imperative mood, lowercase, no period. The body uses bullet points for multiple changes.

## Gitmoji Reference

| Emoji | Type | When to use |
|-------|------|-------------|
| 🎉 | `feat` | Initial commit / first commit in a repo |
| ✨ | `feat` | New feature or capability |
| 🐛 | `fix` | Bug fix |
| ♻️ | `refactor` | Code restructuring without behavior change |
| 📝 | `docs` | Documentation only |
| 🔧 | `chore` | Config, tooling, non-code changes |
| ✅ | `test` | Adding or updating tests |
| 🚀 | `perf` | Performance improvement |
| 🔥 | `chore` | Removing code or files |
| 🏗️ | `refactor` | Architectural change |
| 💄 | `style` | UI/cosmetic change |
| 🔒 | `security` | Security fix |
| ⬆️ | `chore` | Dependency upgrade |
| 🚚 | `refactor` | Moving or renaming files |

## Examples

**Good:**
```
✨ feat: add user authentication with JWT

- Add login/logout endpoints in auth.controller.ts
- Add JWT middleware for protected routes
- Add refresh token rotation
- Add auth integration tests

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
🐛 fix: prevent race condition in websocket reconnect

The reconnect logic was firing multiple times when the connection
dropped during a message send, causing duplicate subscriptions.
Added a mutex guard around the reconnect path.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

```
♻️ refactor: rename getUserById to fetchUser across codebase

Aligns with the fetch* naming convention for async data access.
Updated all call sites, tests, and type definitions.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Bad:**
```
updated stuff          # No type, no emoji, vague
feat: Add Feature      # No emoji, capitalized
✨ feat: add feature.  # Trailing period
🐛✨ fix/feat: stuff   # Multiple types
```

## Rules

1. **One type per commit.** If changes span multiple types, split into multiple commits.
2. **Body explains WHY, not just WHAT.** The diff shows what changed — the message explains the reasoning.
3. **Use bullet points** in the body when listing multiple changes.
4. **Always include Co-Authored-By** when the commit was AI-assisted.
5. **Use HEREDOC** for multi-line messages to preserve formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   ✨ feat: add new feature

   Body text here.

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

## Commit Frequency

Commit early and often:
- After each logical unit of work (one feature, one fix, one refactor)
- After adding a new file or skill
- After updating documentation alongside code changes
- **Never** batch unrelated changes into a single commit

## Pre-Commit Checklist

Before committing, verify:
- **README.md** is updated if the change affects user-facing documentation (new features, skills, APIs, installation steps)
- **AGENTS.md** is updated if the change affects project structure, conventions, or available skills
- Documentation changes are part of the same commit as the code they describe — not a separate "docs" commit after the fact
