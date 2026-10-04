---
name: generate-commit-message
description: >-
  Generate a Conventional Commit message from the repository's staged Git changes. Use when asked to write a commit
  message or commit title. Return only the message in a plaintext code block. Does not stage files or create commits.
---

# Generate Commit Message

Create a commit message for the repository's current staged changes.

## Workflow

1. Inspect the git index without changing it:

   ```bash
   git status --short
   git diff --cached --stat
   git diff --cached
   ```

2. Base the message only on staged changes. Ignore unstaged and untracked changes except to avoid mixing them into the
   staged summary.
3. If there are no staged changes, output a plaintext code block containing exactly:

   ```text
   chore: no staged changes
   ```

## Message Rules

- Use Conventional Commit format:

  ```text
  <type>(optional-scope): <imperative summary>
  ```

- Allowed types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `build`, `ci`.
- Put the most important staged change first.
- If there is room on the same line, include minor staged changes after the primary change.
- Keep the subject concise and readable. Prefer one line unless extra context is genuinely needed.
- Use imperative mood: `add`, `fix`, `update`, `remove`, `refactor`, not `added`, `fixes`, or `updated`.
- Do not mention file paths unless they are the clearest useful scope.

## Optional Body

Add body text only when it is important and genuinely needed for context, such as a breaking behavior change, migration
note, or significant secondary changes that do not fit in the subject.

When a body is needed:

- Keep it short.
- Use markdown list bullets instead of paragraphs.
- Include only important staged changes.

Example:

```text
feat(auth): add passkey enrollment and tighten session renewal

- Requires a new WebAuthn origin setting in production.
- Moves legacy session cleanup behind the renewal path.
```

## Output Contract

Output nothing except one plaintext code block containing the exact commit message.

Do not add explanations, labels, summaries, caveats, follow-up questions, or text outside the code block.
