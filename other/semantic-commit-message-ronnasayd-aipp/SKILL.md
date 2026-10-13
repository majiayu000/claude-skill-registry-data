---
name: semantic-commit-message
description: "Generate Conventional Commit messages in English based on staged git diffs. Use this skill whenever the user asks for a commit message, semantic/Conventional Commits, or wants a commit based on staged changes, even if they just say 'write my commit message' or 'help with commit title'."
---

Your objective is to produce a Conventional Commit message in English by analyzing staged changes only.

Do not run `git commit`. Only generate the message.

====================
PHASE 1 — CONTEXT
====================

1. Run `git status -sb` to understand the staging state.
2. Run `git diff --staged` to inspect the actual staged changes.
3. If `git diff --staged` is empty, tell the user there are no staged changes and ask them to stage files before you can generate a commit message.

====================
PHASE 2 — TYPE SELECTION
====================

Choose the most accurate type based on the diff:

- `feat`: New user-facing functionality.
- `fix`: Bug fixes or incorrect behavior corrections.
- `docs`: Documentation-only changes.
- `style`: Formatting, whitespace, linting, no functional change.
- `refactor`: Code changes that neither fix a bug nor add a feature.
- `perf`: Performance improvements.
- `test`: Adding or updating tests only.
- `build`: Build system or dependency changes.
- `ci`: CI/CD configuration changes.
- `chore`: Maintenance tasks (non-code changes not covered above).
- `revert`: Reverts a previous commit.

If multiple types apply, pick the most user-visible or behavior-impacting change. If still ambiguous, present two options and ask the user to choose.

====================
PHASE 3 — SCOPE
====================

Infer a scope from the dominant top-level folder or package when clear (e.g., `api`, `ui`, `auth`, `docs`). If changes are spread across unrelated areas, omit the scope.

Examples:

- `feat(auth): add password reset flow`
- `docs: update installation guide`

====================
PHASE 4 — SUBJECT LINE
====================

Write the subject in English following these rules:

- Imperative mood (e.g., "add", "fix", "update", "remove")
- Lowercase (except proper nouns)
- No trailing period
- 72 characters or fewer

====================
PHASE 5 — BREAKING CHANGES
====================

If the diff includes a breaking change:

- Add `!` after the type or scope (e.g., `feat!: remove legacy auth`)
- Add a footer:
  `BREAKING CHANGE: <clear description of the breaking change>`

====================
OUTPUT
====================

Return exactly one recommended commit message in a Markdown code block.
Use a single line unless a breaking change requires a footer.

====================
EXAMPLES
====================

**Example 1**
Input: Added a new password reset endpoint under `api/auth`.
Output:

```text
feat(auth): add password reset endpoint
```

**Example 2**
Input: Updated README and installation docs only.
Output:

```text
docs: update installation guide
```
