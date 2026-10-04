---
name: caveman-commit
description: Write a terse, exact Conventional Commits message from the intended diff. Use when asked for a commit message, when `/commit` or `/caveman-commit` is invoked, or when another workflow needs to name a commit.
---

# Caveman commit

Generate the message only. Do not stage files, create or amend a commit, rewrite history, or push unless another active workflow and the user authorize those actions.

## Inspect the change

Read the repository's contribution rules and recent commit subjects. Prefer the staged diff and its status:

```sh
git status --short
git diff --cached --stat
git diff --cached
git log -10 --format=%s
```

If nothing is staged, inspect only the diff the user identifies. Do not guess that every working-tree change belongs in one commit.

## Write the subject

Use this form unless the repository has a different established convention:

```text
<type>(<scope>): <imperative summary>
```

- Scope is optional.
- Use `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, or `revert`.
- Start the summary with an imperative verb such as `add`, `fix`, or `remove`.
- Keep it at 50 characters when practical and never exceed 72.
- Omit the trailing period.
- Match the project's capitalization convention.
- Describe the behavior or intent, not a list of edited files.

## Add a body only when it earns its space

Use a body for a non-obvious reason, a breaking change, a security fix, a data migration, a revert, a compatibility constraint, or a linked issue. Wrap prose at 72 characters. Put issue trailers at the end, such as `Closes #42` or `Refs #17`.

For a breaking change, mark the subject with `!` and add a `BREAKING CHANGE:` paragraph that explains the migration.

Do not include filler such as "this commit," narration of the diff, AI attribution, emoji, or author commentary unless repository policy explicitly requires it.

## Output

Return one ready-to-use message in a fenced text block. Add alternatives only when the actual intent is ambiguous, and state the ambiguity briefly.
