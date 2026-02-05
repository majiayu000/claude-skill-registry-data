---
name: dev-swarm-draft-commit-message
description: Draft a conventional commit message when the user asks to commit code.
metadata:
  short-description: Draft an informative commit message.
---

# AI Builder - Draft Commit Message

This skill drafts conventional commit messages that accurately summarize code changes based on git diff output.

## When to Use This Skill

- User asks to commit code changes
- User requests a commit message draft
- User wants to create a conventional commit message
- Before committing changes to version control

## Your Roles in This Skill

- **DevOps Engineer**: Review git diff output and analyze code changes. Identify the type of change (feat, fix, refactor, etc.). Determine the scope of changes and affected components. Draft clear, concise commit messages following conventional commits format.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Draft a conventional commit message that matches the change summary by git diff.

Requirements:
- Use `git diff` command first, then summary the changes
- Use the Conventional Commits format: `type(scope): summary`
- Use the imperative mood in the summary (for example, "Add", "Fix", "Refactor")
- Keep the summary under 72 characters
- If there are breaking changes, include a `BREAKING CHANGE:` footer

**Atomic Commits - One Task Per Commit**:
- **IMPORTANT**: Each commit should represent ONE atomic task only
- Create separate commits for:
  - Different types of changes (feature vs bugfix vs docs vs refactor)
  - Different features (feature A vs feature B)
  - Different bugfixes (bug X vs bug Y)
  - Different refactorings (refactor component A vs component B)
- Each commit should focus on ONE logical change with a short, clear message
- Avoid multi-line commit messages that describe multiple unrelated changes
- This creates a clean, atomic commit history that's easier to review, revert, and understand
- Examples:
  - Instead of: "Add feature X and feature Y" → Create two commits: `feat: add feature X`, `feat: add feature Y`
  - Instead of: "Fix bug A and bug B" → Create two commits: `fix: resolve bug A`, `fix: resolve bug B`
  - Instead of: "Add feature X, fix bug Y, update docs" → Create three commits: `feat: add feature X`, `fix: resolve bug Y`, `docs: update API documentation`

Do not add content as below, to make the message shorter
```
Generated with xx
Co-Authored-By: xxx
``
