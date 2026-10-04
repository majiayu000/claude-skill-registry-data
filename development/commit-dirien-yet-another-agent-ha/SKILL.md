---
name: commit
description: "Atomic, semantic-boundary git commit workflow"
---

# /commit — Atomic Commit Workflow

## When to use
When the user runs /commit or asks to commit changes.

## Steps

1. Run `git status` and `git diff --staged` to understand what's changed
2. If nothing is staged, identify logical change groups and stage them separately
3. Write a commit message following Conventional Commits:
   - feat: new feature
   - fix: bug fix
   - refactor: code restructuring
   - docs: documentation
   - test: tests
   - chore: tooling/build
4. Use the imperative mood in the subject line
5. Keep subject under 72 characters
6. Add body with "why" not "what" if the change isn't self-evident
7. Create the commit using a heredoc for the message
8. Run `git status` to verify

## Rules
- NEVER use --no-verify or --amend unless explicitly asked
- NEVER stage .env, credentials, or secret files
- Prefer multiple small commits over one large commit
- Each commit should compile and pass tests independently
